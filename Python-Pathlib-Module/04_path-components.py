from pathlib import Path

# ============ Working with the root directory ============

"""
The root is the topmost directory in a file system. In Unix-like systems, 
it is represented by a forward slash (/). In Windows, it is typically a 
drive letter followed by a colon, like C:.
"""
home = Path.home()

home / "downloads" / "projects"

image_file = home / "downloads" / "midjourney.png"
image_file.root



# ============ Working with the parent directory ============
"""
The parent contains the current file or directory. it is one level 
higher relative to the current directory or file.
"""
image_file.parent



# ============ Working with the file name ============
"""
This attribute returns the entire file name, 
including the extension, as a string.
"""

image_file.name



# ============ Working with the file suffix ============

"""
The suffix attribute returns the file extension, including the dot, 
as a string (or an empty string if there’s no extension).
"""

image_file.suffix


# ============ Working with the file stem ============
"""
The stem returns the file name without the extension. Working with 
the stem can be useful when converting files to different formats.
"""

image_file.stem

"""
NOTE: On a Mac, file paths are case-sensitive, so 
/Users/username/Documents and /users/username/documents would be different. 
"""



# ============ The pathlib parts attribute ============
"""
We can use the .parts attribute to split a Path object into its components.
"""

image_file.parts



# ============ The pathlib parents attribute ============
"""
The parents attribute, which returns a generator, turns these components 
into Path objects.
"""

list(image_file.parents)
