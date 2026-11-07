param([Parameter(Mandatory=$true)][string]$EngineRoot)
$ErrorActionPreference = 'Stop'
[Diagnostics.Process]::GetCurrentProcess().PriorityClass = 'BelowNormal'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectFile = Join-Path $projectRoot 'AlvoMovel.uproject'
$editor = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
foreach ($required in @($projectFile, $editor)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Required path does not exist: $required" }
}
$reportDir = Join-Path (Join-Path $projectRoot 'tmp') ('test-report-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
$reserved = [Math]::Max(0, [Environment]::ProcessorCount - 4)
$shaderLimit = "-ini:Engine:[DevOptions.Shaders]:NumUnusedShaderCompilingThreads=$reserved"
& $editor $projectFile $shaderLimit '-ExecCmds=Automation RunTests AlvoMovel.Gameplay.HitMissAndMovement' '-TestExit=Automation Test Queue Empty' -unattended -nop4 -nullrhi -nosound -nosplash "-ReportExportPath=$reportDir" -log
if ($LASTEXITCODE -ne 0) { throw "Unreal exited with code $LASTEXITCODE" }
$reportPath = Join-Path $reportDir 'index.json'
if (-not (Test-Path -LiteralPath $reportPath)) { throw "Unreal test report missing: $reportPath" }
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json
$testResults = @($report.tests | Where-Object fullTestPath -eq 'AlvoMovel.Gameplay.HitMissAndMovement')
if ($testResults.Count -ne 1 -or $testResults[0].state -ne 'Success' -or $report.failed -ne 0) {
    throw "Gameplay test failed or did not run: count=$($testResults.Count), failed=$($report.failed), report=$reportPath"
}
Write-Output "GAMEPLAY_TEST_PASS report=$reportPath"
