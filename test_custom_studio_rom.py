import os
import tarfile
import hashlib
import pytest

ROM_PATH = r"D:\T295_Studio_ROM_Build\AP_Muzaffar_Studio_OS_T295.tar.md5"
REQUIRED_PARTITIONS = {
    "boot.img.lz4",
    "dtbo.img.lz4",
    "recovery.img.lz4",
    "system.img.ext4.lz4",
    "vendor.img.ext4.lz4",
    "vbmeta.img.lz4"
}

def test_rom_tar_md5_exists():
    """Verify AP_Muzaffar_Studio_OS_T295.tar.md5 exists and is properly sized."""
    assert os.path.exists(ROM_PATH), "Custom ROM file does not exist!"
    size_mb = os.path.getsize(ROM_PATH) / (1024 * 1024)
    assert size_mb > 2500, f"ROM size {size_mb} MB is too small!"

def test_rom_md5_checksum_verification():
    """Verify MD5 checksum in trailer matches the tar data exactly."""
    file_size = os.path.getsize(ROM_PATH)
    
    with open(ROM_PATH, "rb") as f:
        # Read trailer cleanly by splitting on null bytes
        f.seek(-100, 2)
        tail = f.read()
        trailer_bytes = [p for p in tail.split(b"\x00") if p][-1]
        trailer_len = len(trailer_bytes)
        tar_content_len = file_size - trailer_len
        
        parts = trailer_bytes.decode("ascii").strip().split()
        expected_md5 = parts[0]
        
        f.seek(0)
        hasher = hashlib.md5()
        remaining = tar_content_len
        while remaining > 0:
            chunk = f.read(min(remaining, 16 * 1024 * 1024))
            hasher.update(chunk)
            remaining -= len(chunk)
            
        actual_md5 = hasher.hexdigest()
        assert actual_md5 == expected_md5, f"MD5 mismatch! Expected {expected_md5}, got {actual_md5}"


def test_tar_partitions_integrity():
    """Verify all 6 critical partitions are present inside the Odin archive."""
    with open(ROM_PATH, "rb") as f:
        # Open as tar stream
        with tarfile.open(fileobj=f, mode="r") as t:
            names = set(t.getnames())
            for req in REQUIRED_PARTITIONS:
                assert req in names, f"Missing partition in AP archive: {req}"

def test_samsung_lz4_headers():
    """Verify all partitions have the official Samsung LZ4 header (0x6c with content size)."""
    with open(ROM_PATH, "rb") as f:
        with tarfile.open(fileobj=f, mode="r") as t:
            for member in t.getmembers():
                if member.name.endswith(".lz4"):
                    f_lz4 = t.extractfile(member)
                    hdr = f_lz4.read(6)
                    # Magic: 04 22 4d 18, FLG: 0x6c (Content Size + Independent Blocks + Checksum)
                    assert hdr[:4] == b"\x04\x22\x4d\x18", f"{member.name} has invalid LZ4 magic!"
                    assert hdr[4] == 0x6c, f"{member.name} has FLG {hex(hdr[4])}, expected 0x6c!"

def test_vbmeta_patched_avb_flags():
    """Verify vbmeta has AVB0 magic, authentic 7552 byte size, and flags == 3 (verity/verification disabled)."""
    import lz4.frame
    import struct
    with open(ROM_PATH, "rb") as f:
        with tarfile.open(fileobj=f, mode="r") as t:
            vb_data = t.extractfile("vbmeta.img.lz4").read()
            raw = lz4.frame.decompress(vb_data)
            assert len(raw) == 7552, f"vbmeta decompressed size {len(raw)} != 7552"
            assert raw[:4] == b"AVB0", "Invalid AVB magic"
            flags = struct.unpack(">I", raw[120:124])[0]
            assert flags == 3, f"Expected AVB flags 3, got {flags}"

