$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$repoName = Split-Path -Leaf $RepoRoot
$requiredMarker = Join-Path $RepoRoot "README.md"
if ($repoName -ne "competency-assessment" -or -not (Test-Path -LiteralPath $requiredMarker)) {
    throw "Refusing to reorganize a directory that does not look like the competency-assessment repository: $RepoRoot"
}

function Assert-InRepo {
    param([Parameter(Mandatory = $true)][string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $prefix = $RepoRoot.TrimEnd('\') + '\'
    if (-not $fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside the repository: $fullPath"
    }
    return $fullPath
}

function Move-RepoItem {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination,
        [string]$FinalDestination
    )

    $sourcePath = Assert-InRepo (Join-Path $RepoRoot $Source)
    $destinationPath = Assert-InRepo (Join-Path $RepoRoot $Destination)

    if (-not (Test-Path -LiteralPath $sourcePath)) {
        if (Test-Path -LiteralPath $destinationPath) {
            Write-Host "Already moved: $Destination"
            return
        }
        if ($FinalDestination) {
            $finalDestinationPath = Assert-InRepo (Join-Path $RepoRoot $FinalDestination)
            if (Test-Path -LiteralPath $finalDestinationPath) {
                Write-Host "Already archived or cleaned: $FinalDestination"
                return
            }
        }
        throw "Expected source does not exist: $sourcePath"
    }
    if (Test-Path -LiteralPath $destinationPath) {
        throw "Destination already exists: $destinationPath"
    }

    $destinationParent = Split-Path -Parent $destinationPath
    New-Item -ItemType Directory -Force -Path $destinationParent | Out-Null
    Move-Item -LiteralPath $sourcePath -Destination $destinationPath
    Write-Host "Moved: $Source -> $Destination"
}

Move-RepoItem "Business_Value_Need.docx" "docs\project\Business_Value_Need.docx"
Move-RepoItem "Tracker\Competency_Assessment_Tracker_Project_Plan.docx" "docs\project\Competency_Assessment_Tracker_Project_Plan.docx"
Move-RepoItem "Tracker\App Architecture & Implementation Guide.pdf" "docs\project\App Architecture & Implementation Guide.pdf"
Move-RepoItem "Tracker\QMML and NCIRD Guidelines.docx" "docs\controlled-sources\QMML and NCIRD Guidelines.docx"
Move-RepoItem "Tracker\Non-CLIA Annual Competency Assessment Form_Approved.pdf" "docs\controlled-sources\Non-CLIA Annual Competency Assessment Form_Approved.pdf"

Move-RepoItem "Tracker\Approved Test Systems.xlsx" "data\authoritative\Approved Test Systems.xlsx"
Move-RepoItem "Tracker\Tracking System_MIST.xlsx" "data\migration\Tracking System_MIST.xlsx"
Move-RepoItem "Tracker\Tracking System_HIR.xlsx" "data\migration\Tracking System_HIR.xlsx"
Move-RepoItem "Tracker\CA Relational Tables.xlsx" "data\reference\CA Relational Tables.xlsx"

Move-RepoItem "build_consolidated_documents.py" "scripts\documents\build_consolidated_documents.py"
Move-RepoItem "Tracker\build_leadership_concept_brief.py" "scripts\documents\build_leadership_concept_brief.py"
Move-RepoItem "tmp\build_business_value_need.py" "scripts\documents\build_business_value_need.py"

Move-RepoItem "competency-assessment-html-workshop" "presentations\html-workshop"
Move-RepoItem "tmp\leadership_deck\build_deck.mjs" "presentations\leadership-deck\build_deck.mjs" "artifacts\archive\2026-08-13-leadership-concept\deck\source\build_deck.mjs"
Move-RepoItem "tmp\leadership_deck\package.json" "presentations\leadership-deck\package.json" "artifacts\archive\2026-08-13-leadership-concept\deck\source\package.json"
Move-RepoItem "tmp\leadership_deck\source-notes.txt" "presentations\leadership-deck\source-notes.txt" "artifacts\archive\2026-08-13-leadership-concept\deck\source\source-notes.txt"
Move-RepoItem "tmp\leadership_deck\node_modules" "presentations\leadership-deck\node_modules" "artifacts\archive\2026-08-13-leadership-concept\deck\source"

Move-RepoItem "tmp\business_value_need_render" "artifacts\renders\business-value"
Move-RepoItem "tmp\consolidation" "artifacts\renders\consolidation"
Move-RepoItem "tmp\leadership_brief_render_v1" "artifacts\renders\leadership-brief\v1" "artifacts\archive\2026-08-13-leadership-concept\brief\v1"
Move-RepoItem "tmp\leadership_brief_render_v2" "artifacts\renders\leadership-brief\v2" "artifacts\archive\2026-08-13-leadership-concept\brief\v2"
Move-RepoItem "tmp\leadership_brief_render_v3" "artifacts\renders\leadership-brief\v3" "artifacts\archive\2026-08-13-leadership-concept\brief\v3"
Move-RepoItem "tmp\leadership_brief_render_final" "artifacts\renders\leadership-brief\final" "artifacts\archive\2026-08-13-leadership-concept\brief\final"
Move-RepoItem "tmp\leadership_deck\qa" "artifacts\renders\leadership-deck\qa" "artifacts\archive\2026-08-13-leadership-concept\deck\renders\qa"
Move-RepoItem "tmp\leadership_deck\final_pptx_render" "artifacts\renders\leadership-deck\final-pptx" "artifacts\archive\2026-08-13-leadership-concept\deck\renders\final-pptx"
Move-RepoItem "tmp\share_package_20260814_110155" "artifacts\sharing\share-package-20260814-110155" "artifacts\archive\2026-08-14-html-release"
Move-RepoItem "tmp\share_verify_20260814_110210" "artifacts\sharing\share-verification-20260814-110210" "artifacts\archive\2026-08-14-html-release"

foreach ($relativePath in @("tmp\pdfs", "Tracker", "tmp\leadership_deck", "tmp")) {
    $path = Assert-InRepo (Join-Path $RepoRoot $relativePath)
    if (Test-Path -LiteralPath $path) {
        $children = @(Get-ChildItem -LiteralPath $path -Force)
        if ($children.Count -eq 0) {
            $item = Get-Item -LiteralPath $path -Force
            $item.Attributes = $item.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
            Remove-Item -LiteralPath $path
            Write-Host "Removed empty directory: $relativePath"
        } else {
            throw "Directory is not empty after reorganization: $path"
        }
    }
}

$pythonCache = Assert-InRepo (Join-Path $RepoRoot "__pycache__")
if (Test-Path -LiteralPath $pythonCache) {
    $unexpectedCacheItems = @(
        Get-ChildItem -LiteralPath $pythonCache -Recurse -Force |
            Where-Object { -not $_.PSIsContainer -and $_.Extension -ne ".pyc" }
    )
    if ($unexpectedCacheItems.Count -gt 0) {
        throw "Refusing to remove __pycache__; it contains non-generated files."
    }
    Get-ChildItem -LiteralPath $pythonCache -Recurse -Force | ForEach-Object {
        $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
    }
    $cacheDirectory = Get-Item -LiteralPath $pythonCache -Force
    $cacheDirectory.Attributes = $cacheDirectory.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
    Remove-Item -LiteralPath $pythonCache -Recurse
    Write-Host "Removed generated Python cache: __pycache__"
}

Write-Host "Repository reorganization complete."
