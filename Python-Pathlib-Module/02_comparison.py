# ============ COMPARISON: OS MODULE VS. PATHLIB ============

# Find all png files in given directory and its sub-directories

# ----- os -----
import os
dir_path = "/home/user/documents"           # Windows Path: "C:\\Users\\username\\documents"

files = [
    os.path.join(dir_path, f) 
    for f in os.listdir(dir_path)
    if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(".png")
]

# ----- pathlib -----
from pathlib import Path

# Create a path object
dir_path = Path(dir_path)

# Find all text files inside a directory
files = list(dir_path.glob("*.png"))