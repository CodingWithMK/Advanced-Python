from pathlib import Path

# ============ Listing Directories ============
"""
The iterdir() method allows you to iterate over all the files and 
subdirectories in a folder. It is particularly useful for processing 
all files in a directory or performing operations on each entry.
"""

cwd = Path.cwd()

for entry in cwd.iterdir():
    # Process the entry here
    # print(entry)
    pass



# ============ The is_dir() method ============
"""
The is_dir() method returns True if the path points to a directory, 
False otherwise.
"""

for entry in cwd.iterdir():
    if entry.is_dir():       # Checks if path is a directory
        print(entry.name)



# ============ The is_file() method ============
"""
The .is_file() method returns True if the path points to a file, 
False otherwise.
"""

for entry in cwd.iterdir():
    if entry.is_file():       # Checks if path is a file
        print(entry.suffix)



# ============ The exists() method ============
"""
The .exists() method check if a path exists. This is useful because 
Path objects can represent files and directories that may or may not 
actually be present in the file system.
"""
home = Path.home()

home / "downloads" / "projects"

image_file = home / "downloads" / "midjourney.png"
image_file.root

image_file.exists()



# ============ CREATING AND DELETING PATHS =============

# ============ The mkdir() method =============

"""
The mkdir() method creates a new directory at the specified path. By default, 
it creates the directory in the current working directory.
"""

data_dir = Path("new_data_dir")

# Create the directory 'new_data_dir' in the current working directory
data_dir.mkdir()



# ============ The mkdir(parents=True) method ============
"""
The mkdir(parents=True) method is particularly useful when you want to create 
a directory structure where some parent directories might not exist. Setting 
parents=True ensures that all necessary parent directories are created along the way.
"""

sub_dir = Path("data/nested/subdirectory")

# Create 'data/nested/subdirectory', even if 'data' or 'nested' do not exist
sub_dir.mkdir(parents=True)

"""
NOTE: Keep in mind that mkdir() raises an exception if a directory with the same name 
already exists.
"""



# ============ The unlink() method ============
"""
The unlink() method permanently deletes a file represented by the Path object. It is 
recommended to check if a file exists before running this method in order to avoid 
receiving an error.
"""


to_delete = Path("data/prices.csv")

if to_delete.exists():
    to_delete.unlink()
    print(f"Successfully deleted {to_delete.name}")
