[CmdletBinding()]
param(
    [string]$DocsDirectory = (Join-Path $PSScriptRoot ([string]([char]0x9898) + [char]0x76EE))
)

$ErrorActionPreference = 'Stop'
$python = Get-Command python3 -ErrorAction SilentlyContinue
if ($null -eq $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if ($null -eq $python) {
    throw 'Python 3 must be available on PATH.'
}

Write-Host 'Compatibility wrapper: running schema v3 library validation.'
& $python.Source (Join-Path $PSScriptRoot 'tools/validate_library.py')
exit $LASTEXITCODE
