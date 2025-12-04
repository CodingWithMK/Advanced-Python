from pathlib import Path

# ============ RELATIVE VS. ABSOLUTE PATHS ============
"""
Relative vs. absolute paths
We will start by understanding the differences between 
absolute and relative paths, as they come up often.

Relative paths
Relative paths specify the location of a file or directory 
relative to the current directory, hence the word relative. 
They are short and flexible within your project but can be 
confusing if you change the working directory.

For example, I have an images folder in my current working 
directory, which has the midjourney.png file.
"""

image = Path("images/test.png")

image



# ============ Absolute Paths =============

"""
Absolute paths specify the full location of a file or a directory 
from the root of the file system. They are independent 
of the current directory and offer a clear reference point 
for any user anywhere on the system.
"""

image_absolute = Path("/home/user/documents/Advanced-Python/images/test.png")

image_absolute



# ============ Resolve Method ============
"""
pathlib provides methods to convert relative paths to absolute with the 
resolve() method.
"""

relative_image = Path("images/test.png")

absolute_image = relative_image.resolve()

absolute_image

"""
We can also go the other way: If we have an absolute path, we can convert 
it to a relative path based on a reference directory.
"""

relative_path = Path.cwd()

absolute_image.relative_to(relative_path)



# ============ Globbing ============
"""
pathlib uses the built-in .glob() module to efficiently search for files 
matching a specific pattern in any directory. This module is very useful 
when processing files with similar names or extensions.
"""

dir_path = Path.cwd() / "images"

files = list(dir_path.glob("*.png"))

"""
The glob method works by accepting a pattern string containing wildcards 
as input and it returns a generator object that yields matching Path 
objects on demand:

*: Matches zero or more characters.

?: Matches any single character.

[]: Matches a range of characters enclosed within brackets 
(e.g., [a-z] matches any lowercase letter).

To illustrate, let’s try to find all Jupyter notebooks in my 
project directory.
"""

project_dir = Path.home() / "documents" / "Advanced-Python"

# Find all scripts
notebooks = project_dir.glob("*.ipynb")
scripts = project_dir.glob("*.py")

# Print how many found
print(f"Jupyter Notebooks: {len(list(notebooks))}\nPython Scripts: {len(list(scripts))}")

"""
The .glob() method didn't find any notebooks, which at first 
glance seems surprising because I have written over 150 articles. 
The reason is that .glob() only searches inside the given directory, 
not its subdirectories.

We can solve this by doing a recursive search, for which we need 
to use the rglob() method, which has similar syntax:
"""

notebooks = project_dir.rglob("*.ipynb")
scripts = project_dir.rglob("*.py")

print(len(list(notebooks)))
print(len(list(scripts)))