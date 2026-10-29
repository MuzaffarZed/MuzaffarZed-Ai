import lz4.frame
import os

input_path = r'C:\Users\MuzaffarZed\Desktop\boot.img.lz4'
output_path = r'C:\Users\MuzaffarZed\Desktop\boot.img'

with open(input_path, 'rb') as f_in:
    compressed_data = f_in.read()

# LZ4 framed or legacy
try:
    decompressed = lz4.frame.decompress(compressed_data)
except Exception:
    import lz4.block
    decompressed = lz4.block.decompress(compressed_data)

with open(output_path, 'wb') as f_out:
    f_out.write(decompressed)

print(f"Decompressed boot.img size: {os.path.getsize(output_path)} bytes")
