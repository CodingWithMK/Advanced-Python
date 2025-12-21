from dataclasses import dataclass
import string
import secrets

def generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    generated = [secrets.choice(alphabet) for _ in range(length)]
    generated_pw = "".join(generated)
    
    return generated_pw

@dataclass
class PasswordEntry:
    website: str
    email: str
    password: str
    username: str = ""
    
    # Create an entry using the generate_password() function.
    def create_entry(website: str, email: str, username: str=""):
        website = website
        email = email
        generated_password = generate_password()
        
        return website, email, generated_password, username
    
if __name__ == "__main__":
    print(PasswordEntry.create_entry(website="Google", email="jack123@gmail.com"))