import shutil

def main() -> None:
    # Copy a file
    shutil.copy("pyproject.toml", "backup_pyproject.toml")

    # Create a zip archive
    shutil.make_archive("pyproject_backup", "zip", ".")

if __name__ == "__main__":
    main()