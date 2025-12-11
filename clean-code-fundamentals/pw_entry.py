from dataclasses import dataclass
import string
import secrets

alphabet = string.ascii_letters + string.digits + string.punctuation

def generate_password(length: int = 12) -> str:
    generated = [secrets.choice(alphabet) for _ in range(length)]
    generated_pw = "".join(generated)
    
    return generated_pw

print(generate_password())

# @dataclass
# class PasswordEntry:
#     website: str
#     email: str
#     password: str
#     username: str = ""
