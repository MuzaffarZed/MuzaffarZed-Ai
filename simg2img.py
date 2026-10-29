import struct
import sys
import time
import os

def simg2img(in_path, out_path):
    print(f"Opening sparse image: {in_path}")
    t0 = time.time()
    with open(in_path, "rb") as f_in, open(out_path, "wb") as f_out:
        header = f_in.read(28)
        magic, major, minor, file_hdr_sz, chunk_hdr_sz, blk_sz, total_blks, total_chunks, crc = struct.unpack("<I4H4I", header)
        if magic != 0xED26FF3A:
            raise ValueError(f"Invalid sparse magic: {hex(magic)}")
        
        if file_hdr_sz > 28:
            f_in.seek(file_hdr_sz - 28, os.SEEK_CUR)
            
        print(f"Total blocks: {total_blks}, Block size: {blk_sz}, Chunks: {total_chunks}")
        out_bytes = 0

        for chunk_idx in range(total_chunks):
            chunk_header = f_in.read(12)
            if len(chunk_header) < 12:
                break
            chunk_type, reserved, chunk_sz, total_sz = struct.unpack("<2H2I", chunk_header)
            if chunk_hdr_sz > 12:
                f_in.seek(chunk_hdr_sz - 12, os.SEEK_CUR)
                
            chunk_bytes = chunk_sz * blk_sz

            if chunk_type == 0xCAC1: # RAW
                # Read chunk_bytes directly and write
                remaining = chunk_bytes
                while remaining > 0:
                    read_len = min(remaining, 16 * 1024 * 1024)
                    buf = f_in.read(read_len)
                    if not buf:
                        raise EOFError("Unexpected EOF reading raw chunk")
                    f_out.write(buf)
                    remaining -= len(buf)
                out_bytes += chunk_bytes
            elif chunk_type == 0xCAC2: # FILL
                fill_val = f_in.read(4)
                # repeat fill_val
                pattern = fill_val * (blk_sz // 4)
                # write in 4MB blocks
                batch = pattern * (min(chunk_sz, 1024))
                left_chunks = chunk_sz
                while left_chunks > 0:
                    cnt = min(left_chunks, 1024)
                    f_out.write(pattern * cnt)
                    left_chunks -= cnt
                out_bytes += chunk_bytes
            elif chunk_type == 0xCAC3: # DONT_CARE
                # Seek or write zeros
                # To ensure valid non-sparse file on Windows, write zero blocks
                zero_buf = b"\x00" * min(chunk_bytes, 16 * 1024 * 1024)
                remaining = chunk_bytes
                while remaining > 0:
                    write_len = min(remaining, len(zero_buf))
                    f_out.write(zero_buf[:write_len])
                    remaining -= write_len
                out_bytes += chunk_bytes
            elif chunk_type == 0xCAC4: # CRC32
                f_in.read(4)
            else:
                raise ValueError(f"Unknown chunk type: {hex(chunk_type)}")
                
            if (chunk_idx + 1) % 10 == 0 or chunk_idx == total_chunks - 1:
                print(f"Processed chunk {chunk_idx + 1}/{total_chunks} ({out_bytes / (1024*1024):.1f} MB)...")

    print(f"Extraction completed in {time.time()-t0:.2f}s! Total: {out_bytes / (1024*1024):.2f} MB")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: simg2img.py <input.simg> <output.raw>")
    else:
        simg2img(sys.argv[1], sys.argv[2])
