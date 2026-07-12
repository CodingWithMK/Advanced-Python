from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass
import hashlib
import send2trash
import os

@dataclass
class DuplicateFinder:
    dir_path: Path
    chunk_size: int = 65536
    file_size: float
    files_by_size: dict[str, dict[int, list[Path]]] = {
        "<=8MB": {},
        "<=16MB": {},
        ">16MB": {}
    }
    file_status: Literal["scanning", "hashing", "completed", "error"]
    duplicates: dict
    potential_duplicates: list[tuple[Path, ...]]
    hash_algorithm: Literal["md5", "sha1", "sha256"]
    min_size: int = 2048
    scan_results: str
    ignored_extensions: set[str] = {}
    fast_scan: bool = False
    
    def __post_init__(self):
        self.ignored_extensions = {
            ".ini", ".DS_Store", ".log", ".tmp",".pyc", ".pyo", ".pyd", ".git", ".gitignore", ".svn", ".git", ".gitignore", ".svn",
            ".idea", ".vscode", ".project", ".ckpt", ".weights"
            }
        
        if self.fast_scan == True:
            self.chunk_size = 16384

            for entry in self.dir_path.iterdir():
                if entry.is_file():
                    with open(entry, "rb", buffering=self.chunk_size) as file:
                        hashlib.sha256(file)

    def scan(self) -> list[Path]:
        self.files = [file for file in self.dir_path.iterdir() if file.is_file() and file.stat().st_size >= 2048 and file.suffix not in self.ignored_extensions]

        return self.files
    
    def group_by_size(self) -> dict[str, dict[int, list[Path]]]:
        """
        Adds every file by their size in the exact size of bytes,
        and categorizes them by the matching size label.
        """
        for file in self.scan:
            file_size_bytes = file.stat().st_size
            file_size_mb = file_size_bytes / (1024 * 1024)

            # Determine category
            category = "<=8MB" if file_size_mb <= 8 else "<=16MB" if file_size_mb <= 16 else ">16MB"

            # Call into inner dictionary branch
            inner_dict = self.files_by_size[category]

            inner_dict.setdefault(file_size_bytes, []).append(file)

        return self.files_by_size
    
    def group_by_partial_hash(self) -> list[tuple[Path, ...]]:
        """
        Gets grouped files of file_by_size and scans first 64KB of every file.
        If first partial hash matches it returns them as a group for full hash
        scan.
        """
        partial_hash_groups = {}

        # iterating through categories
        for category, inner_dict in self.files_by_size.items():
            # iterating through exact bytesizes and the corresponding file list
            for byte_size, file_list in inner_dict.items():
                if len(file_list) < 2:
                    continue

                for file_path in file_list:
                    try:
                        hasher = hashlib.new(self.hash_algorithm)

                        with open(file_path, "rb") as file:
                            chunk = file.read(self.chunk_size)
                            hasher.update(chunk)

                        partial_hash = hasher.hexdigest()

                        # Grouping the file paths by their partial hashes
                        partial_hash_groups.setdefault(partial_hash, []).append(file_path)

                    except (PermissionError, OSError):
                        continue                        # skip compromised/blocked files
                
        # Filtering the groups of potential duplicates
        temp_list = []
        for p_hash, paths in partial_hash_groups.items():
                if len(paths) > 1:                          # if more than one file in partial hash then add to temp_list
                    temp_list.append(tuple(paths))

        self.potential_duplicates = temp_list

        return self.potential_duplicates
    
    def check_full_hash(self) -> list[Path]:
        """
        Gets potential duplicates and makes a full-hash on all potential duplicate
        pairs to ensure real duplicants before removing.
        """
        confirmed_duplicates = []

        for duplicate_group in self.potential_duplicates:
            group_hashes = {}

            for file_path in duplicate_group:
                try:
                    hasher = hashlib.new(self.hash_algorithm)

                    with open(file_path, "rb") as file:
                        # read file in 8KB chunks for memory efficiency
                        while chunk := file.read(8192):
                            hasher.update(chunk)
                    
                    full_hash = hasher.hexdigest()

                    group_hashes.setdefault(full_hash, []).append(file_path)

                except (PermissionError, OSError):
                    continue

            for file_hash, paths in group_hashes.items():
                if len(paths) > 1:
                    for duplicate_path in paths[1:]:
                        try:
                            send2trash.send2trash(duplicate_path)
                            confirmed_duplicates.append(duplicate_path)
                        except Exception:
                            continue

        return confirmed_duplicates
        
        # TODO: Iterate through every potential duplicate, check for duplicates by making a full hash.


    

        
        


    



