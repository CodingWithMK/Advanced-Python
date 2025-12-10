from dataclasses import dataclass
import string
import secrets

ascii = string.ascii_letters + string.digits + string.punctuation

def generate_password(length: int = 12) -> str:
    generated = list()
    for char in range(length):
        generate = secrets.choice(ascii)
        generated.append(generate)
    generated_pw = "".join(generated)
    
    return generated_pw

print(generate_password())

# @dataclass
# class PasswordEntry:
#     website: str
#     email: str
#     password: str
#     username: str = ""
