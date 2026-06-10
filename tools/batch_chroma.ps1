param([string]$InputDir = "")
if (-not $InputDir) { Write-Host "Usage: .\batch_chroma.ps1 -InputDir 'C:\path'"; exit }

$files = Get-ChildItem -Path $InputDir -File | Where-Object { $_.Extension -in @('.png','.jpg','.jpeg') }
Write-Host "Processing $($files.Count) files in $InputDir"

foreach ($f in $files) {
    $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
    $out = Join-Path $InputDir ($base + ".png")
    Write-Host "  -> $out"
    powershell -File AutoChromaKey.ps1 -InputPath $f.FullName -OutputPath $out -TargetHeight 0
    # Remove original jpg if converted
    if ($f.Extension -in @('.jpg','.jpeg') -and $out -ne $f.FullName) {
        Remove-Item $f.FullName -Force
        Write-Host "     (removed $($f.Name))"
    }
}
Write-Host "Done!"
