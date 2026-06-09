# ============================================================
# AutoChromaKey.ps1 - AI 立绘自动去白底 + 缩放工具
# Flood Fill 版：只删除与角落背景连通的区域
# ============================================================

param(
    [string]$InputPath = "",
    [string]$OutputPath = "",
    [int]$TargetHeight = 0,
    [int]$Tolerance = 35,
    [switch]$Batch,
    [string]$OutputDir = "",
    [switch]$SkipChromaKey
)

Add-Type -AssemblyName System.Drawing

function Remove-Background($srcPath, $dstPath, $tol, $targetH, [bool]$skipKey = $false) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    
    $src = [System.Drawing.Image]::FromFile($srcPath)
    $w = [int]$src.Width
    $h = [int]$src.Height
    Write-Host "  Load: ${w}x${h}"

    $bmp = New-Object System.Drawing.Bitmap($w, $h, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.DrawImage($src, 0, 0, $w, $h)
    $g.Dispose()
    $src.Dispose()

    if (-not $skipKey) {
        # Background color from corners
        $c1 = $bmp.GetPixel(0, 0)
        $c2 = $bmp.GetPixel($w - 1, 0)
        $c3 = $bmp.GetPixel(0, $h - 1)
        $c4 = $bmp.GetPixel($w - 1, $h - 1)
        $bgR = [int](($c1.R + $c2.R + $c3.R + $c4.R) / 4)
        $bgG = [int](($c1.G + $c2.G + $c3.G + $c4.G) / 4)
        $bgB = [int](($c1.B + $c2.B + $c3.B + $c4.B) / 4)
        Write-Host "  BG ref: R=$bgR G=$bgG B=$bgB"

        # LockBits
        $rect = New-Object System.Drawing.Rectangle(0, 0, $w, $h)
        $bmpData = $bmp.LockBits($rect, [System.Drawing.Imaging.ImageLockMode]::ReadWrite, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $stride = $bmpData.Stride
        $totalBytes = $stride * $h
        $bytes = New-Object byte[] $totalBytes
        [System.Runtime.InteropServices.Marshal]::Copy($bmpData.Scan0, $bytes, 0, $totalBytes)

        $pixelCount = $w * $h
        $visited = New-Object bool[] $pixelCount
        $queue = New-Object System.Collections.Generic.Queue[int]

        # Seed four corners (encode as y*w + x)
        $seeds = @(0, ($w - 1), (($h - 1) * $w), ((($h - 1) * $w) + $w - 1))
        foreach ($s in $seeds) {
            if ($s -ge 0 -and $s -lt $pixelCount -and -not $visited[$s]) {
                $queue.Enqueue($s)
                $visited[$s] = $true
            }
        }

        $dx = @(0, 0, -1, 1)
        $dy = @(-1, 1, 0, 0)
        $transparentCount = 0
        $tolSq = $tol * $tol

        while ($queue.Count -gt 0) {
            $code = $queue.Dequeue()
            $px = $code % $w
            $py = [int][Math]::Floor($code / $w)
            $byteIdx = $py * $stride + $px * 4
            $bVal = $bytes[$byteIdx]
            $gVal = $bytes[$byteIdx + 1]
            $rVal = $bytes[$byteIdx + 2]

            $dr = $rVal - $bgR
            $dg = $gVal - $bgG
            $db = $bVal - $bgB
            $distSq = $dr * $dr + $dg * $dg + $db * $db

            if ($distSq -le $tolSq) {
                $bytes[$byteIdx + 3] = 0
                $transparentCount++

                for ($i = 0; $i -lt 4; $i++) {
                    $nx = $px + $dx[$i]
                    $ny = $py + $dy[$i]
                    if ($nx -ge 0 -and $nx -lt $w -and $ny -ge 0 -and $ny -lt $h) {
                        $nCode = $ny * $w + $nx
                        if (-not $visited[$nCode]) {
                            $visited[$nCode] = $true
                            $queue.Enqueue($nCode)
                        }
                    }
                }
            }
        }

        [System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $bmpData.Scan0, $totalBytes)
        $bmp.UnlockBits($bmpData)

        Write-Host "  Transparent pixels: $transparentCount"
    } else {
        Write-Host "  Skipping chroma key (white background preserved)"
    }

    # Resize
    $finalBmp = $bmp
    if ($targetH -gt 0 -and $h -ne $targetH) {
        $ratio = $targetH / $h
        $targetW = [int]($w * $ratio)
        $finalBmp = New-Object System.Drawing.Bitmap($targetW, $targetH, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $g2 = [System.Drawing.Graphics]::FromImage($finalBmp)
        $g2.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g2.DrawImage($bmp, 0, 0, $targetW, $targetH)
        $g2.Dispose()
        $bmp.Dispose()
        Write-Host "  Resized to: ${targetW}x${targetH}"
    }

    $finalBmp.Save($dstPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $finalBmp.Dispose()

    $sw.Stop()
    Write-Host "  Done -> $dstPath ($($sw.ElapsedMilliseconds)ms)"
    Write-Host ""
}

# ============================================================
# Main
# ============================================================

if ($Batch) {
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
    }
    $files = Get-ChildItem -Path $InputPath -Filter "*.png"
    Write-Host "========================================"
    Write-Host "Batch: $($files.Count) images"
    Write-Host "Tolerance: $Tolerance"
    if ($TargetHeight -gt 0) { Write-Host "Target height: $TargetHeight" } else { Write-Host "Target height: original" }
    Write-Host "========================================"
    Write-Host ""
    foreach ($f in $files) {
        $out = Join-Path $OutputDir $f.Name
        Remove-Background $f.FullName $out $Tolerance $TargetHeight $SkipChromaKey
    }
    Write-Host "All done! Output: $OutputDir"
}
else {
    if (-not $InputPath) {
        Write-Host "Single file:"
        Write-Host "  .\AutoChromaKey.ps1 -InputPath 'img.png' -OutputPath 'out.png' -TargetHeight 600"
        Write-Host "  .\AutoChromaKey.ps1 -InputPath 'img.png' -OutputPath 'out.png' -TargetHeight 600 -SkipChromaKey"
        Write-Host ""
        Write-Host "Batch:"
        Write-Host "  .\AutoChromaKey.ps1 -Batch -InputPath 'C:\myart\' -OutputDir 'C:\out\' -TargetHeight 600"
        Write-Host "  .\AutoChromaKey.ps1 -Batch -InputPath 'C:\myart\' -OutputDir 'C:\out\' -TargetHeight 600 -SkipChromaKey"
        exit
    }
    if (-not $OutputPath) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
        $ext = [System.IO.Path]::GetExtension($InputPath)
        $dir = [System.IO.Path]::GetDirectoryName($InputPath)
        $outName = $base + "_transparent" + $ext
        $OutputPath = [System.IO.Path]::Combine($dir, $outName)
    }
    Remove-Background $InputPath $OutputPath $Tolerance $TargetHeight $SkipChromaKey
}
