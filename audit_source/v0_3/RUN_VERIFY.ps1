$ErrorActionPreference = "Stop"
$taskScript = Join-Path $PSScriptRoot "verify_obstructions.py"
python $taskScript
if ($LASTEXITCODE -ne 0) { throw "Verification failed." }
$revisionScript = Join-Path $PSScriptRoot "verify_revision.py"
python $revisionScript
if ($LASTEXITCODE -ne 0) { throw "Revision verification failed." }
