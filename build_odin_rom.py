import os
import sys
import urllib.request
import lzma
import hashlib
import tarfile
import shutil
import lz4.frame

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORK_DIR = r"D:\T295_Custom_ROM"
GSI_URL = "https://github.com/ponces/treble_build_pe/releases/download/v2023.09.14/PixelExperience_arm64-ab-slim-13.0-20230914-UNOFFICIAL.img.xz"
XZ_FILE = os.path.join(WORK_DIR, "system.img.xz")
RAW_IMG = os.path.join(WORK_DIR, "system.img")
LZ4_FILE = os.path.join(WORK_DIR, "system.img.ext4.lz4")
VBMETA_SRC = r"C:\Users\MuzaffarZed\ai_workspace\vbmeta.img.lz4"
VBMETA_DST = os.path.join(WORK_DIR, "vbmeta.img.lz4")
TAR_FILE = os.path.join(WORK_DIR, "AP_PixelExperience_GApps_T295.tar")
TAR_MD5_FILE = os.path.join(WORK_DIR, "AP_PixelExperience_GApps_T295.tar.md5")

def download_with_progress(url, dest_path):
    print(f"[*] Starting download from: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out_file:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        last_percent = -1
        chunk_size = 1024 * 1024  # 1MB
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            percent = int(downloaded * 100 / total) if total else 0
            if percent != last_percent and percent % 10 == 0:
                print(f"    [Progress] Downloaded: {percent}% ({downloaded // (1024*1024)}MB / {total // (1024*1024)}MB)")
                last_percent = percent
    print("[+] Download complete!")

def decompress_xz(src_xz, dst_img):
    print(f"[*] Decompressing XZ archive to raw system image: {dst_img}")
    with lzma.open(src_xz, "rb") as f_in, open(dst_img, "wb") as f_out:
        total_decomp = 0
        chunk_size = 4 * 1024 * 1024  # 4MB
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            f_out.write(chunk)
            total_decomp += len(chunk)
            if (total_decomp // (1024 * 1024)) % 500 == 0:
                print(f"    [Progress] Decompressed {total_decomp // (1024 * 1024)}MB...")
    print(f"[+] Decompression complete! Raw image size: {os.path.getsize(dst_img) // (1024*1024)}MB")

def compress_to_samsung_lz4(src_img, dst_lz4):
    print(f"[*] Compressing raw image to Samsung Odin LZ4 format: {dst_lz4}")
    total_size = os.path.getsize(src_img)
    processed = 0
    last_p = -1
    
    with open(src_img, "rb") as f_in, open(dst_lz4, "wb") as f_out:
        # Create LZ4 frame with 4MB block size matching Samsung Odin standards
        with lz4.frame.open(f_out, mode="wb", block_size=lz4.frame.BLOCKSIZE_MAX4MB, compression_level=1) as lz4_out:
            chunk_size = 4 * 1024 * 1024
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                lz4_out.write(chunk)
                processed += len(chunk)
                p = int(processed * 100 / total_size)
                if p != last_p and p % 10 == 0:
                    print(f"    [Progress] LZ4 Compression: {p}% ({processed // (1024*1024)}MB / {total_size // (1024*1024)}MB)")
                    last_p = p
    print(f"[+] LZ4 Compression complete! Compressed size: {os.path.getsize(dst_lz4) // (1024*1024)}MB")

def build_odin_tar_md5():
    print(f"[*] Packing Odin TAR package: {TAR_FILE}")
    shutil.copy(VBMETA_SRC, VBMETA_DST)
    
    with tarfile.open(TAR_FILE, "w") as tar:
        # 1. system.img.ext4.lz4
        print("    [+] Adding system.img.ext4.lz4 to tar...")
        tar.add(LZ4_FILE, arcname="system.img.ext4.lz4")
        # 2. vbmeta.img.lz4
        print("    [+] Adding vbmeta.img.lz4 to tar...")
        tar.add(VBMETA_DST, arcname="vbmeta.img.lz4")
        
    print("[*] Calculating MD5 checksum of the TAR package...")
    md5 = hashlib.md5()
    with open(TAR_FILE, "rb") as f:
        while chunk := f.read(4 * 1024 * 1024):
            md5.update(chunk)
    hash_str = md5.hexdigest()
    print(f"    [+] MD5: {hash_str}")
    
    tar_name = os.path.basename(TAR_FILE)
    md5_line = f"{hash_str}  {tar_name}\n".encode("ascii")
    
    # Append MD5 to create .tar.md5
    with open(TAR_FILE, "ab") as f:
        f.write(md5_line)
        
    if os.path.exists(TAR_MD5_FILE):
        os.remove(TAR_MD5_FILE)
    os.rename(TAR_FILE, TAR_MD5_FILE)
    print(f"[SUCCESS] Final Odin Package Created: {TAR_MD5_FILE}")
    print(f"          Final Size: {os.path.getsize(TAR_MD5_FILE) // (1024*1024)}MB")

def main():
    print("================================================================")
    print("SAMSUNG SM-T295 PIXEL EXPERIENCE (GAPPS) ODIN ROM BUILDER")
    print("================================================================")
    os.makedirs(WORK_DIR, exist_ok=True)
    
    if not os.path.exists(XZ_FILE):
        download_with_progress(GSI_URL, XZ_FILE)
    else:
        print(f"[*] Found existing archive: {XZ_FILE}")
        
    if not os.path.exists(RAW_IMG):
        decompress_xz(XZ_FILE, RAW_IMG)
    else:
        print(f"[*] Found existing raw image: {RAW_IMG}")
        
    if not os.path.exists(LZ4_FILE):
        compress_to_samsung_lz4(RAW_IMG, LZ4_FILE)
    else:
        print(f"[*] Found existing LZ4 compressed image: {LZ4_FILE}")
        
    build_odin_tar_md5()
    print("\n[ALL TASKS COMPLETED SUCCESSFULLY]")

if __name__ == "__main__":
    main()
