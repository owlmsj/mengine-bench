"""Unreal C++: the bug that shows only in a packaged build, the kind that costs the most in real game work (#103).

No engine and no compile: the agent reads sources, config and a crash log, and fixes them. The checks accept
every valid fix found so far, and refuse the ones Unreal itself would refuse.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import WROTE_RESULT, CheckResult, EvalTask, Step, checkpoints, read, result_json, write

HEADER = "Source/PixelArena/ArenaGameMode.h"
SOURCE = "Source/PixelArena/ArenaGameMode.cpp"
GAME_INI = "Config/DefaultGame.ini"
ASSET = "/Game/Data/Palettes/DA_Primary"

UE_FILES = {
    "README.md": """# Pixel Arena

A match game painted in primary colors, on Unreal Engine 5.

- `Source/PixelArena`: the game module.
- `Config`: project settings.
- `Saved/Logs/PixelArena-shipping.log`: log of the packaged run that crashed.
""",
    HEADER: """#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "ArenaGameMode.generated.h"

class UArenaHud;
class UArenaPalette;
class UArenaScoreTracker;
struct FArenaStats;

UCLASS()
class PIXELARENA_API AArenaGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type Reason) override;

	void OnGoalScored(int32 TeamIndex);

private:
	UPROPERTY()
	TObjectPtr<UArenaHud> Hud;

	UPROPERTY()
	TObjectPtr<UArenaPalette> Palette;

	UArenaScoreTracker* ScoreTracker = nullptr;

	// Plain C++ data owned by this class, freed in EndPlay.
	FArenaStats* Stats = nullptr;
};
""",
    SOURCE: """#include "ArenaGameMode.h"

#include "ArenaHud.h"
#include "ArenaPalette.h"
#include "ArenaScoreTracker.h"
#include "ArenaStats.h"

DEFINE_LOG_CATEGORY_STATIC(LogArena, Log, All);

void AArenaGameMode::BeginPlay()
{
	Super::BeginPlay();

	Hud = NewObject<UArenaHud>(this);
	ScoreTracker = NewObject<UArenaScoreTracker>(this);
	Stats = new FArenaStats();

	Palette = LoadObject<UArenaPalette>(nullptr, TEXT("/Game/Data/Palettes/DA_Primary.DA_Primary"));
	if (!Palette)
	{
		UE_LOG(LogArena, Warning, TEXT("Palette is null, using fallback gray"));
	}
	Hud->ApplyPalette(Palette);
}

void AArenaGameMode::EndPlay(const EEndPlayReason::Type Reason)
{
	delete Stats;
	Stats = nullptr;
	Super::EndPlay(Reason);
}

void AArenaGameMode::OnGoalScored(int32 TeamIndex)
{
	Stats->Goals++;
	ScoreTracker->AddPoints(TeamIndex, 1);
	Hud->ShowScore(TeamIndex, ScoreTracker->GetPoints(TeamIndex));
}
""",
    GAME_INI: """[/Script/EngineSettings.GeneralProjectSettings]
ProjectName=Pixel Arena
ProjectVersion=0.9.2

[/Script/UnrealEd.ProjectPackagingSettings]
Build=IfProjectHasCode
BuildConfiguration=PPBC_Shipping
UsePakFile=True
bCookAll=False
+MapsToCook=(FilePath="/Game/Maps/Arena")
+DirectoriesToAlwaysCook=(Path="/Game/Data/Effects")
+DirectoriesToNeverCook=(Path="/Game/Dev")
""",
    "Saved/Logs/PixelArena-shipping.log": f"""[2026.10.28-21.04.11:102][  0]LogInit: Build: Shipping, Version: 0.9.2
[2026.10.28-21.04.11:380][  0]LogAudio: Warning: Audio device has no surround layout, falling back to stereo
[2026.10.28-21.04.12:015][  0]LogLoad: Game class is 'ArenaGameMode'
[2026.10.28-21.04.12:244][  0]LogStreaming: Error: Couldn't find file for package {ASSET} requested by async loading code. NameToLoad: {ASSET}
[2026.10.28-21.04.12:245][  0]LogUObjectGlobals: Warning: Failed to find object 'ArenaPalette {ASSET}.DA_Primary'
[2026.10.28-21.04.12:246][  0]LogArena: Warning: Palette is null, using fallback gray
[2026.10.28-21.04.31:610][1120]LogNet: Warning: Ping spike of 212 ms on the local client
[2026.10.28-21.05.13:071][3684]LogGarbage: Collecting garbage: 412 objects purged
[2026.10.28-21.05.27:903][4570]LogArena: Display: Goal for team 1
[2026.10.28-21.05.27:904][4570]LogWindows: Error: === Critical error: ===
[2026.10.28-21.05.27:904][4570]LogWindows: Error: Fatal error!
[2026.10.28-21.05.27:904][4570]LogWindows: Error: Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0xffffffffffffffff
[2026.10.28-21.05.27:904][4570]LogWindows: Error: PixelArena-Win64-Shipping.exe!UArenaScoreTracker::AddPoints() [Source/PixelArena/ArenaScoreTracker.cpp:18]
[2026.10.28-21.05.27:904][4570]LogWindows: Error: PixelArena-Win64-Shipping.exe!AArenaGameMode::OnGoalScored() [Source/PixelArena/ArenaGameMode.cpp:38]
""",
}

TRACKER_TYPE = r"(?:class\s+)?UArenaScoreTracker"
# Only what keeps the object alive: a reflected member, a strong pointer, the root set or a reported reference.
KEPT_ALIVE = (
    rf"UPROPERTY\s*\([^)]*\)\s*(?:TObjectPtr\s*<\s*{TRACKER_TYPE}\s*>|{TRACKER_TYPE}\s*\*)\s*ScoreTracker\b",
    rf"TStrongObjectPtr\s*<\s*{TRACKER_TYPE}\s*>\s*ScoreTracker\b",
    r"ScoreTracker\s*->\s*AddToRoot\s*\(",
    r"AddReferencedObject\s*\(\s*\w*\s*->\s*ScoreTracker|AddReferencedObject\s*\(\s*ScoreTracker",
)
# UHT stops the build on a reflected pointer to a type it does not know.
STRUCT_REFLECTED = r"UPROPERTY\s*\([^)]*\)\s*(?:TObjectPtr\s*<\s*)?(?:struct\s+)?FArenaStats\b"
PACKAGING_SECTION = "/script/unrealed.projectpackagingsettings"
COOKED_PATHS = frozenset({"/game/data/palettes", "data/palettes", "/game/data", "data", "/game"})


def _code(text: str | None) -> str:
    """Source without comments or #if 0 blocks: a fix left in a comment or a disabled block fixes nothing."""
    return _enabled_lines(re.sub(r"//[^\n]*|/\*.*?\*/", "", text or "", flags=re.DOTALL))


def _enabled_lines(code: str) -> str:
    """Drop the lines an `#if 0` (or `#if false`) disables, up to its #else, #elif or #endif (#164)."""
    kept: list[str] = []
    depth = 0  # > 0 inside a disabled block, counting the #if nested in it
    for line in code.splitlines():
        directive = re.match(r"\s*#\s*(\w+)\s*(\S*)", line)
        word, arg = (directive.group(1), directive.group(2).lower()) if directive else ("", "")
        if depth == 0:
            if word == "if" and arg in {"0", "false"}:
                depth = 1
                continue
            kept.append(line)
            continue
        if word in {"if", "ifdef", "ifndef"}:
            depth += 1
        elif word == "endif" or (depth == 1 and word in {"else", "elif"}):
            depth -= 1
    return "\n".join(kept)


def _ini_sections(text: str | None) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            current = stripped[1:-1].strip().lower()
        elif stripped and not stripped.startswith(";"):
            sections.setdefault(current, []).append(stripped)
    return sections


def _cooks_all_content(packaging: Sequence[str]) -> bool:
    """bCookAll=True cooks every asset, the palette too, unless a never-cook entry drops its folder (#164)."""
    values = [found.group(1).lower() for line in packaging
              if (found := re.match(r"bCookAll\s*=\s*(\w+)", line, re.IGNORECASE))]
    if not values or values[-1] != "true":
        return False
    for line in packaging:
        found = re.match(r'[+]?DirectoriesToNeverCook\s*=\s*\(\s*Path\s*=\s*"?([^")]+)"?\s*\)', line, re.IGNORECASE)
        if found and found.group(1).strip().rstrip("/").lower() in COOKED_PATHS:
            return False
    return True


def _palette_reaches_the_cook(ws: Path) -> bool:
    sections = _ini_sections(read(ws, GAME_INI))
    if _cooks_all_content(sections.get(PACKAGING_SECTION, [])):
        return True
    for line in sections.get(PACKAGING_SECTION, []):
        found = re.match(r'[+]?DirectoriesToAlwaysCook\s*=\s*\(\s*Path\s*=\s*"?([^")]+)"?\s*\)', line, re.IGNORECASE)
        if found and found.group(1).strip().rstrip("/").lower() in COOKED_PATHS:
            return True
    # Other routes that also cook it: the asset manager, or a hard reference from the class.
    scan = any("primaryassettypestoscan" in line.lower() and "palettes" in line.lower()
               for lines in sections.values() for line in lines)
    hard = re.search(r"ConstructorHelpers\s*::\s*FObjectFinder[^;]*DA_Primary", _code(read(ws, HEADER)) + _code(read(ws, SOURCE)))
    return scan or hard is not None


def _ue_setup(ws: Path) -> None:
    for rel, text in UE_FILES.items():
        write(ws, rel, text)


def _ue_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    code = _code(read(ws, HEADER)) + "\n" + _code(read(ws, SOURCE))
    result.add("crash fixed: the score tracker survives garbage collection", any(re.search(way, code) for way in KEPT_ALIVE),
               "ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference")
    result.add("colors fixed: the palette reaches the cook", _palette_reaches_the_cook(ws),
               f"{ASSET} is not cooked by the packaging settings (always-cook folder or bCookAll), the asset manager or a hard reference")
    result.add("the plain C++ pointer stays out of reflection", re.search(STRUCT_REFLECTED, code) is None,
               "UPROPERTY on FArenaStats stops the build: it is not a reflected type")
    got = result_json(ws)
    crash, colors = str(got.get("crash_cause", "")), str(got.get("no_colors_cause", ""))
    result.add("the report names the crash cause", re.search(r"scoretracker|score tracker|garbage|\bgc\b|uproperty", crash, re.IGNORECASE) is not None,
               f"crash_cause: {crash!r}")
    result.add("the report names the color cause", re.search(r"cook|palettes|da_primary|packag", colors, re.IGNORECASE) is not None,
               f"no_colors_cause: {colors!r}")
    return result


def _ue_reference(ws: Path) -> list[str]:
    write(ws, HEADER, UE_FILES[HEADER].replace("	UArenaScoreTracker* ScoreTracker", "	UPROPERTY()\n	TObjectPtr<UArenaScoreTracker> ScoreTracker"))
    write(ws, GAME_INI, UE_FILES[GAME_INI].replace('+DirectoriesToNeverCook', '+DirectoriesToAlwaysCook=(Path="/Game/Data/Palettes")\n+DirectoriesToNeverCook'))
    write(ws, "result.json", '{"crash_cause": "ScoreTracker has no UPROPERTY, so garbage collection frees it", '
                             '"no_colors_cause": "DA_Primary is loaded by path only, so it is never cooked"}')
    return ["fixed the header and the packaging settings"]


TASKS = [
    EvalTask(
        id="ue-packaged-bug", category="gamedev",
        provenance="Real Unreal work: garbage collection and the cook list, two bugs an editor session hides; synthetic project",
        summary="Find out why an Unreal game loses its colors and crashes only in the packaged build, and fix it.",
        setup=_ue_setup, check=_ue_check, reference=_ue_reference, timeout_s=90,
        checkpoints=checkpoints(("read the crash log", r"shipping\.log"), ("read the game mode", r"ArenaGameMode"), WROTE_RESULT),
        steps=(Step("Pixel Arena, our Unreal game in {WS}, runs fine in the editor. In the packaged build, players say the arena "
                    "has no colors, and the game crashes after a minute or so of play. The log of one packaged run is in "
                    "{WS}/Saved/Logs. There is no engine on this machine, so you cannot build or run it. Find out why and fix the "
                    "sources and the config. Record the causes in {WS}/result.json: crash_cause, no_colors_cause."),),
    ),
]
