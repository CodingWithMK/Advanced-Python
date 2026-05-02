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
        "<8MB": {},
        "<16MB": {},
        ">16MB": {}
    }
    file_status: Literal["scanning", "hashing", "completed", "error"]
    duplicates: dict
    potential_duplicates: tuple[Path, ...]
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
            category = "<8MB" if file_size_mb < 8 else "<16MB" if file_size_mb < 16 else ">16MB"

            # Call into inner dictionary branch
            inner_dict = self.files_by_size[category]

            inner_dict.setdefault(category, []).append(file)

            return self.files_by_size

    

        
        


    



