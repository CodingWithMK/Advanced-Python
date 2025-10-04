from pathlib import Path

def main() -> None:
    base = Path("Advanced-Python")
    file = base / "standard libraries" / "example.py"

    print("Python file path:", file)
    
    if file.exists():
        print("File size:", file.stat().st_size)
    else:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("print('Hello from pathlib module!')")

if __name__ == "__main__":
    main()
