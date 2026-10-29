import struct
import sys
import time
import os

BLOCK_SIZE = 4096
ZERO_BLOCK = b"\x00" * BLOCK_SIZE

def img2simg(raw_path, simg_path):
    print(f"Converting RAW image to Android Sparse Image: {raw_path}")
    t0 = time.time()
    
    file_size = os.path.getsize(raw_path)
    total_blocks = file_size // BLOCK_SIZE
    if file_size % BLOCK_SIZE != 0:
        total_blocks += 1
        
    print(f"Total size: {file_size / (1024*1024):.2f} MB, Total blocks: {total_blocks}")
    
    # We will do a single-pass or two-pass convert
    # Let's collect chunks:
    chunks = []
    
    with open(raw_path, "rb") as f_in:
        current_type = None # 0xCAC1 (RAW) or 0xCAC3 (DONT_CARE)
        current_len = 0
        
        blk_idx = 0
        while blk_idx < total_blocks:
            buf = f_in.read(BLOCK_SIZE)
            if not buf:
                break
            if len(buf) < BLOCK_SIZE:
                buf = buf.ljust(BLOCK_SIZE, b"\x00")
                
            is_zero = (buf == ZERO_BLOCK)
            chunk_type = 0xCAC3 if is_zero else 0xCAC1
            
            if current_type is None:
                current_type = chunk_type
                current_len = 1
            elif current_type == chunk_type:
                # Max chunk size is 65535 blocks
                if current_len >= 65535:
                    chunks.append((current_type, current_len))
                    current_len = 1
                else:
                    current_len += 1
            else:
                chunks.append((current_type, current_len))
                current_type = chunk_type
                current_len = 1
                
            blk_idx += 1
            if blk_idx % 200000 == 0:
                print(f"Analyzed {blk_idx}/{total_blocks} blocks...")
                
        if current_type is not None:
            chunks.append((current_type, current_len))
            
    print(f"Identified {len(chunks)} chunks in total. Writing sparse file...")
    
    # Write sparse header
    with open(raw_path, "rb") as f_in, open(simg_path, "wb") as f_out:
        # header: magic, major, minor, file_hdr_sz, chunk_hdr_sz, blk_sz, total_blks, total_chunks, crc
        header = struct.pack(
            "<I4H4I",
            0xED26FF3A,
            1, 0,
            28, 12,
            BLOCK_SIZE,
            total_blocks,
            len(chunks),
            0
        )
        f_out.write(header)
        
        for idx, (c_type, c_len) in enumerate(chunks):
            # chunk header: chunk_type, reserved, chunk_sz, total_sz
            if c_type == 0xCAC1: # RAW
                total_sz = 12 + c_len * BLOCK_SIZE
                f_out.write(struct.pack("<2H2I", c_type, 0, c_len, total_sz))
                # Stream raw blocks from f_in
                rem = c_len * BLOCK_SIZE
                while rem > 0:
                    read_bytes = min(rem, 16 * 1024 * 1024)
                    b = f_in.read(read_bytes)
                    f_out.write(b)
                    rem -= len(b)
            elif c_type == 0xCAC3: # DONT_CARE
                total_sz = 12 # No payload
                f_out.write(struct.pack("<2H2I", c_type, 0, c_len, total_sz))
                # Seek f_in past zero blocks
                f_in.seek(c_len * BLOCK_SIZE, os.SEEK_CUR)
                
            if (idx + 1) % 100 == 0 or idx == len(chunks) - 1:
                print(f"Written chunk {idx + 1}/{len(chunks)}...")
                
    simg_size = os.path.getsize(simg_path)
    print(f"Sparse image created in {time.time()-t0:.2f}s! Output size: {simg_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: img2simg.py <raw_image> <sparse_image>")
    else:
        img2simg(sys.argv[1], sys.argv[2])
