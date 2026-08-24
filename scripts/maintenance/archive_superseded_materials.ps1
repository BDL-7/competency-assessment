$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$repoName = Split-Path -Leaf $RepoRoot
$requiredMarker = Join-Path $RepoRoot "README.md"

if ($repoName -ne "competency-assessment" -or -not (Test-Path -LiteralPath $requiredMarker)) {
    throw "Refusing to archive files in an unexpected directory: $RepoRoot"
}

function Resolve-RepoPath {
    param([Parameter(Mandatory = $true)][string]$RelativePath)

    $fullPath = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $RelativePath))
    $prefix = $RepoRoot.TrimEnd('\') + '\'
    if (-not $fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside the repository: $fullPath"
    }
    return $fullPath
}

function Move-RepoPath {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    $sourcePath = Resolve-RepoPath $Source
    $destinationPath = Resolve-RepoPath $Destination

    if (-not (Test-Path -LiteralPath $sourcePath)) {
        if (Test-Path -LiteralPath $destinationPath) {
            Write-Host "Already archived: $Destination"
            return
        }
        throw "Expected archive source does not exist: $sourcePath"
    }
    if (Test-Path -LiteralPath $destinationPath) {
        throw "Archive destination already exists: $destinationPath"
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destinationPath) | Out-Null
    Move-Item -LiteralPath $sourcePath -Destination $destinationPath
    Write-Host "Archived: $Source -> $Destination"
}

function Clear-ReadOnlyRecursively {
    param([Parameter(Mandatory = $true)][string]$Path)

    Get-ChildItem -LiteralPath $Path -Recurse -Force | ForEach-Object {
        $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
    }
    $item = Get-Item -LiteralPath $Path -Force
    $item.Attributes = $item.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
}

$packageRelative = "artifacts\sharing\share-package-20260814-110155"
$verificationRelative = "artifacts\sharing\share-verification-20260814-110210"
$packagePath = Resolve-RepoPath $packageRelative
$verificationPath = Resolve-RepoPath $verificationRelative
$releaseArchiveRelative = "artifacts\archive\2026-08-14-html-release"
$releaseArchivePath = Resolve-RepoPath $releaseArchiveRelative
$expectedReleaseFiles = @(
    "competency-assessment-system-audience.html",
    "competency-assessment-system-presenter.html",
    "HOW_TO_OPEN.txt"
)

if (-not (Test-Path -LiteralPath $releaseArchivePath)) {
    foreach ($directory in @($packagePath, $verificationPath)) {
        if (-not (Test-Path -LiteralPath $directory)) {
            throw "Expected release directory does not exist: $directory"
        }
        $actualFiles = @(
            Get-ChildItem -LiteralPath $directory -File -Force |
                Select-Object -ExpandProperty Name |
                Sort-Object
        )
        $expectedFiles = @($expectedReleaseFiles | Sort-Object)
        if (Compare-Object -ReferenceObject $expectedFiles -DifferenceObject $actualFiles) {
            throw "Release directory contains unexpected or missing files: $directory"
        }
        if (@(Get-ChildItem -LiteralPath $directory -Directory -Force).Count -ne 0) {
            throw "Release directory contains unexpected subdirectories: $directory"
        }
    }

    foreach ($fileName in $expectedReleaseFiles) {
        $packageHash = (Get-FileHash -LiteralPath (Join-Path $packagePath $fileName) -Algorithm SHA256).Hash
        $verificationHash = (Get-FileHash -LiteralPath (Join-Path $verificationPath $fileName) -Algorithm SHA256).Hash
        if ($packageHash -ne $verificationHash) {
            throw "Release copies differ; refusing to remove either copy: $fileName"
        }
        Write-Host "Verified duplicate SHA256: $fileName $packageHash"
    }
}

Move-RepoPath `
    "artifacts\renders\leadership-brief" `
    "artifacts\archive\2026-08-13-leadership-concept\brief"
Move-RepoPath `
    "artifacts\renders\leadership-deck" `
    "artifacts\archive\2026-08-13-leadership-concept\deck\renders"

$dependencyPath = Resolve-RepoPath "presentations\leadership-deck\node_modules"
if (Test-Path -LiteralPath $dependencyPath) {
    Clear-ReadOnlyRecursively $dependencyPath
    Remove-Item -LiteralPath $dependencyPath -Recurse
    Write-Host "Removed reproducible dependency directory: presentations\leadership-deck\node_modules"
}

Move-RepoPath `
    "presentations\leadership-deck" `
    "artifacts\archive\2026-08-13-leadership-concept\deck\source"

if (-not (Test-Path -LiteralPath $releaseArchivePath)) {
    New-Item -ItemType Directory -Force -Path $releaseArchivePath | Out-Null
    Move-Item -LiteralPath (Join-Path $packagePath "competency-assessment-system-audience.html") -Destination (Join-Path $releaseArchivePath "audience.html")
    Move-Item -LiteralPath (Join-Path $packagePath "competency-assessment-system-presenter.html") -Destination (Join-Path $releaseArchivePath "presenter.html")
    Move-Item -LiteralPath (Join-Path $packagePath "HOW_TO_OPEN.txt") -Destination (Join-Path $releaseArchivePath "HOW_TO_OPEN.txt")
    Write-Host "Archived retained HTML release: $releaseArchiveRelative"

    Clear-ReadOnlyRecursively $packagePath
    Remove-Item -LiteralPath $packagePath

    Clear-ReadOnlyRecursively $verificationPath
    Remove-Item -LiteralPath $verificationPath -Recurse
    Write-Host "Removed verified duplicate release: $verificationRelative"
}

$sharingPath = Resolve-RepoPath "artifacts\sharing"
if (Test-Path -LiteralPath $sharingPath) {
    if (@(Get-ChildItem -LiteralPath $sharingPath -Force).Count -eq 0) {
        Clear-ReadOnlyRecursively $sharingPath
        Remove-Item -LiteralPath $sharingPath
        Write-Host "Removed empty directory: artifacts\sharing"
    }
}

Write-Host "Superseded-material archive complete."
