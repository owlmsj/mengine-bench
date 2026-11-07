param(
    [Parameter(Mandatory=$true)][string]$EngineRoot,
    [string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
[Diagnostics.Process]::GetCurrentProcess().PriorityClass = 'BelowNormal'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectFile = Join-Path $projectRoot 'AlvoMovel.uproject'
$uat = Join-Path $EngineRoot 'Engine\Build\BatchFiles\RunUAT.bat'
$appLocal = Join-Path $EngineRoot 'Engine\Binaries\ThirdParty\AppLocalDependencies'
$playtest = Join-Path $PSScriptRoot 'AlvoMovelPlaytest.exe'
foreach ($required in @($projectFile, $uat, $appLocal, $playtest)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Required path does not exist: $required" }
}
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path (Join-Path $projectRoot 'Packaged') ('build-' + [guid]::NewGuid().ToString('N'))
}
if (Test-Path -LiteralPath $OutputDirectory) { throw "Output directory already exists: $OutputDirectory" }
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$reserved = [Math]::Max(0, [Environment]::ProcessorCount - 4)
$cookOptions = "-AdditionalCookerOptions=-ini:Engine:[DevOptions.Shaders]:NumUnusedShaderCompilingThreads=$reserved"
& $uat BuildCookRun "-project=$projectFile" -noP4 -platform=Win64 -clientconfig=Shipping -build -cook -stage -pak -iostore -compressed "-applocaldirectory=$appLocal" -archive "-archivedirectory=$OutputDirectory" -utf8output $cookOptions -ubtargs=-MaxParallelActions=4
if ($LASTEXITCODE -ne 0) { throw "Unreal packaging failed with exit code $LASTEXITCODE" }
$stage = Join-Path $OutputDirectory 'Windows'
if (-not (Test-Path -LiteralPath (Join-Path $stage 'AlvoMovel.exe'))) { throw "Packaged game is missing in $stage" }
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipPath = Join-Path $OutputDirectory 'AlvoMovel.zip'
$archive = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    $files = @(Get-ChildItem -LiteralPath $stage -Recurse -File | Where-Object { $_.Extension -ne '.pdb' -and $_.Name -notlike 'Manifest_*_Win64.txt' })
    foreach ($file in $files) {
        $entry = [IO.Path]::GetRelativePath($stage, $file.FullName).Replace('\', '/')
        [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $file.FullName, $entry, [IO.Compression.CompressionLevel]::Optimal)
    }
    [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, (Join-Path $projectRoot 'LEIA-ME.txt'), 'LEIA-ME.txt', [IO.Compression.CompressionLevel]::Optimal)
    [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $playtest, 'AlvoMovelPlaytest.exe', [IO.Compression.CompressionLevel]::Optimal)
} finally { $archive.Dispose() }
$bytes = (Get-Item -LiteralPath $zipPath).Length
if ($bytes -gt 300000000) { throw "ZIP exceeds 300 MB: $bytes bytes ($zipPath)" }
Write-Output "ZIP=$zipPath"
Write-Output "ZIP_BYTES=$bytes"
Write-Output "SHA256=$((Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash)"
