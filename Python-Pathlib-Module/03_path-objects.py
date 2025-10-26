from pathlib import Path

# ============ Creating path objects from strings ============

file_path_str = "data/union_data.txt"

data_path = Path(file_path_str)



# ============ Creating path objects from other path objects ============

base_path = Path("/home/user")
data_dir = Path("data")

# Combining multiple paths
file_path = base_path / data_dir / "prices.csv"  
print(file_path)



# ============ Creating path objects fro the current working directory ============

cwd = Path.cwd()

print(cwd)



# ============ Creating path objects from the home working directory ============

home = Path.home()

home / "downloads" / "projects"


"""
NOTE: The Path class itself doesn't perform any file system operations 
such as path validation, creating directories or files. It is designed 
for representing and manipulating paths. To actually interact with the 
file system (checking existence, reading/writing files), we will have 
to use special methods of Path objects and for some advanced cases, get 
help from the os module.
"""