import tarfile
import hashlib
import os
import time

BUILD_DIR = r"D:\T295_Studio_ROM_Build"
TAR_NAME = "AP_Muzaffar_Studio_OS_T295.tar"
TAR_PATH = os.path.join(BUILD_DIR, TAR_NAME)
TAR_MD5_PATH = os.path.join(BUILD_DIR, "AP_Muzaffar_Studio_OS_T295.tar.md5")

PARTITIONS = [
    "boot.img.lz4",
    "dtbo.img.lz4",
    "recovery.img.lz4",
    "system.img.ext4.lz4",
    "vendor.img.ext4.lz4",
    "vbmeta.img.lz4"
]

def build_ap():
    print(f"Creating Odin archive: {TAR_PATH}...")
    t0 = time.time()
    
    if os.path.exists(TAR_PATH):
        os.remove(TAR_PATH)
    if os.path.exists(TAR_MD5_PATH):
        os.remove(TAR_MD5_PATH)

    with tarfile.open(TAR_PATH, "w", format=tarfile.GNU_FORMAT) as t:
        for p in PARTITIONS:
            file_path = os.path.join(BUILD_DIR, p)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing partition file: {file_path}")
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"Adding {p} ({size_mb:.2f} MB)...")
            t.add(file_path, arcname=p)
            
    print(f"TAR creation completed in {time.time()-t0:.2f}s! Calculating MD5 checksum...")
    t1 = time.time()
    md5 = hashlib.md5()
    with open(TAR_PATH, "rb") as f:
        while True:
            chunk = f.read(16 * 1024 * 1024)
            if not chunk:
                break
            md5.update(chunk)
            
    hex_digest = md5.hexdigest()
    print(f"Calculated MD5: {hex_digest} in {time.time()-t1:.2f}s")
    
    # Append Odin MD5 trailer
    trailer = f"{hex_digest}  {TAR_NAME}\n".encode("ascii")
    with open(TAR_PATH, "ab") as f:
        f.write(trailer)
        
    os.rename(TAR_PATH, TAR_MD5_PATH)
    final_size_mb = os.path.getsize(TAR_MD5_PATH) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"SUCCESS! ODIN FLASHABLE ROM CREATED:")
    print(f"Path: {TAR_MD5_PATH}")
    print(f"Size: {final_size_mb:.2f} MB")
    print(f"MD5:  {hex_digest}")
    print(f"=======================================================")

if __name__ == "__main__":
    build_ap()
