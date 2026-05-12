import argparse
import os
import shutil
import zipfile

# Dictionary mapping hex signatures to file extensions
# These "magic numbers" allow us to identify files without relying on extensions.
MAGIC_NUMBERS = {
    b'\x50\x4B\x03\x04': '.zip',
    b'\x25\x50\x44\x46': '.pdf',
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': '.png',
    b'\xFF\xD8\xFF': '.jpg',
    b'\x47\x49\x46\x38': '.gif',
    b'\x1F\x8B\x08': '.gz',
    b'\x52\x61\x72\x21\x1A\x07\x00': '.rar',
    b'\x52\x61\x72\x21\x1A\x07\x01\x00': '.rar',
}

def identify_extension(file_path):
    """
    Reads the first 8 bytes of a file and returns the likely extension
    based on known magic numbers.
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
        for sig, ext_name in MAGIC_NUMBERS.items():
            if header.startswith(sig):
                return ext_name
    except Exception as e:
        print(f"[ERROR] Reading {file_path}: {e}")
    return None

def process_file(file_path, output_dir=None):
    """
    Identifies, renames, and optionally moves a single file.
    If the file is a ZIP, it also extracts it.
    """
    if not os.path.isfile(file_path):
        return

    detected_ext = identify_extension(file_path)
    
    if not detected_ext:
        print(f"[SKIP]  Could not identify: {file_path}")
        return

    print(f"[MATCH] {detected_ext.upper()} detected: {file_path}")
    
    base_name = os.path.basename(file_path)
    name_without_ext, _ = os.path.splitext(base_name)
    
    # Append the extension only if it's not already there
    if not base_name.lower().endswith(detected_ext):
        new_file_name = f"{base_name}{detected_ext}"
    else:
        new_file_name = base_name

    # Determine the destination folder
    target_dir = output_dir if output_dir else os.path.dirname(file_path)
    if target_dir == "":
        target_dir = "."
        
    os.makedirs(target_dir, exist_ok=True)
    new_file_path = os.path.join(target_dir, new_file_name)
    
    try:
        # Move and rename the file to its destination
        if os.path.abspath(file_path) != os.path.abspath(new_file_path):
            shutil.move(file_path, new_file_path)
            print(f"[MOVE]  {file_path} -> {new_file_path}")
        else:
            print(f"[READY] {new_file_path}")
            
        # If it's a zip file, extract it in the same target directory
        if detected_ext == '.zip':
            extract_dir = os.path.join(target_dir, f"{name_without_ext}_extracted")
            if not os.path.exists(extract_dir):
                print(f"[UNZIP] Extracting to: {extract_dir}")
                with zipfile.ZipFile(new_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            else:
                print(f"[SKIP]  Extraction directory already exists: {extract_dir}")
            
    except Exception as e:
        print(f"[ERROR] Processing {file_path}: {e}")

def process_path(path, output_dir=None):
    """
    Handles both single files and recursive directory traversal.
    """
    if os.path.isfile(path):
        process_file(path, output_dir)
    elif os.path.isdir(path):
        print(f"[SCAN]  Searching directory: {path}")
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path, output_dir)
    else:
        print(f"[ERROR] Path not found: {path}")

def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to resolve file types by magic numbers and extract archives."
    )
    parser.add_argument(
        "input_path", 
        help="The file or directory containing files to resolve."
    )
    parser.add_argument(
        "-o", "--output-dir", 
        help="Optional: The directory where resolved files and extracted contents will be placed.",
        default=None
    )
    
    args = parser.parse_args()
    process_path(args.input_path, args.output_dir)

if __name__ == "__main__":
    main()
