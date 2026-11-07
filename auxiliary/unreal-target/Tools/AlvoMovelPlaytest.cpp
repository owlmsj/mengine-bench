#define NOMINMAX
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cwchar>
#include <iterator>
#include <string>
#include <thread>

struct WindowSearch
{
    std::wstring ExpectedExecutable;
    HWND Window = nullptr;
};

static BOOL CALLBACK FindGameWindow(HWND window, LPARAM parameter)
{
    auto& search = *reinterpret_cast<WindowSearch*>(parameter);
    if (!IsWindowVisible(window) || GetWindow(window, GW_OWNER)) return TRUE;
    DWORD processId = 0;
    GetWindowThreadProcessId(window, &processId);
    HANDLE process = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, processId);
    if (!process) return TRUE;
    wchar_t path[32768] = {};
    DWORD size = static_cast<DWORD>(std::size(path));
    const bool matches = QueryFullProcessImageNameW(process, 0, path, &size) &&
        _wcsicmp(path, search.ExpectedExecutable.c_str()) == 0;
    CloseHandle(process);
    if (!matches) return TRUE;
    search.Window = window;
    return FALSE;
}

static HWND LocateGame(WindowSearch& search)
{
    search.Window = nullptr;
    EnumWindows(FindGameWindow, reinterpret_cast<LPARAM>(&search));
    return search.Window;
}

static bool FocusGame(HWND window)
{
    DWORD ignored = 0;
    const DWORD current = GetCurrentThreadId();
    const DWORD foreground = GetWindowThreadProcessId(GetForegroundWindow(), &ignored);
    const bool attached = foreground && foreground != current && AttachThreadInput(current, foreground, TRUE);
    ShowWindow(window, SW_RESTORE);
    MONITORINFO monitor = {};
    monitor.cbSize = sizeof(monitor);
    if (GetMonitorInfoW(MonitorFromWindow(window, MONITOR_DEFAULTTONEAREST), &monitor))
        SetWindowPos(window, HWND_TOP, monitor.rcWork.left + 20, monitor.rcWork.top + 20, 0, 0, SWP_NOSIZE | SWP_SHOWWINDOW);
    BringWindowToTop(window);
    SetForegroundWindow(window);
    if (attached) AttachThreadInput(current, foreground, FALSE);
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    return GetForegroundWindow() == window;
}

static bool PressKey(WORD key)
{
    INPUT inputs[2] = {};
    inputs[0].type = INPUT_KEYBOARD;
    inputs[0].ki.wVk = key;
    inputs[1] = inputs[0];
    inputs[1].ki.dwFlags = KEYEVENTF_KEYUP;
    return SendInput(2, inputs, sizeof(INPUT)) == 2;
}

static bool MoveMouse(int dx, int dy)
{
    INPUT input = {};
    input.type = INPUT_MOUSE;
    input.mi.dx = dx;
    input.mi.dy = dy;
    input.mi.dwFlags = MOUSEEVENTF_MOVE;
    return SendInput(1, &input, sizeof(INPUT)) == 1;
}

static bool Fire()
{
    INPUT inputs[2] = {};
    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTUP;
    return SendInput(2, inputs, sizeof(INPUT)) == 2;
}

struct RedTarget
{
    int X = 0;
    int Y = 0;
    int Width = 0;
    int Height = 0;
    int Pixels = 0;
};

static RedTarget FindRedTarget(HWND window)
{
    RECT rect = {};
    POINT origin = {};
    if (!GetClientRect(window, &rect) || !ClientToScreen(window, &origin)) return {};
    const int width = rect.right - rect.left;
    const int height = rect.bottom - rect.top;
    if (width <= 0 || height <= 0 || width > 7680 || height > 4320) return {};
    HDC screen = GetDC(nullptr);
    if (!screen) return {};
    HDC memory = CreateCompatibleDC(screen);
    BITMAPINFO info = {};
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = width;
    info.bmiHeader.biHeight = -height;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;
    void* pixels = nullptr;
    HBITMAP bitmap = CreateDIBSection(screen, &info, DIB_RGB_COLORS, &pixels, nullptr, 0);
    if (!memory || !bitmap || !pixels)
    {
        if (bitmap) DeleteObject(bitmap);
        if (memory) DeleteDC(memory);
        ReleaseDC(nullptr, screen);
        return {};
    }
    HGDIOBJ old = SelectObject(memory, bitmap);
    const bool copied = BitBlt(memory, 0, 0, width, height, screen, origin.x, origin.y, SRCCOPY | CAPTUREBLT);
    RedTarget result;
    long long xTotal = 0, yTotal = 0;
    int minX = width, minY = height, maxX = 0, maxY = 0;
    if (copied)
    {
        const auto* bytes = static_cast<const unsigned char*>(pixels);
        for (int y = 2; y < height - 2; y += 2)
            for (int x = 2; x < width - 2; x += 2)
            {
                const unsigned char* pixel = bytes + (static_cast<size_t>(y) * width + x) * 4;
                const int b = pixel[0], g = pixel[1], r = pixel[2];
                if (r < 75 || r * 10 < g * 15 || r * 10 < b * 15) continue;
                ++result.Pixels;
                xTotal += x;
                yTotal += y;
                minX = std::min(minX, x); maxX = std::max(maxX, x);
                minY = std::min(minY, y); maxY = std::max(maxY, y);
            }
        if (result.Pixels > 12)
        {
            result.X = static_cast<int>(xTotal / result.Pixels);
            result.Y = static_cast<int>(yTotal / result.Pixels);
            result.Width = maxX - minX;
            result.Height = maxY - minY;
        }
    }
    SelectObject(memory, old);
    DeleteObject(bitmap);
    DeleteDC(memory);
    ReleaseDC(nullptr, screen);
    return result;
}

int main(int argc, char** argv)
{
    SetConsoleOutputCP(CP_UTF8);
    const bool keepOpen = argc > 1 && std::string(argv[1]) == "--keep-open";
    SetProcessDPIAware();
    wchar_t executable[32768] = {};
    const DWORD length = GetModuleFileNameW(nullptr, executable, static_cast<DWORD>(std::size(executable)));
    if (!length || length >= std::size(executable)) { std::puts("Não foi possível localizar a pasta do playtest."); return 1; }
    std::wstring root(executable, length);
    const size_t slash = root.find_last_of(L"\\/");
    if (slash == std::wstring::npos) { std::puts("Caminho do playtest inválido."); return 1; }
    root.resize(slash);
    WindowSearch search { root + L"\\AlvoMovel\\Binaries\\Win64\\AlvoMovel-Win64-Shipping.exe" };
    if (LocateGame(search)) { std::puts("Feche o jogo desta pasta antes de iniciar o playtest."); return 1; }
    std::wstring command = L"\"" + root + L"\\AlvoMovel.exe\"";
    STARTUPINFOW startup = {};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION child = {};
    if (!CreateProcessW(nullptr, command.data(), nullptr, nullptr, FALSE, 0, nullptr, root.c_str(), &startup, &child))
    { std::printf("Não foi possível iniciar o jogo. Erro do Windows: %lu.\n", GetLastError()); return 1; }
    CloseHandle(child.hThread);
    CloseHandle(child.hProcess);
    HWND window = nullptr;
    for (int attempt = 0; attempt < 300 && !window; ++attempt)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        window = LocateGame(search);
    }
    if (!window || !FocusGame(window)) { std::puts("A janela do jogo não abriu ou não recebeu o foco."); return 1; }
    std::this_thread::sleep_for(std::chrono::seconds(2));
    if (GetForegroundWindow() != window) { std::puts("O jogo perdeu o foco; nenhum comando foi enviado."); return 1; }
    if (!PressKey(VK_RETURN)) { std::puts("Falha ao enviar o comando de início."); return 1; }
    const auto started = std::chrono::steady_clock::now();
    auto lastShot = started - std::chrono::seconds(1);
    int detectedFrames = 0, shots = 0;
    while (std::chrono::steady_clock::now() - started < std::chrono::milliseconds(15300))
    {
        if (!IsWindow(window) || GetForegroundWindow() != window)
        { std::puts("O jogo perdeu o foco; o playtest foi interrompido."); return 1; }
        RECT client = {};
        if (!GetClientRect(window, &client)) return 1;
        const RedTarget target = FindRedTarget(window);
        if (target.Pixels > 12 && target.Width < client.right / 2 && target.Height < client.bottom / 2)
        {
            ++detectedFrames;
            const int dx = target.X - client.right / 2;
            const int dy = target.Y - client.bottom / 2;
            const int marginX = std::max(8, target.Width / 3);
            const int marginY = std::max(8, target.Height / 3);
            if (std::abs(dx) < marginX && std::abs(dy) < marginY &&
                std::chrono::steady_clock::now() - lastShot > std::chrono::milliseconds(200))
            {
                if (!Fire()) { std::puts("Falha ao enviar o tiro."); return 1; }
                lastShot = std::chrono::steady_clock::now(); ++shots;
            }
            else if (!MoveMouse(std::clamp(static_cast<int>(dx * 0.45), -80, 80),
                                std::clamp(static_cast<int>(dy * 0.45), -80, 80)))
            { std::puts("Falha ao enviar o movimento do mouse."); return 1; }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    std::printf("Quadros com alvo detectado: %d; tiros enviados: %d.\n", detectedFrames, shots);
    if (keepOpen) { std::puts("O jogo permanece aberto na tela de resultado."); return 0; }
    std::this_thread::sleep_for(std::chrono::seconds(1));
    if (GetForegroundWindow() != window) { std::puts("O jogo perdeu o foco antes do replay; nenhum comando foi enviado."); return 1; }
    if (!PressKey('R')) { std::puts("Falha ao enviar o comando de replay."); return 1; }
    std::this_thread::sleep_for(std::chrono::milliseconds(400));
    if (!PressKey(VK_ESCAPE)) { std::puts("Falha ao enviar o comando de saída."); return 1; }
    for (int attempt = 0; attempt < 50 && IsWindow(window); ++attempt)
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    if (IsWindow(window)) { std::puts("O jogo não foi encerrado."); return 1; }
    std::puts("Comando de replay enviado; saída do jogo confirmada.");
    return 0;
}
