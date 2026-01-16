from dataclasses import dataclass
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import string
import secrets
import sqlite3

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Master-Key derivation using the Key Derivation Function (KDF)

    Input: str -> master password, bytes -> salt

    Returns: bytes -> URL safe base64 encoded key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000
    )

def load_or_create_salt() -> bytes:
    """
    Loading or creating a 16 bytes salt for Master-Key verification.
    
    :return: Salt (16 bytes)
    :rtype: Path
    """
    home = Path.home()
    salt_path = home / '.my_password_manager' / 'salt.bin'
    if not salt_path.exists():
        salt = secrets.token_bytes(16)
        with open(salt_path, 'wb') as file:
            file.write(salt)
    else:
        with open(salt_path, 'rb') as file:
            salt = file.read()
        
    return salt
    

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

def init_db():
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS passwords (
                         website TEXT,
                         email BLOB,
                         password BLOB,
                         username BLOB
                     );
                     """)


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