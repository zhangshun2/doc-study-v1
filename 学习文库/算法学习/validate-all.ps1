[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$python = Get-Command python3 -ErrorAction SilentlyContinue
if ($null -eq $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if ($null -eq $python) {
    throw 'Python 3 must be available on PATH.'
}

& $python.Source (Join-Path $PSScriptRoot 'tools/validate_all.py')
exit $LASTEXITCODE
