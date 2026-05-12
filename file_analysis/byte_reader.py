import sys
import os

def read_file_signature(file_path, num_bytes=64):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, 'rb') as f:
            signature = f.read(num_bytes)
            
        hex_sig = signature.hex(' ', 1)
        print(f"File: {file_path}")
        print(f"First {len(signature)} bytes (hex):")
        print(hex_sig)
        print("\nRaw bytes representation:")
        print(signature)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python byte_reader.py <file_path>")
    else:
        read_file_signature(sys.argv[1])
