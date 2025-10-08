from pathlib import Path

# Create a Path object
path = Path("example_folder/example_file.txt")

# Check if the path exists
if path.exists():
    print("f{path} already exists!")
else:
    print(f"{path} does not exist! Generating path...")

# Get parts of the path
print("Name:", path.name)           # example_file.txt
print("Stem:", path.stem)           # example_file
print("Suffix:", path.suffix)       # .txt
print("Parent:", path.parent)       # example_folder

# Create directories
path.parent.mkdir(parents=True, exist_ok=True)

# Write to a file
path.write_text("Hello, Pathlib!")

# Read from a file
content = path.read_text()
print("File Content:", content)

# Iterate through files in a directory
for file in path.parent.iterdir():
    print("File/Folder:", file)

# Check if it is a file or directory
print("Is File?", path.is_file())
print("Is Directory?", path.is_dir())