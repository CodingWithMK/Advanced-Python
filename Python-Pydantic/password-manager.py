from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, AfterValidator
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import StringConstraints
from typing import Optional, Annotated
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

    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

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


class PasswordEntry(BaseModel):
    website: Annotated[str, StringConstraints(strip_whitespace=True)]
    email: EmailStr
    password: str = Field(min_length=12)
    username: Annotated[str, StringConstraints(strip_whitespace=True)] = ""

    model_config = {
        "frozen": True
    }
    
    # Create an entry using the generate_password() function.
    @classmethod
    def create_entry(cls, website: str, email: str, username: str=""):
        generated_password = generate_password()
        
        return cls(
            website=website,
            email=email,
            password=generated_password,
            username=username
        )
    
@dataclass
class VaultManager:
    master_password: str
    salt: bytes

    # Initialization for cipher features after main initialization
    def __post_init__(self):
        key = derive_key(self.master_password, self.salt)
        self.cipher = Fernet(key)

    def encrypt_data(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_bytes: bytes) -> str:
        return self.cipher.decrypt(encrypted_bytes).decode()
    
@dataclass
class DatabaseManager:
    db_path: Path
    vault: VaultManager

    def save_password_entry(
        self,
        entry: PasswordEntry):
        """Encrypts an Pydantic object and saves it to the database."""
        enc_mail = self.vault.encrypt_data(entry.email)
        enc_pw = self.vault.encrypt_data(entry.password)
        enc_user = self.vault.encrypt_data(entry.username)

        query = """
        INSERT INTO passwords (website, email, password, username) VALUES (?, ?, ?, ?);
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (entry.website, enc_mail, enc_pw, enc_user))
        print(f"✅ Entry for {entry.website} saved successfully.")

    def get_entry(self, website: str):
        """Searches, decryptes and validates an entry."""
        query = "SELECT email, password, username FROM passwords WHERE website = ?;"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (website,))
            row = cursor.fetchone() # Fetches first match

        if not row:
            raise ValueError(f"❌ No entry found for '{website}'.")
        
        # Decryption
        # row[0] = email, row[1] = password, row[2] = username
        dec_email = self.vault.decrypt_data(row[0])
        dec_pw = self.vault.decrypt_data(row[1])
        dec_user = self.vault.decrypt_data(row[2])

        # Fit entry back to data validation
        return PasswordEntry(
            website=website,
            email=dec_email,
            password=dec_pw,
            username=dec_user
        )


if __name__ == "__main__":
    # print(PasswordEntry.create_entry(website="Google", email="jack123@gmail.com"))
    init_db()
    master_pw = "MyUltraSecureMasterPassword123!"
    salt = load_or_create_salt()

    vault = VaultManager(master_pw, salt)
    db_manager = DatabaseManager(get_db_path(), vault)

    new_entry = PasswordEntry.create_entry(website="Netflix", email="user123@web.com")

    db_manager.save_password_entry(new_entry)

    try:
        retrieved = db_manager.get_entry("Netflix")
        print(f"Found password: {retrieved.password}")
    except ValueError as e:
        print(e)