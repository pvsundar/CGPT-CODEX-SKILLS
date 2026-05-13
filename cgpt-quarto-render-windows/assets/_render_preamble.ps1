$ErrorActionPreference = "Stop"

$env:PATHEXT = ".COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC;.PS1"

$systemRoot = if ($env:SystemRoot) { $env:SystemRoot } else { "C:\Windows" }
$pathParts = @(
    "$systemRoot\System32",
    "$systemRoot",
    "$systemRoot\System32\Wbem",
    "$systemRoot\System32\WindowsPowerShell\v1.0",
    "C:\Program Files\Quarto\bin"
)

$rRoot = "C:\Users\sundar\AppData\Local\Programs\R"
if (Test-Path -LiteralPath $rRoot) {
    $rDir = Get-ChildItem -LiteralPath $rRoot -Directory |
        Where-Object { $_.Name -match '^R-\d+\.\d+\.\d+$' } |
        Sort-Object { [Version]($_.Name -replace '^R-', '') } -Descending |
        Select-Object -First 1
    if ($rDir) {
        $pathParts += (Join-Path $rDir.FullName 'bin\x64')
    }
}

$pathParts += $env:PATH
$env:PATH = ($pathParts | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -Unique) -join ";"

[Environment]::CurrentDirectory = $PWD.Path

$quartoExe = "C:\Program Files\Quarto\bin\quarto.exe"
if (-not (Test-Path -LiteralPath $quartoExe)) {
    throw "Quarto not found at $quartoExe. Install Quarto or update _render_preamble.ps1."
}

Set-Alias quarto $quartoExe -Scope Global
Write-Host "[preamble] Quarto: $quartoExe"
Write-Host "[preamble] PWD:    $PWD"
