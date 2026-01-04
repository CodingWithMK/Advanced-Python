from dataclasses import dataclass
from pathlib import Path
import string
import secrets

def generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    generated = [secrets.choice(alphabet) for _ in range(length)]
    generated_pw = "".join(generated)
    
    return generated_pw

def get_db_path() -> Path:
    home = Path.home()
    folder_path = home / '.my_password_manager'
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path / "passwords.db"


@dataclass
class PasswordEntry:
    website: str
    email: str
    password: str
    username: str = ""
    
    # Create an entry using the generate_password() function.
    @classmethod
    def create_entry(cls, website: str, email: str, username: str=""):
        generated_password = generate_password()
        
        return cls(website, email, generated_password, username)
    
if __name__ == "__main__":
    # print(PasswordEntry.create_entry(website="Google", email="jack123@gmail.com"))
    print(get_db_path())