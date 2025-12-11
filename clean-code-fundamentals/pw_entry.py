from dataclasses import dataclass
import string
import secrets

@dataclass
class PasswordEntry:
    website: str
    email: str
    password: str
    username: str = ""

    def generate_password(length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        generated = [secrets.choice(alphabet) for _ in range(length)]
        generated_pw = "".join(generated)
        
        return generated_pw
    
    # TODO: Create an entry using the generate_password() function. -> Tip: create_entry(website: str, email: str, username: str = "") -> PasswordEntry
