import lz4.frame
import os
import time
import sys

def compress_file(in_path, out_path):
    print(f"Compressing {in_path} to LZ4: {out_path}...")
    t0 = time.time()
    total_in = os.path.getsize(in_path)
    
    # Use Samsung standard LZ4 frame flags: 1MB block size, unlinked blocks, content checksum, content size (0x6c 0x60)
    with open(in_path, "rb") as f_in, lz4.frame.open(out_path, mode="wb", block_size=lz4.frame.BLOCKSIZE_MAX1MB, block_linked=False, content_checksum=True, source_size=total_in) as f_out:
        read_total = 0
        while True:
            chunk = f_in.read(16 * 1024 * 1024)
            if not chunk:
                break
            f_out.write(chunk)
            read_total += len(chunk)
            if read_total % (256 * 1024 * 1024) == 0:
                print(f"Compressed {read_total / (1024*1024):.0f} / {total_in / (1024*1024):.0f} MB...")
                
    out_size = os.path.getsize(out_path)
    print(f"Compression completed in {time.time()-t0:.2f}s! Final LZ4 size: {out_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compress_lz4.py <input> <output.lz4>")
    else:
        compress_file(sys.argv[1], sys.argv[2])
