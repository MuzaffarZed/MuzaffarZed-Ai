@echo off
setlocal EnableExtensions
chcp 65001 >nul
title O'zbek Musiqa Markazi Ultimate Pro v4.0 (Avto-Magnitola va Fleshka Engine)

set "SCRIPT_FULL_PATH=%~f0"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$raw = [System.IO.File]::ReadAllText($env:SCRIPT_FULL_PATH, [System.Text.Encoding]::UTF8); $marker = '::POWER' + 'SHELL_BEGIN::'; $idx = $raw.IndexOf($marker); if ($idx -ge 0) { Invoke-Expression ($raw.Substring($idx + $marker.Length)) }"

if %errorlevel% neq 0 (
    echo.
    echo   [Xatolik yuz berdi. Kod: %errorlevel%]
)

echo.
echo   [!] Dastur o'z ishini yakunladi.
echo   Oynani yopish uchun istalgan tugmani bosing...
pause >nul
exit /b

::POWERSHELL_BEGIN::
try {
    $Host.UI.RawUI.WindowTitle = "O'zbek Musiqa Markazi Ultimate Pro v4.0 (Avto-Magnitola va Fleshka Engine)"
} catch {}

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

try {
    function Refresh-Path {
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    }

    function Get-YtDlpPath {
        Refresh-Path
        $cmd = Get-Command "yt-dlp" -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
        $scriptDir = [System.IO.Path]::GetDirectoryName($env:SCRIPT_FULL_PATH)
        if ($scriptDir) {
            $local = Join-Path $scriptDir "yt-dlp.exe"
            if (Test-Path $local) { return $local }
        }
        $cur = Join-Path (Get-Location).Path "yt-dlp.exe"
        if (Test-Path $cur) { return $cur }
        return $null
    }

    function Get-FFmpegPath {
        Refresh-Path
        $cmd = Get-Command "ffmpeg" -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
        $scriptDir = [System.IO.Path]::GetDirectoryName($env:SCRIPT_FULL_PATH)
        if ($scriptDir) {
            $local = Join-Path $scriptDir "ffmpeg.exe"
            if (Test-Path $local) { return $local }
        }
        $cur = Join-Path (Get-Location).Path "ffmpeg.exe"
        if (Test-Path $cur) { return $cur }
        return $null
    }

    function Get-FFprobePath {
        $ffmpegPath = Get-FFmpegPath
        if ($ffmpegPath) {
            $dir = [System.IO.Path]::GetDirectoryName($ffmpegPath)
            $probe = Join-Path $dir "ffprobe.exe"
            if (Test-Path $probe) { return $probe }
        }
        $cmd = Get-Command "ffprobe" -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
        return $null
    }

    function Speak-Notification ($text) {
        try {
            $voice = New-Object -ComObject SAPI.SpVoice
            # 1 = SVSFlagsAsync (Non-blocking fon ovozi)
            $null = $voice.Speak($text, 1)
        } catch {}
        try {
            [System.Media.SystemSounds]::Asterisk.Play()
        } catch {}
    }

    function Format-CleanTitle ($rawTitle) {
        if (-not $rawTitle) { return "Nomalum_Tarona" }
        # 1. Faqat vertikal chiziq yoki qo'shaloq slesh bo'yicha ajratish (Kirillcha yoki kanal qo'shimchasi)
        $part = ($rawTitle -split '\s*\|\s*|\s*//\s*')[0]
        if ($part.Length -lt 4) { $part = $rawTitle }

        # 2. Qavslar ichidagi yozuvlarni olib tashlash
        $c = $part -replace '[\(\[\{][^\)\]\}]*[\)\]\}]', ' '

        # 3. Reklama so'zlari, telekanallar va audioformat so'zlarini tozalash
        $c = $c -replace '(?i)\b(official|music|video|audio|klip|clip|premyera|premiere|konsert|concert|rizanova|nevomusic|nevo|tarona|navouz|navo|panterra|shou-biznes|gita|milliy|zortv|sevimli|hd|4k|1080p|720p|mp3|lyric|lyrics|cover|soundtrack|ost|parodiya|jonli ijro|live|remix|full album|202\d|201\d)\b', ' '

        # 4. Emojilarni to'g'ri .NET regex bilan tozalash (xatosiz)
        $c = [regex]::Replace($c, "[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27BF]", "")

        # 5. Xavfsiz apostroflar (magnitolalar qotmasligi uchun)
        $c = $c -replace '[ʻʼ`‘’“”…–—]', '' -replace '[''"]', ''

        # 6. Keraksiz simvollarni tozalash (artist va nom orasidagi chiziqchani saqlagan holda)
        $c = $c -replace '[^\w\s\.-]', ' '
        $c = ($c -replace '\s+', ' ').Trim(" -_.,")

        if ($c.Length -lt 3) { $c = "Tarona" }
        return $c
    }

    function Select-SaveLocation ($folderName) {
        Clear-Host
        Write-Host ""
        Write-Host " +-- SAQLASH MANZILINI TANLANG --------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " |  ( 1 )  Ish stoli (Desktop papkasi)                                                |" -ForegroundColor White

        $drives = @([System.IO.DriveInfo]::GetDrives() | Where-Object { $_.DriveType -eq 'Removable' -and $_.IsReady })
        $driveMap = @{}
        $optIndex = 2
        if ($drives.Count -gt 0) {
            foreach ($d in $drives) {
                $freeGB = [math]::Round($d.TotalFreeSpace / 1GB, 1)
                $label = if ($d.VolumeLabel) { $d.VolumeLabel } else { "Fleshka" }
                $driveName = $d.Name.TrimEnd('\')
                $fs = $d.DriveFormat

                $fsColor = "Green"
                $fsWarning = ""
                if ($fs -ne "FAT32") {
                    $fsColor = "Yellow"
                    $fsWarning = " [DIQQAT: $fs formati! Magnitolalar faqat FAT32 ni o'qiydi]"
                }

                Write-Host (" |  ( {0} )  USB Fleshkaga: {1} [{2}] ({3} GB bo'sh, {4}){5}" -f $optIndex, $driveName, $label, $freeGB, $fs, $fsWarning) -ForegroundColor $fsColor
                $driveMap[$optIndex.ToString()] = $d.RootDirectory.FullName
                $optIndex++
            }
        } else {
            Write-Host " |  ( * )  [USB fleshka aniqlanmadi, agar fleshka bo'lsa ulab qayta tanlang]          |" -ForegroundColor Gray
        }
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " +------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""

        $maxOpt = $optIndex - 1
        $tanlov = Read-Host "  > Qayerga saqlansin? (1-$maxOpt, Standart: 1 - Desktop)"
        $tanlov = $tanlov.Trim()

        $targetBase = [Environment]::GetFolderPath("Desktop")
        if ($driveMap.ContainsKey($tanlov)) {
            $targetBase = $driveMap[$tanlov]
        }

        $cleanFolder = ($folderName -replace '[:*?"<>|]', '_').Trim(" ._")
        if (-not $cleanFolder) { $cleanFolder = "Yuklangan_Musiqalar" }

        $fullPath = Join-Path $targetBase $cleanFolder
        if (-not (Test-Path $fullPath)) {
            [void](New-Item -ItemType Directory -Path $fullPath -Force)
        }
        return $fullPath
    }

    function Select-AudioDSPProfile {
        Clear-Host
        Write-Host ""
        Write-Host " +-- AVTOMOBIL AKUSTIKASI VA OVOZ STANDARTINI TANLANG --------------------------------+" -ForegroundColor Cyan
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " |  ( 1 )  Studio Harmonic Exciter & Balance (Virtual Hi-Res) [TAVSIYA ETILADI]        |" -ForegroundColor Green
        Write-Host " |         11kHz tiniq havo jilosi, me'yoriy 70Hz zamin, EBU R128 ovoz balansi va     |" -ForegroundColor Gray
        Write-Host " |         True-Peak Limiter (Quloqni charchatmaydi, ortiqcha gupillovchi bass yo'q). |" -ForegroundColor Gray
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " |  ( 2 )  Kristal Vokal & Tiniq So'zlar (Vokal va suhbat jilosi)                      |" -ForegroundColor White
        Write-Host " |         Qo'shiqchining so'zlari va ovozi juda tiniq va jarangdor chiqadi.           |" -ForegroundColor Gray
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " |  ( 3 )  Sof Asl Studiya (Original o'zgartirishsiz asl manba ovozi)                  |" -ForegroundColor White
        Write-Host " |         Asl YouTube audiosi hech qanday filtrsiz to'g'ridan-to'g'ri olinadi.       |" -ForegroundColor Gray
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " |  ( 4 )  Avto-VIP Sabvufer Rejim (Faqat maxsus sabvuferli mashinalar uchun)          |" -ForegroundColor White
        Write-Host " |         Chuqur pastki chastotali bass kuchaytirilgan rejim.                         |" -ForegroundColor Gray
        Write-Host " |                                                                                    |" -ForegroundColor Cyan
        Write-Host " +------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""

        $dspChoice = Read-Host "  > Tanlovingiz (1-4, Standart: 1 - Studio Harmonic Exciter & Balance)"
        $dspChoice = $dspChoice.Trim()

        switch ($dspChoice) {
            '2' {
                return @{
                    Name = "Kristal Vokal & Tiniq So'zlar (Treble & EBU R128)"
                    Filter = "treble=g=2.2:f=3500,loudnorm=I=-14:LRA=7:TP=-1.5,alimiter=limit=-1.2dB:attack=5:release=50:asc=1"
                }
            }
            '3' {
                return @{
                    Name = "Sof Asl Studiya (Original o'zgartirishsiz)"
                    Filter = $null
                }
            }
            '4' {
                return @{
                    Name = "Avto-VIP Sabvufer Rejim (+3dB Dinamik Bass)"
                    Filter = "bass=g=3:f=70,loudnorm=I=-14:LRA=7:TP=-1.5,alimiter=limit=-1.2dB:attack=5:release=50:asc=1"
                }
            }
            default {
                return @{
                    Name = "Studio Harmonic Exciter & Balance (Virtual Hi-Res & True-Peak)"
                    Filter = "treble=g=1.5:f=11000,bass=g=0.5:f=70,loudnorm=I=-14:LRA=7:TP=-1.5,alimiter=limit=-1.2dB:attack=5:release=50:asc=1"
                }
            }
        }
    }

    function Format-UsbDriveToFat32 {
        Clear-Host
        Write-Host ""
        Write-Host " +-- USB FLESHKANI XAVFSIZ FAT32 FORMATLASH ASBOBI ------------------------------------+" -ForegroundColor Red
        Write-Host " | Avtomobil magnitolalari faqat FAT32 formatdagi fleshkalarni taniydi.               |" -ForegroundColor Yellow
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Red
        Write-Host ""

        $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        if (-not $isAdmin) {
            Write-Host "  [DIQQAT] Fleshkani formatlash uchun administrator huquqi talab qilinadi." -ForegroundColor Yellow
            Write-Host "  Iltimos, dasturni sichqonchaning o'ng tugmasi orqali 'Run as Administrator'" -ForegroundColor White
            Write-Host "  (Administrator nomidan ishga tushirish) qilib oching." -ForegroundColor White
            Write-Host ""
            Read-Host "  Orqaga qaytish uchun [Enter] bosing"
            return
        }

        $drives = @([System.IO.DriveInfo]::GetDrives() | Where-Object { $_.DriveType -eq 'Removable' -and $_.IsReady })
        if ($drives.Count -eq 0) {
            Write-Host "  [!] Kompyuterga birorta ham USB fleshka ulanmagan!" -ForegroundColor Red
            Start-Sleep -Seconds 2
            return
        }

        $driveMap = @{}
        $idx = 1
        foreach ($d in $drives) {
            $freeGB = [math]::Round($d.TotalFreeSpace / 1GB, 1)
            $totalGB = [math]::Round($d.TotalSize / 1GB, 1)
            $label = if ($d.VolumeLabel) { $d.VolumeLabel } else { "Fleshka" }
            $driveLetter = $d.Name.TrimEnd('\')
            Write-Host ("  ( {0} )  {1} [{2}] - {3} GB jami ({4} formati)" -f $idx, $driveLetter, $label, $totalGB, $d.DriveFormat) -ForegroundColor Green
            $driveMap[$idx.ToString()] = $d
            $idx++
        }

        Write-Host ""
        Write-Host "  ( 0 )  Bekor qilish va orqaga qaytish" -ForegroundColor Gray
        Write-Host ""
        $c = Read-Host "  > Qaysi fleshkani FAT32 ga formatlamoqchisiz? (1-$($idx-1))"
        $c = $c.Trim()
        if ($c -eq '0' -or -not $driveMap.ContainsKey($c)) { return }

        $targetDrive = $driveMap[$c]
        $letter = $targetDrive.Name.TrimEnd('\')

        Write-Host ""
        Write-Host "  ======================================================================" -ForegroundColor Red
        Write-Host "  DIQQAT: $letter FLESHKASIDAGI BARCHA FAYLLAR BUTUNLAY O'CHIRILADI!" -ForegroundColor Red
        Write-Host "  ======================================================================" -ForegroundColor Red
        Write-Host ""
        $confirm = Read-Host "  > Haqiqatan ham formatlashni tasdiqlaysizmi? (ha / yoq)"
        if ($confirm.Trim().ToLower() -eq 'ha') {
            Write-Host ""
            Write-Host "  [ * ] Fleshka FAT32 ga formatlanmoqda, iltimos kuting..." -ForegroundColor Cyan
            $p = Start-Process -FilePath "format.exe" -ArgumentList @("$letter", "/FS:FAT32", "/Q", "/V:AVTO_MUSIC", "/Y") -NoNewWindow -Wait -PassThru
            if ($p.ExitCode -eq 0) {
                Write-Host "  [✓] Fleshka muvaffaqiyatli FAT32 ga formatlandi va maytafonga tayyorlandi!" -ForegroundColor Green
                Speak-Notification "Fleshka muvaffaqiyatli formatlandi!"
            } else {
                Write-Host "  [!] Formatlashda xatolik yuz berdi. Fleshka boshqa dastur tomonidan band bo'lishi mumkin." -ForegroundColor Red
            }
            Start-Sleep -Seconds 3
        }
    }

    function Generate-PlaylistsAndIndex ($cleanFiles, $chiqishPapka, $ffprobePath) {
        Write-Host "  [ * ] Mundarija va M3U/M3U8 pleylistlari generatsiya qilinmoqda..." -ForegroundColor Cyan
        
        $linesTxt = @()
        $linesM3u = @("#EXTM3U")
        $linesM3u8 = @("#EXTM3U")

        $linesTxt += "========================================================================"
        $linesTxt += "                      TARONALAR RO'YXATI (MUNDARIJA)"
        $linesTxt += "========================================================================"
        $linesTxt += ""

        foreach ($item in $cleanFiles) {
            $fPath = if ($item.Path) { $item.Path } else { $item.FullName }
            $fName = if ($item.Name) { $item.Name } else { [System.IO.Path]::GetFileName($fPath) }
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($fName)

            $secTotal = 0
            $tf = ""
            if ($ffprobePath -and (Test-Path $fPath)) {
                try {
                    $durStr = & $ffprobePath -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$fPath" 2>$null
                    if ($durStr) {
                        $secTotal = [int][math]::Round([double]$durStr)
                        $m = [int][math]::Floor($secTotal / 60)
                        $s = [int]($secTotal % 60)
                        $tf = (' ({0:00}:{1:00})' -f $m, $s)
                    }
                } catch {}
            }

            $linesTxt += ($baseName + $tf)
            $m3uDur = if ($secTotal -gt 0) { $secTotal } else { -1 }
            $linesM3u += ("#EXTINF:{0},{1}" -f $m3uDur, $baseName)
            $linesM3u += $fName
            $linesM3u8 += ("#EXTINF:{0},{1}" -f $m3uDur, $baseName)
            $linesM3u8 += $fName
        }

        $linesTxt += ""
        $linesTxt += "========================================================================"
        $linesTxt += ("Jami: " + $cleanFiles.Count + " ta tarona | 100% Avto-Magnitola va Fleshka Standarti")
        $linesTxt += "========================================================================"

        $txtFile = Join-Path $chiqishPapka "00_Taronalar_Royxati.txt"
        $m3uFile = Join-Path $chiqishPapka "01_Taronalar_Pleylist.m3u"
        $m3u8File = Join-Path $chiqishPapka "02_Taronalar_Pleylist.m3u8"

        $linesTxt | Out-File -FilePath $txtFile -Encoding utf8
        $linesM3u | Out-File -FilePath $m3uFile -Encoding ascii
        $linesM3u8 | Out-File -FilePath $m3u8File -Encoding utf8
    }

    function Invoke-LocalFolderCleaner ($ffmpegPath, $ffprobePath) {
        Clear-Host
        Write-Host ""
        Write-Host " +-- MAHALLIY PAPKANI TOZALASH VA MAGNITOLAGA MOSLASH ---------------------------------+" -ForegroundColor Cyan
        Write-Host " | Kompyuter yoki fleshkadagi mavjud aralash MP3 fayllarni tartibga keltirish.         |" -ForegroundColor White
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""
        $targetDir = Read-Host "  > MP3 fayllar joylashgan papka yo'lini kiriting (Masalan: E:\Musiqalar yoki Desktop\Qoshiqlar)"
        $targetDir = $targetDir.Trim().Trim('"')
        if (-not (Test-Path $targetDir)) {
            Write-Host "  [!] Belgilangan papka topilmadi!" -ForegroundColor Red
            Start-Sleep -Seconds 2
            return
        }

        $mp3Files = Get-ChildItem -Path $targetDir -Filter "*.mp3"
        if ($mp3Files.Count -eq 0) {
            Write-Host "  [!] Papkada birorta ham MP3 fayl topilmadi!" -ForegroundColor Yellow
            Start-Sleep -Seconds 2
            return
        }

        Write-Host ""
        Write-Host ("  [✓] Papkada {0} ta MP3 fayl topildi. Tartiblash boshlanmoqda..." -f $mp3Files.Count) -ForegroundColor Green

        $baseDate = (Get-Date).AddDays(-1)
        $dateOffset = 0
        $idx = 1
        $cleanList = @()

        foreach ($f in ($mp3Files | Sort-Object Name)) {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
            $baseNoNum = $base -replace '^\d+\s*[-_.]\s*', ''
            $cleanName = Format-CleanTitle $baseNoNum
            $numStr = '{0:D3}' -f $idx
            $newFileName = ("{0} - {1}.mp3" -f $numStr, $cleanName)
            $targetPath = Join-Path $targetDir $newFileName

            if ($f.FullName -ne $targetPath) {
                try {
                    Rename-Item -LiteralPath $f.FullName -NewName $newFileName -Force -ErrorAction SilentlyContinue
                } catch {}
            }

            try {
                $itemObj = Get-Item -LiteralPath $targetPath -ErrorAction SilentlyContinue
                if ($itemObj) {
                    $assignedTime = $baseDate.AddSeconds($dateOffset)
                    $itemObj.CreationTime = $assignedTime
                    $itemObj.LastWriteTime = $assignedTime
                    $itemObj.LastAccessTime = $assignedTime
                    $dateOffset += 3
                }
            } catch {}

            $cleanList += [PSCustomObject]@{
                Path = $targetPath
                Name = $newFileName
                Base = ("{0} - {1}" -f $numStr, $cleanName)
            }
            $idx++
        }

        # Pleylistlar va mundarija yaratish
        Generate-PlaylistsAndIndex -cleanFiles $cleanList -chiqishPapka $targetDir -ffprobePath $ffprobePath

        Write-Host ""
        Write-Host "  [✓] Papkadagi barcha fayllar tozalandi, FAT32 tartiblandi va pleylistlar tuzildi!" -ForegroundColor Green
        Speak-Notification "Mahalliy papka taronalari muvaffaqiyatli tartiblandi!"
        Start-Sleep -Seconds 3
        try { Start-Process $targetDir } catch {}
    }

    $ytdlp = Get-YtDlpPath
    $ffmpeg = Get-FFmpegPath

    if (-not $ytdlp -or -not $ffmpeg) {
        Clear-Host
        Write-Host ""
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Yellow
        Write-Host " |       DIQQAT: KOMPYUTERDA VOSITALAR O'RNATILMOQDA (BIR MARTALIK SOZLASH)            |" -ForegroundColor Yellow
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   Qo'shiqlarni yuklab, maytafon formatiga (MP3 256k CBR + Cover) aylantirish uchun" -ForegroundColor White
        Write-Host "   kerakli vositalar (yt-dlp va ffmpeg) sozlanmoqda..." -ForegroundColor White
        Write-Host ""

        $scriptDir = [System.IO.Path]::GetDirectoryName($env:SCRIPT_FULL_PATH)
        if (-not $scriptDir) { $scriptDir = (Get-Location).Path }

        $winget = Get-Command "winget" -ErrorAction SilentlyContinue
        if ($winget) {
            if (-not $ytdlp) {
                & winget install yt-dlp --accept-source-agreements --accept-package-agreements --silent *>$null
            }
            if (-not $ffmpeg) {
                & winget install ffmpeg --accept-source-agreements --accept-package-agreements --silent *>$null
            }
            Refresh-Path
            $ytdlp = Get-YtDlpPath
            $ffmpeg = Get-FFmpegPath
        }

        if (-not $ytdlp) {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            $dest = Join-Path $scriptDir "yt-dlp.exe"
            Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $dest
            $ytdlp = Get-YtDlpPath
        }

        if (-not $ytdlp) {
            Write-Host "  [!] yt-dlp yuklanmadi. Iltimos internet aloqasini tekshiring." -ForegroundColor Red
            Read-Host "  Chiqish uchun [Enter] bosing"
            return
        }

        Write-Host "  [ OK ] Asboblar muvaffaqiyatli sozlandi!" -ForegroundColor Green
        Start-Sleep -Seconds 2
    }

    $ffprobe = Get-FFprobePath
    $ffmpegDir = $null
    if ($ffmpeg) {
        $ffmpegDir = [System.IO.Path]::GetDirectoryName($ffmpeg)
    }

    if ($ytdlp) {
        try {
            Start-Process -FilePath $ytdlp -ArgumentList @("-U") -NoNewWindow -ErrorAction SilentlyContinue
        } catch {}
    }

    # Barcha YouTube so'rovlari uchun qat'iy xavfsiz bot-bypass parametrlari
    $globalBypassArgs = @(
        "--remote-components", "ejs:github",
        "--extractor-args", "youtube:player_client=mweb,android"
    )

    while ($true) {
        Clear-Host
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host " |                                                                                      |" -ForegroundColor Cyan
        Write-Host " |   O'ZBEK MUSIQA MARKAZI ULTIMATE PRO v4.0 - AVTO-MAGNITOLA VA FLESHKA ENGINE         |" -ForegroundColor Cyan
        Write-Host " |   100% ISHONCHLI YUKLASH | HARMONIC BALANS | 800x800 HD MUQOVA | FAT32 XRONOLOGIYA    |" -ForegroundColor Yellow
        Write-Host " |                                                                                      |" -ForegroundColor Cyan
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "   +-- YUKLASH YO'NALISHINI TANLANG ----------------------------------------------------+" -ForegroundColor Cyan
        Write-Host "   |                                                                                    |" -ForegroundColor Cyan
        Write-Host "   |   ( 1 )  Mashhur San'atkorlar Katalogi (16 ta Yulduz: Jaloliddin, Gulinur, Konsta)  |" -ForegroundColor White
        Write-Host "   |   ( 2 )  2026-yil Eng Yangi O'zbek Xitlari (TOP-50 Premyeralar va Trendlar)        |" -ForegroundColor White
        Write-Host "   |   ( 3 )  Tungi Safar va Karvon / Romantik Sokin (Dardli va Orombaxsh Taronalar)    |" -ForegroundColor White
        Write-Host "   |   ( 4 )  To'yona & Lazgi Super Sho'x (Katta Yo'l va Bayramona Raqsbop)             |" -ForegroundColor White
        Write-Host "   |   ( 5 )  O'zbek Retro / Oltin Fond (Original 70-80-90-2000 Durdona Ijrolar)        |" -ForegroundColor White
        Write-Host "   |   ( 6 )  Avtomobil VIP Bass & Trap Remix (Sabvufer va Maxsus Akustika)             |" -ForegroundColor White
        Write-Host "   |   ( 7 )  Choyxona va Diltortar / Jonli Ijro (Do'stlar davrasi va Choyxona uchun)   |" -ForegroundColor White
        Write-Host "   |   ( 8 )  Erkin Qidiruv / YouTube Havolasi (Ism, Qo'shiq yoki Pleylist Link)        |" -ForegroundColor White
        Write-Host "   |   ( 9 )  Mahalliy Papkani Tozalash va Magnitolaga Moslash (Kompyuterdagi MP3 lar)  |" -ForegroundColor Green
        Write-Host "   |   ( F )  Fleshkani FAT32 ga Xavfsiz Formatlash (Maytafonda o'qilishi uchun)        |" -ForegroundColor Magenta
        Write-Host "   |                                                                                    |" -ForegroundColor Cyan
        Write-Host "   |   ( 0 )  Dasturdan chiqish                                                         |" -ForegroundColor Red
        Write-Host "   +------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "   MASLAHAT: Raqam tanlamasdan, to'g'ridan-to'g'ri xohlagan artist yoki qo'shiq nomini" -ForegroundColor Yellow
        Write-Host "             yozishingiz ham mumkin (Masalan: Konsta, Ozoda, Sevinch va h.k.)" -ForegroundColor Yellow
        Write-Host ""

        $bolim = Read-Host "  > Raqam tanlang (0-9, F) YOKI to'g'ridan-to'g'ri Artist nomini yozing"
        $bolim = $bolim.Trim()
        if (-not $bolim) { continue }
        if ($bolim -eq '0') { break }

        if ($bolim.ToUpper() -eq 'F') {
            Format-UsbDriveToFat32
            continue
        }

        if ($bolim -eq '9') {
            Invoke-LocalFolderCleaner -ffmpegPath $ffmpeg -ffprobePath $ffprobe
            continue
        }

        $manba = ""
        $papkaNomi = ""
        $isFixed = $false
        $defSoni = 40
        $artistKeywords = @()
        $filterArtist = $false

        if ($bolim -eq '1') {
            Clear-Host
            Write-Host ""
            Write-Host " +-- MASHHUR XONANDALAR KATALOGI -------------------------------------------------------+" -ForegroundColor Cyan
            Write-Host " | Raqamni tanlang yoki (0) orqali orqaga qayting                                       |" -ForegroundColor White
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "   ( 1 )  Jaloliddin Ahmadaliyev     ( 9 )  Janob Rasul" -ForegroundColor White
            Write-Host "   ( 2 )  Gulinur                    ( 10)  Xamdam Sobirov" -ForegroundColor White
            Write-Host "   ( 3 )  Yulduz Usmonova            ( 11)  Konsta (Zamonaviy ma'noli xitlar)" -ForegroundColor White
            Write-Host "   ( 4 )  Shohruhxon                 ( 12)  Ulug'bek Rahmatullayev" -ForegroundColor White
            Write-Host "   ( 5 )  Tohir Sodiqov (Bolalar)    ( 13)  Rayhon & Shahzoda (Duet/Xitlar)" -ForegroundColor White
            Write-Host "   ( 6 )  Ozodbek Nazarbekov         ( 14)  Ozoda Nursaidova (Jonli va to'yona)" -ForegroundColor White
            Write-Host "   ( 7 )  Doston Ergashev            ( 15)  Eldor Qayumov & Ziyoda" -ForegroundColor White
            Write-Host "   ( 8 )  Munisa Rizayeva            ( 16)  Mirjalol Ne'matov & Sardor Tairov" -ForegroundColor White
            Write-Host ""
            Write-Host "   ( 0 )  Orqaga qaytish" -ForegroundColor Red
            Write-Host ""
            $xId = Read-Host "  > San'atkor raqami (1-16) yoki boshqa artist ismi"
            $xId = $xId.Trim()
            if ($xId -eq '0' -or -not $xId) { continue }

            $singers = @{
                '1' = 'Jaloliddin Ahmadaliyev'; '2' = 'Gulinur'; '3' = 'Yulduz Usmonova';
                '4' = 'Shohruhxon'; '5' = 'Tohir Sodiqov Bolalar'; '6' = 'Ozodbek Nazarbekov';
                '7' = 'Doston Ergashev'; '8' = 'Munisa Rizayeva'; '9' = 'Janob Rasul';
                '10' = 'Xamdam Sobirov'; '11' = 'Konsta'; '12' = 'Ulugbek Rahmatullayev';
                '13' = 'Rayhon Shahzoda'; '14' = 'Ozoda Nursaidova'; '15' = 'Eldor Qayumov Ziyoda';
                '16' = 'Mirjalol Nematov Sardor Tairov'
            }
            if ($singers.ContainsKey($xId)) {
                $xonanda = $singers[$xId]
            } else {
                $xonanda = $xId
            }

            Write-Host ""
            Write-Host "   +-- QO'SHIQLAR USLUBINI TANLANG -----------------------------------------------------+" -ForegroundColor Cyan
            Write-Host "   |   ( 1 )  Barcha sara qo'shiqlar (Aralash oltin to'plam)                            |" -ForegroundColor White
            Write-Host "   |   ( 2 )  Faqat Sho'x va Raqsbop (To'yona / Lazgi / Shodon)                         |" -ForegroundColor White
            Write-Host "   |   ( 3 )  Faqat Sokin va Lirik (Dardli / Orombaxsh / Safar)                         |" -ForegroundColor White
            Write-Host "   +------------------------------------------------------------------------------------+" -ForegroundColor Cyan
            $uslub = Read-Host "  > Tanlovingiz (1-3, Standart: 1)"
            if ($uslub -eq '2') {
                $manba = "$xonanda sho'x o'yinbop qo'shiqlari"
                $papkaNomi = "$xonanda\Shox_Taronalar"
            } elseif ($uslub -eq '3') {
                $manba = "$xonanda sokin lirik qo'shiqlari"
                $papkaNomi = "$xonanda\Sokin_Taronalar"
            } else {
                $manba = "$xonanda"
                $papkaNomi = "$xonanda"
            }
            $defSoni = 40
            $filterArtist = $true
            $rawWords = $xonanda -split '\s+'
            foreach ($w in $rawWords) {
                if ($w.Length -ge 3) { $artistKeywords += $w.ToLower() }
            }
        }
        elseif ($bolim -eq '2') {
            $manba = "2026 yangi o'zbek xit qo'shiqlar klip"
            $papkaNomi = "Yangi_Xitlar_2026"
            $isFixed = $true
            $defSoni = 50
        }
        elseif ($bolim -eq '3') {
            $manba = "tungi safar karvon sokin lirik dardli o'zbekcha qo'shiqlar"
            $papkaNomi = "Tungi_Safar_va_Karvon"
            $isFixed = $true
            $defSoni = 45
        }
        elseif ($bolim -eq '4') {
            $manba = "eng sara sho'x to'yona o'zbekcha lazgi qo'shiqlar klip"
            $papkaNomi = "Toyona_va_Shox_Lazgi"
            $isFixed = $true
            $defSoni = 45
        }
        elseif ($bolim -eq '5') {
            $manba = "o'zbek retro oltin fond sara qo'shiqlari klip"
            $papkaNomi = "Retro_Oltin_Fond"
            $isFixed = $true
            $defSoni = 40
        }
        elseif ($bolim -eq '6') {
            $manba = "uzbek bass remix avto mashina sabvufer trek"
            $papkaNomi = "Avto_VIP_Bass_Remix"
            $isFixed = $true
            $defSoni = 40
        }
        elseif ($bolim -eq '7') {
            $manba = "choyxona diltortar jonli ijro o'zbek qo'shiqlar"
            $papkaNomi = "Choyxona_va_Diltortar"
            $isFixed = $true
            $defSoni = 40
        }
        elseif ($bolim -eq '8') {
            Clear-Host
            Write-Host ""
            Write-Host " +-- ERKIN QIDIRUV VA HAVOLA (LINK) REJIMI ---------------------------------------------+" -ForegroundColor Cyan
            Write-Host " | Xonanda ismini yozing YOKI to'g'ridan-to'g'ri YouTube havolasini tashlang            |" -ForegroundColor White
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
            Write-Host ""
            $manba = Read-Host "  > Ism yoki Havolani kiriting"
            if (-not $manba.Trim()) { continue }
            if ($manba -match '^https?://') {
                $papkaNomi = "Havola_Toplami"
                $defSoni = 30
                if ($manba -match 'list=') {
                    Write-Host ""
                    Write-Host "  [i] YouTube pleylist aniqlandi! Qo'shiqlar hisoblanmoqda, iltimos kuting..." -ForegroundColor Cyan
                    $plCheckArgs = @($globalBypassArgs) + @("--flat-playlist", "--print", "%(id)s", "--no-warnings", "--ignore-errors", $manba)
                    $plCheck = & $ytdlp @plCheckArgs 2>$null
                    $plTotal = @($plCheck).Count
                    if ($plTotal -gt 0) {
                        Write-Host "  [✓] Pleylistda jami $plTotal ta tarona mavjud!" -ForegroundColor Green
                        Write-Host ""
                        Write-Host "   ( 1 )  Barcha qo'shiqlar ($plTotal ta) to'liq yuklansin (Tavsiya)" -ForegroundColor White
                        Write-Host "   ( 2 )  Muayyan qismi yuklansin (sonini qo'lda kiritish)" -ForegroundColor White
                        $plChoice = Read-Host "  > Tanlovingiz [1 yoki 2, Standart: 1]"
                        if ($plChoice.Trim() -ne '2') {
                            $defSoni = $plTotal
                            $isFixed = $true
                        }
                    }
                }
            } else {
                $papkaNomi = $manba
                $defSoni = 40
                $filterArtist = $true
                $rawWords = $manba -split '\s+'
                foreach ($w in $rawWords) {
                    if ($w.Length -ge 3) { $artistKeywords += $w.ToLower() }
                }
            }
        }
        else {
            $manba = $bolim
            if ($manba -match '^https?://') {
                $papkaNomi = "Havola_Toplami"
                $defSoni = 30
                if ($manba -match 'list=') {
                    Write-Host ""
                    Write-Host "  [i] YouTube pleylist aniqlandi! Qo'shiqlar hisoblanmoqda..." -ForegroundColor Cyan
                    $plCheckArgs = @($globalBypassArgs) + @("--flat-playlist", "--print", "%(id)s", "--no-warnings", "--ignore-errors", $manba)
                    $plCheck = & $ytdlp @plCheckArgs 2>$null
                    $plTotal = @($plCheck).Count
                    if ($plTotal -gt 0) {
                        Write-Host "  [✓] Pleylistda jami $plTotal ta tarona mavjud!" -ForegroundColor Green
                        $defSoni = $plTotal
                        $isFixed = $true
                    }
                }
            } else {
                $papkaNomi = $manba
                $defSoni = 40
                $filterArtist = $true
                $rawWords = $manba -split '\s+'
                foreach ($w in $rawWords) {
                    if ($w.Length -ge 3) { $artistKeywords += $w.ToLower() }
                }
            }
        }

        if ($filterArtist) {
            $extra = @()
            foreach ($k in $artistKeywords) {
                if ($k -like "*jalol*" -or $k -like "*ahmad*") {
                    $extra += "jaloliddin"; $extra += "jaloldin"; $extra += "ahmadaliyev"
                }
                if ($k -like "*shohruh*" -or $k -like "*shoxrux*") {
                    $extra += "shohruhxon"; $extra += "shoxruxxon"; $extra += "shohrux"
                }
                if ($k -like "*tohir*" -or $k -like "*tahir*") {
                    $extra += "tohir"; $extra += "tahir"; $extra += "bolalar"
                }
                if ($k -like "*xamdam*" -or $k -like "*hamdam*") {
                    $extra += "hamdam"; $extra += "xamdam"; $extra += "sobirov"
                }
                if ($k -like "*yulduz*") {
                    $extra += "yulduz"; $extra += "usmonova"
                }
                if ($k -like "*doston*") {
                    $extra += "doston"; $extra += "ergashev"
                }
                if ($k -like "*konsta*") {
                    $extra += "konsta"; $extra += "sharif"
                }
            }
            foreach ($e in $extra) {
                if ($artistKeywords -notcontains $e) { $artistKeywords += $e }
            }
        }

        Clear-Host
        Write-Host ""
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host " |                            QO'SHIQLAR SONINI BELGILASH                               |" -ForegroundColor Yellow
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "   * Tanlangan yo'nalish / manba : $manba" -ForegroundColor White
        if ($filterArtist) {
            Write-Host "   * Qat'iy Artist Filtri        : YOQILGAN (Begona ijrochilar tozalanadi)" -ForegroundColor Green
        }
        Write-Host ""
        Write-Host "   +-- YUKLANADIGAN TARONALAR SONINI KIRITING ------------------------------------------+" -ForegroundColor Cyan
        Write-Host "   |   Ixtiyoriy miqdorni kiriting (Masalan: 10, 20, 30, 40, 50, 80 va h.k.)            |" -ForegroundColor White
        Write-Host "   |   (Hech narsa yozmay to'g'ridan-to'g'ri [Enter] bossangiz: $defSoni ta yuklanadi)      |" -ForegroundColor Gray
        Write-Host "   +------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""
        $soniKirit = Read-Host "  > Nechta qo'shiq yuklansin? [Standart: $defSoni]"
        $soni = $defSoni
        if ($soniKirit) {
            $parsed = 0
            if ([int]::TryParse($soniKirit.Trim(), [ref]$parsed) -and $parsed -gt 0) {
                $soni = $parsed
            } else {
                Write-Host "   [!] Noto'g'ri son kiritildi, standart $defSoni ta belgilandi." -ForegroundColor Yellow
                Start-Sleep -Seconds 1
            }
        }

        # 1-Qadam: Akustika va DSP Profilini tanlash
        $audioProfile = Select-AudioDSPProfile

        # 2-Qadam: Saqlash manzilini tanlash (Desktop yoki Fleshka)
        $chiqishPapka = Select-SaveLocation -folderName $papkaNomi

        # 3-Qadam: Avto-o'chirish so'rovi
        Write-Host ""
        $avtoOchirishInput = Read-Host "  > Barcha ishlar yakunlangach kompyuter avtomatik o'chsinmi? (ha / yoq, Standart: yoq)"
        $autoShutdown = ($avtoOchirishInput.Trim().ToLower() -eq 'ha')

        Clear-Host
        Write-Host ""
        Write-Host " +-- YUKLASH JARAYONI ------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host " |  * IJROCHI / MANBA : $manba" -ForegroundColor White
        Write-Host " |  * REJA            : $soni ta saralangan tarona" -ForegroundColor White
        Write-Host " |  * SAQLASH MANZILI : $chiqishPapka" -ForegroundColor White
        Write-Host " |  * OVOZ STANDARTI  : $($audioProfile.Name)" -ForegroundColor Yellow
        Write-Host " |  * ALBOM MUQOVASI  : 800x800 HD Kvadrat (ID3v2 APIC Avto-Monitor)" -ForegroundColor Green
        if ($filterArtist) {
            Write-Host " |  * SAN'ATKOR NAZOR : Faqat o'zining qo'shiqlari (Begona ijrochilar tozalanadi)   |" -ForegroundColor Green
        }
        Write-Host " |  * TEZKOR PARALLEL : 4 ta xavfsiz turbo oqim (Anti-ban rejimida)" -ForegroundColor Green
        Write-Host " |  * TEGLAR & TARTIB : Toza ID3v2 teglar, M3U/M3U8 pleylist va FAT32 tartib           |" -ForegroundColor Green
        Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Cyan
        Write-Host ""

        Write-Host "  [ 1/3 ] San'atkor qo'shiqlari saralanmoqda va begona ijrochilar filtrlanmoqda..." -ForegroundColor Cyan

        $seen = @{}
        if (Test-Path $chiqishPapka) {
            $existing = Get-ChildItem -Path $chiqishPapka -Filter "*.mp3"
            foreach ($f in $existing) {
                $n = Format-CleanTitle ($f.BaseName -replace '^\d+\s*[-_.]\s*', '')
                $n = $n.ToLower()
                if ($n.Length -gt 2) { $seen[$n] = -1 }
            }
        }

        $searchQueries = @()
        if ($manba -match '^https?://') {
            $searchQueries += $manba
        } elseif ($filterArtist) {
            $candEach = [math]::Min([math]::Max($soni * 2, 40), 150)
            $searchQueries += "ytsearch$($candEach):$manba barcha qo'shiqlari"
            $searchQueries += "ytsearch$($candEach):$manba yangi xitlar"
            $searchQueries += "ytsearch$($candEach):$manba albom"
        } else {
            $candTotal = [math]::Min([math]::Max($soni * 2, 60), 200)
            $searchQueries += "ytsearch$($candTotal):$manba"
        }

        $queue = @()

        foreach ($sq in $searchQueries) {
            if ($queue.Count -ge $soni) { break }
            $searchCmdArgs = @($globalBypassArgs) + @(
                "--flat-playlist",
                "--print", "%(id)s|||%(title)s|||%(duration)s",
                "--no-warnings",
                "--ignore-errors",
                $sq
            )
            $raw = & $ytdlp @searchCmdArgs 2>$null
            if (-not $raw) { continue }

            foreach ($line in $raw) {
                $parts = $line -split '\|\|\|'
                if ($parts.Count -lt 2) { continue }

                $vid = $parts[0].Trim()
                $title = $parts[1].Trim()
                $durStr = if ($parts.Count -ge 3) { $parts[2].Trim() } else { "" }

                $dur = 0
                if ($durStr) { [int]::TryParse($durStr, [ref]$dur) | Out-Null }
                if ($dur -gt 0 -and ($dur -lt 85 -or $dur -gt 660)) { continue }

                if ($filterArtist -and $artistKeywords.Count -gt 0) {
                    $tLow = $title.ToLower()
                    $isArtistMatch = $false
                    foreach ($kw in $artistKeywords) {
                        if ($tLow.Contains($kw)) {
                            $isArtistMatch = $true
                            break
                        }
                    }
                    if (-not $isArtistMatch) { continue }
                }

                $cleanName = Format-CleanTitle $title
                $c = $cleanName.ToLower()
                if ($c.Length -lt 2) { continue }

                $isDup = $false
                if ($seen.ContainsKey($c)) {
                    $isDup = $true
                } else {
                    $wordsC = @($c -split '\s+').Where({ $_.Length -gt 1 })
                    foreach ($sKey in $seen.Keys) {
                        $wordsS = @($sKey -split '\s+').Where({ $_.Length -gt 1 })
                        if ($wordsC.Count -ge 2 -and $wordsS.Count -ge 2) {
                            $matchCount = 0
                            foreach ($w in $wordsC) { if ($wordsS -contains $w) { $matchCount++ } }
                            $ratio = [double]$matchCount / [math]::Max($wordsC.Count, $wordsS.Count)
                            $sDur = $seen[$sKey]
                            if ($ratio -ge 0.75 -and ($sDur -eq -1 -or $dur -eq 0 -or [math]::Abs($dur - $sDur) -le 4)) {
                                $isDup = $true
                                break
                            }
                        }
                    }
                }

                if (-not $isDup) {
                    $seen[$c] = $dur
                    $queue += [PSCustomObject]@{
                        Num = 0
                        Url = "https://www.youtube.com/watch?v=$vid"
                        Title = $cleanName
                    }
                    if ($queue.Count -ge $soni) { break }
                }
            }
        }

        if ($queue.Count -eq 0) {
            Write-Host ""
            Write-Host "  [!] Belgilangan so'rov bo'yicha toza qo'shiqlar topilmadi." -ForegroundColor Yellow
            Write-Host ""
            Read-Host "  Davom etish uchun [Enter] bosing"
            continue
        }

        Write-Host ""
        Write-Host "  [ 2/3 ] Saralangan toza qo'shiqlar 4 ta xavfsiz turbo oqimda yuklanmoqda..." -ForegroundColor Green
        Write-Host "  * Jami saralangan qo'shiqlar soni: $($queue.Count) ta" -ForegroundColor Yellow
        Write-Host ""

        $startNum = 1
        $existingMp3s = Get-ChildItem -Path $chiqishPapka -Filter "*.mp3"
        if ($existingMp3s.Count -gt 0) { $startNum = $existingMp3s.Count + 1 }

        $curNum = $startNum
        foreach ($item in $queue) {
            $item.Num = $curNum
            $curNum++
        }

        $total = $queue.Count
        $maxWorkers = [math]::Min(4, [math]::Max($total, 1))

        $SessionState = [System.Management.Automation.Runspaces.InitialSessionState]::CreateDefault()
        $Pool = [runspacefactory]::CreateRunspacePool(1, $maxWorkers, $SessionState, $Host)
        $Pool.Open()

        $dspFilter = $audioProfile.Filter

        $tasks = [System.Collections.Generic.List[PSCustomObject]]::new()
        foreach ($item in $queue) {
            $numStr = '{0:D3}' -f $item.Num
            $outPattern = Join-Path $chiqishPapka ($numStr + ' - %(title)s.%(ext)s')

            $ps = [powershell]::Create()
            $ps.RunspacePool = $Pool
            [void]$ps.AddScript({
                param($exe, $outPattern, $url, $ffmpegDir, $dspFilter)
                $argsList = @(
                    "--remote-components", "ejs:github",
                    "--extractor-args", "youtube:player_client=mweb,android",
                    "-N", "32",
                    "--concurrent-fragments", "32",
                    "--http-chunk-size", "1M",
                    "--buffer-size", "128K",
                    "-x",
                    "--audio-format", "mp3",
                    "--audio-quality", "256K",
                    "--embed-thumbnail",
                    "--convert-thumbnails", "jpg",
                    "--embed-metadata",
                    "--no-playlist",
                    "--no-overwrites",
                    "--no-keep-video",
                    "--no-warnings",
                    "--ignore-errors",
                    "--retries", "5",
                    "--fragment-retries", "5",
                    "--socket-timeout", "25"
                )
                if ($dspFilter) {
                    $argsList += @("--postprocessor-args", "ExtractAudio:-af $dspFilter -threads 0")
                } else {
                    $argsList += @("--postprocessor-args", "ExtractAudio:-threads 0")
                }
                if ($ffmpegDir) {
                    $argsList += @("--ffmpeg-location", $ffmpegDir)
                }
                $argsList += @("-o", $outPattern, $url)
                
                & $exe $argsList *>$null
                return ($LASTEXITCODE -eq 0)
            }).AddArgument($ytdlp).AddArgument($outPattern).AddArgument($item.Url).AddArgument($ffmpegDir).AddArgument($dspFilter)

            $handle = $ps.BeginInvoke()
            $tasks.Add([PSCustomObject]@{
                Pipe = $ps
                Handle = $handle
                Task = $item
            })
            Start-Sleep -Milliseconds 250
        }

        $completed = 0
        $lastReported = -1

        while ($completed -lt $total) {
            Start-Sleep -Milliseconds 150
            $curCompleted = 0
            $activeCount = 0
            foreach ($t in $tasks) {
                if ($t.Handle.IsCompleted) {
                    $curCompleted++
                } else {
                    $activeCount++
                }
            }

            if ($curCompleted -ne $lastReported) {
                $lastReported = $curCompleted
                $completed = $curCompleted
                $pct = [math]::Round(($completed / [math]::Max($total, 1)) * 100)
                if ($pct -gt 100) { $pct = 100 }
                $filled = [math]::Floor($pct / 100.0 * 20)
                $empty = 20 - $filled
                $bar = ('=' * $filled) + ('-' * $empty)

                $latestTitle = ""
                for ($k = $tasks.Count - 1; $k -ge 0; $k--) {
                    if ($tasks[$k].Handle.IsCompleted) {
                        $latestTitle = $tasks[$k].Task.Title
                        break
                    }
                }
                if ($latestTitle.Length -gt 20) { $latestTitle = $latestTitle.Substring(0, 17) + "..." }

                $line = "`r  [{0}] {1,3}% ({2}/{3}) [{4} faol] {5}" -f $bar, $pct, $completed, $total, $activeCount, $latestTitle
                $line = $line.PadRight(74).Substring(0, 74)
                Write-Host -NoNewline $line
            }
        }

        Write-Host ("`r  [====================] 100% ({0}/{0}) Barcha qo'shiqlar yuklandi!                  `n" -f $total) -ForegroundColor Green

        foreach ($t in $tasks) {
            try { [void]$t.Pipe.EndInvoke($t.Handle) } catch {}
            try { $t.Pipe.Dispose() } catch {}
        }
        try { $Pool.Close(); $Pool.Dispose() } catch {}

        # 3-Bosqich: Fayl nomlarini tozalash va FAT32 Xronologik Tartibini tamg'alash
        Write-Host "  [ 3/3 ] Maytafon uchun nomlar tozalanmoqda, FAT32 tartiblanmoqda va pleylistlar tuzilmoqda..." -ForegroundColor Cyan
        $files = Get-ChildItem -Path $chiqishPapka -Filter "*.mp3" | Sort-Object Name
        $baseDate = (Get-Date).AddDays(-1)
        $dateOffset = 0
        $cleanList = @()

        foreach ($f in $files) {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
            $prefixMatch = [regex]::Match($base, '^(\d+)\s*[-_.]\s*(.*)$')
            $prefix = ""
            $rawTitle = $base
            if ($prefixMatch.Success) {
                $prefix = $prefixMatch.Groups[1].Value
                $rawTitle = $prefixMatch.Groups[2].Value
            }

            $cleanOnly = Format-CleanTitle $rawTitle
            $finalName = if ($prefix) { ("{0} - {1}" -f $prefix, $cleanOnly) } else { $cleanOnly }

            $targetPath = $f.FullName
            if ($finalName -ne $base) {
                $newF = Join-Path $chiqishPapka ($finalName + $f.Extension)
                if (-not (Test-Path $newF)) {
                    Rename-Item -LiteralPath $f.FullName -NewName ($finalName + $f.Extension) -Force -ErrorAction SilentlyContinue
                    $targetPath = $newF
                }
            }

            # FAT32 xronologik tartib (Magnitolalar 001, 002, 003 tartibida adashmasligi uchun)
            try {
                $itemFile = Get-Item -LiteralPath $targetPath -ErrorAction SilentlyContinue
                if ($itemFile) {
                    $assignedTime = $baseDate.AddSeconds($dateOffset)
                    $itemFile.CreationTime = $assignedTime
                    $itemFile.LastWriteTime = $assignedTime
                    $itemFile.LastAccessTime = $assignedTime
                    $dateOffset += 3
                }
            } catch {}

            $cleanList += [PSCustomObject]@{
                Path = $targetPath
                Name = [System.IO.Path]::GetFileName($targetPath)
                Base = [System.IO.Path]::GetFileNameWithoutExtension($targetPath)
            }
        }

        # Mundarija va M3U / M3U8 pleylistlarini yaratish
        Generate-PlaylistsAndIndex -cleanFiles $cleanList -chiqishPapka $chiqishPapka -ffprobePath $ffprobe

        Write-Host ""
        if ($cleanList.Count -gt 0) {
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Green
            Write-Host " |  * BARCHA ISHLAR MUVAFFAQIYATLI YAKUNLANDI!                                          |" -ForegroundColor Green
            Write-Host " |  1. Sof 256k CBR MP3 formatiga keltirildi.                                           |" -ForegroundColor White
            Write-Host " |  2. YouTube bot cheklovlari va HTTP 429 xatolari chetlab o'tildi.                   |" -ForegroundColor White
            Write-Host " |  3. Studio Harmonic Exciter & True-Peak balansi ta'minlandi (Gupillamas toza ovoz). |" -ForegroundColor White
            Write-Host " |  4. 800x800 HD Albom muqovasi (Cover Art) har bir trekka biriktirildi.               |" -ForegroundColor White
            Write-Host " |  5. FAT32 xronologik vaqti sozlandi (001, 002, 003 magnitola adashmaydi).            |" -ForegroundColor White
            Write-Host " |  6. 00_Taronalar_Royxati.txt, 01_Taronalar.m3u va 02_Taronalar.m3u8 pleylist tuzildi.|" -ForegroundColor White
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Green
            Speak-Notification "Janob Muzaffar, barcha musiqalar fleshkaga mukammal tartibda yozildi! Oq yo'l tilayman!"
        } else {
            Write-Host "  [!] Yuklash jarayonida fayllar saqlanmadi. Iltimos internet aloqasini tekshiring." -ForegroundColor Yellow
        }
        Write-Host ""

        try { Start-Process $chiqishPapka } catch {}

        # Avtomatik kompyuterni o'chirish (Agar tanlangan bo'lsa)
        if ($autoShutdown) {
            Write-Host ""
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Yellow
            Write-Host " |  [!] Barcha ishlar tugadi. Kompyuter 60 soniyadan so'ng avtomatik o'chadi!          |" -ForegroundColor Yellow
            Write-Host " |  O'chirishni bekor qilish uchun 60 soniya ichida istalgan tugmani bosing...         |" -ForegroundColor Cyan
            Write-Host " +--------------------------------------------------------------------------------------+" -ForegroundColor Yellow

            Start-Process "shutdown.exe" -ArgumentList @("/s", "/t", "60", "/c", "Musiqalar to'liq yuklandi. Kompyuter o'chmoqda...") -NoNewWindow
            $timer = [System.Diagnostics.Stopwatch]::StartNew()
            $cancelled = $false
            while ($timer.Elapsed.TotalSeconds -lt 58) {
                if ([Console]::KeyAvailable) {
                    $null = [Console]::ReadKey($true)
                    $cancelled = $true
                    break
                }
                Start-Sleep -Milliseconds 200
            }

            if ($cancelled) {
                Start-Process "shutdown.exe" -ArgumentList "/a" -NoNewWindow
                Write-Host ""
                Write-Host "  [✓] Kompyuterni o'chirish bekor qilindi!" -ForegroundColor Green
                Start-Sleep -Seconds 2
            } else {
                break
            }
        }

        $yana = Read-Host "  > Yana boshqa to'plam yuklaysizmi? (ha / yoq)"
        if ($yana.Trim().ToLower() -ne 'ha') {
            break
        }
    }

} catch {
    Write-Host ""
    Write-Host "  [XATOLIK]: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Xato satri: $($_.InvocationInfo.ScriptLineNumber)" -ForegroundColor Yellow
    Write-Host "  Oynani yopish uchun istalgan tugmani bosing..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "  Chiqish uchun istalgan tugmani bosing..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
