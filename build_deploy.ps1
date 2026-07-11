$DeployFile = "deploy.zip"

if (Test-Path $DeployFile) {
    Remove-Item $DeployFile
}

Write-Host "Membuat file zip untuk deploy..."

# Daftar folder dan file yang akan dipaketkan
$FilesToZip = @(
    "api",
    "Laangke",
    "Lakonea",
    "Malalanda",
    "index.html",
    "desa-cantik-buton-utara-keluarga.html"
)

# Mengecek keberadaan file/folder dan memasukannya ke ZIP
$ValidPaths = @()
foreach ($Item in $FilesToZip) {
    if (Test-Path $Item) {
        $ValidPaths += $Item
    } else {
        Write-Host "Peringatan: $Item tidak ditemukan, dilewati." -ForegroundColor Yellow
    }
}

if ($ValidPaths.Count -gt 0) {
    # Menggunakan tar (bawaan Windows 10/11) karena jauh lebih cepat dan tidak gampang hang dibanding Compress-Archive
    tar -a -c -f $DeployFile $ValidPaths
    Write-Host "Selesai! File $DeployFile telah berhasil dibuat." -ForegroundColor Green
    Write-Host "Silakan upload file ini ke cPanel (File Manager) -> public_html Rumahweb Anda, lalu extract."
} else {
    Write-Host "Error: Tidak ada file valid yang ditemukan untuk di-zip." -ForegroundColor Red
}
