from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass
import hashlib
import os

@dataclass
class DuplicateFinder:
    dir_path: Path
    file_path: Path
    chunk_size: int = 65536
    file_size: float
    files_by_size: dict[int, list[Path]]
    file_status: Literal["scanning", "hashing", "completed", "error"]
    duplicates: dict
    potential_duplicates: tuple[Path, ...]
    hash_algorithm: Literal["md5", "sha1", "sha256"]
    min_size: int
    scan_results: str
    ingnored_extensions: set[str] = {}
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

    def _scan(self):
        pass

        
        


    



