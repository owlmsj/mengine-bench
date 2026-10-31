"""Own every process a run starts, so that none outlives it (owlmsj/mengine#785).

A parent-to-child walk cannot find a process whose parent already exited, which
is what PowerShell `Start-Process` and any daemon leave behind. So membership is
decided when the process starts: a Windows Job or a POSIX session. On Windows a
Job is not enough: packaged pwsh 7.6.9 creates every child outside the caller's
Job, measured even when the Job denies breakaway, so DescendantWatch reads the
parent links while they last. What leaves on purpose is then found by what it
holds: the workspace as its current directory or on its command line.
"""

from __future__ import annotations

import ctypes
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil

KILL_WAIT_S = 10
POLL_S = 0.05
OBSERVE_EVERY_S = 0.25


class OrphanSurvived(RuntimeError):
    """A process of this run could not be killed."""


def _settle(procs: list[psutil.Process]) -> None:
    for proc in procs:
        try:
            proc.kill()
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied as exc:
            raise OrphanSurvived(f"received AccessDenied killing pid {proc.pid}; expected to own it") from exc
    _gone, alive = psutil.wait_procs(procs, timeout=KILL_WAIT_S)
    if alive:
        raise OrphanSurvived(f"received survivors {[p.pid for p in alive]} after {KILL_WAIT_S}s; expected none")


class PosixSession:
    """The process leads a new session; every descendant that stays in it is found by session id."""

    popen_kwargs: dict[str, object] = {"start_new_session": True}

    def __init__(self) -> None:
        self._sid: int | None = None

    def adopt(self, proc: subprocess.Popen[bytes]) -> None:
        self._sid = proc.pid

    def kill_all(self, root_pid: int) -> int:
        if self._sid is None:
            return 0
        members = []
        for candidate in psutil.process_iter():
            try:
                if candidate.pid != root_pid and os.getsid(candidate.pid) == self._sid:
                    members.append(candidate)
            except (OSError, psutil.Error):
                continue
        alive = [proc for proc in members if proc.status() != psutil.STATUS_ZOMBIE]
        _settle(alive)
        return len(alive)

    def close(self) -> None:
        self._sid = None


class DescendantWatch:
    """Everything born under `root_pid`, read from parent links while they exist."""

    def __init__(self, root_pid: int) -> None:
        self._lock = threading.Lock()
        self._stop = threading.Event()
        # pid to creation time, so a reused pid is never mistaken for a descendant.
        self._born = {root_pid: self._created(root_pid) or 0.0}
        threading.Thread(target=self._watch, name="bench-descendants", daemon=True).start()

    @staticmethod
    def _created(pid: int) -> float | None:
        try:
            return psutil.Process(pid).create_time()
        except psutil.Error:
            return None

    def _watch(self) -> None:
        while not self._stop.wait(OBSERVE_EVERY_S):
            with self._lock:
                self._observe()

    def _observe(self) -> None:
        # One snapshot for all rows; Process.ppid() would take one per process on Windows.
        rows = psutil._ppid_map()
        known = -1
        while known != len(self._born):
            known = len(self._born)
            for pid, parent in rows.items():
                if pid in self._born or parent not in self._born:
                    continue
                created = self._created(pid)
                if created is not None and created >= self._born[parent]:
                    self._born[pid] = created
        # This snapshot already lists every child of a parent that just died, so the
        # parent can go: keeping it would let a reused pid adopt strangers.
        self._born = {pid: created for pid, created in self._born.items() if self._created(pid) == created}

    def stop(self) -> None:
        self._stop.set()

    def kill_all(self) -> int:
        self._stop.set()
        with self._lock:
            self._observe()
            alive = [psutil.Process(pid) for pid in self._born if self._created(pid) is not None]
        _settle(alive)
        return len(alive)


class WindowsJob:
    """Suspended start, then the Job, then resume: no child can run before it belongs to the Job."""

    CREATE_SUSPENDED = 0x00000004
    KILL_ON_JOB_CLOSE = 0x00002000
    EXTENDED_LIMIT_INFORMATION = 9
    BASIC_ACCOUNTING_INFORMATION = 1

    popen_kwargs: dict[str, object] = {"creationflags": CREATE_SUSPENDED}

    def __init__(self) -> None:
        from ctypes import wintypes

        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._ntdll = ctypes.WinDLL("ntdll")
        handle = wintypes.HANDLE
        for name, args, result in (
            ("CreateJobObjectW", (wintypes.LPVOID, wintypes.LPCWSTR), handle),
            ("SetInformationJobObject", (handle, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD), wintypes.BOOL),
            ("AssignProcessToJobObject", (handle, handle), wintypes.BOOL),
            ("QueryInformationJobObject",
             (handle, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID), wintypes.BOOL),
            ("TerminateJobObject", (handle, wintypes.UINT), wintypes.BOOL),
            ("CloseHandle", (handle,), wintypes.BOOL),
        ):
            function = getattr(self._kernel32, name)
            function.argtypes, function.restype = args, result
        self._ntdll.NtResumeProcess.argtypes, self._ntdll.NtResumeProcess.restype = (handle,), ctypes.c_long
        self._job = self._kernel32.CreateJobObjectW(None, None)
        if not self._job:
            raise OSError(ctypes.get_last_error(), "received no Job from CreateJobObjectW; expected a handle")

        class Basic(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class Extended(ctypes.Structure):
            _fields_ = [("Basic", Basic), ("Io", ctypes.c_uint64 * 6), ("ProcessMemoryLimit", ctypes.c_size_t),
                        ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                        ("PeakJobMemoryUsed", ctypes.c_size_t)]

        limits = Extended()
        limits.Basic.LimitFlags = self.KILL_ON_JOB_CLOSE
        if not self._kernel32.SetInformationJobObject(self._job, self.EXTENDED_LIMIT_INFORMATION,
                                                      ctypes.byref(limits), ctypes.sizeof(limits)):
            raise OSError(ctypes.get_last_error(), "received failure setting KILL_ON_JOB_CLOSE; expected success")
        self._descendants: DescendantWatch | None = None

    def adopt(self, proc: subprocess.Popen[bytes]) -> None:
        process = int(proc._handle)  # type: ignore[attr-defined]
        if not self._kernel32.AssignProcessToJobObject(self._job, process):
            error = ctypes.get_last_error()
            proc.kill()
            raise OSError(error, f"received failure assigning pid {proc.pid} to its Job; expected it contained")
        self._descendants = DescendantWatch(proc.pid)
        status = self._ntdll.NtResumeProcess(process)
        if status != 0:
            proc.kill()
            raise OSError(status, f"received NTSTATUS {status:#x} resuming pid {proc.pid}; expected 0")

    def _active(self) -> int:
        from ctypes import wintypes

        class Accounting(ctypes.Structure):
            _fields_ = [("TotalUserTime", ctypes.c_int64), ("TotalKernelTime", ctypes.c_int64),
                        ("ThisPeriodTotalUserTime", ctypes.c_int64), ("ThisPeriodTotalKernelTime", ctypes.c_int64),
                        ("TotalPageFaultCount", wintypes.DWORD), ("TotalProcesses", wintypes.DWORD),
                        ("ActiveProcesses", wintypes.DWORD), ("TotalTerminatedProcesses", wintypes.DWORD)]

        info = Accounting()
        if not self._kernel32.QueryInformationJobObject(self._job, self.BASIC_ACCOUNTING_INFORMATION,
                                                        ctypes.byref(info), ctypes.sizeof(info), None):
            raise OSError(ctypes.get_last_error(), "received failure querying the Job; expected its process count")
        return int(info.ActiveProcesses)

    def kill_all(self, root_pid: int) -> int:
        # The root has already been waited for on a normal exit, so whatever is active is a leftover.
        leftovers = self._active()
        if not self._kernel32.TerminateJobObject(self._job, 1):
            raise OSError(ctypes.get_last_error(), "received failure terminating the Job; expected every member dead")
        deadline = time.monotonic() + KILL_WAIT_S
        while self._active():
            if time.monotonic() > deadline:
                raise OrphanSurvived(f"received {self._active()} live Job members after {KILL_WAIT_S}s; expected 0")
            time.sleep(POLL_S)
        if self._descendants is not None:
            leftovers += self._descendants.kill_all()
        return leftovers

    def close(self) -> None:
        if self._descendants is not None:
            self._descendants.stop()
        if self._job:
            self._kernel32.CloseHandle(self._job)
            self._job = None


def new_scope() -> PosixSession | WindowsJob:
    return WindowsJob() if sys.platform == "win32" else PosixSession()


def _path_forms(root: Path) -> set[str]:
    # TEMP can be an 8.3 short path while a process reports the long one.
    forms = {str(root), str(root.resolve())}
    return {os.path.normcase(form) for form in forms}


def _is_inside(path: str, forms: set[str]) -> bool:
    normal = os.path.normcase(path)
    return any(normal == form or normal.startswith(form + os.sep) for form in forms)


def sweep_workspace(root: Path) -> int:
    """Kill what still holds `root`, unless `root` also holds this runner (a broad directory, not a workspace)."""
    forms = _path_forms(root)
    if _is_inside(os.getcwd(), forms) or _is_inside(str(Path.home()), forms):
        return 0
    me = psutil.Process()
    keep = {me.pid, *(parent.pid for parent in me.parents())}
    holders = []
    for candidate in psutil.process_iter(["pid", "cwd", "cmdline"]):
        if candidate.info["pid"] in keep:
            continue
        cwd = candidate.info["cwd"] or ""
        cmdline = [os.path.normcase(part) for part in candidate.info["cmdline"] or []]
        if _is_inside(cwd, forms) or any(form in part for form in forms for part in cmdline):
            holders.append(candidate)
    _settle(holders)
    return len(holders)


def stop_session_group(pid: int) -> None:
    """Stop the leader's group on POSIX before its session is scanned; a no-op on Windows."""
    if sys.platform != "win32":
        try:
            os.killpg(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
