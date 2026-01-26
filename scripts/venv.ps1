param ($path)

if ($path) {Set-Location $path}

$env:PYTHONPATH="$PWD"

& .\.venv\Scripts\Activate.ps1
