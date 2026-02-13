# ========================================
# =     PYDANTIC AND DATACLASSES         =
# ========================================
from __future__ import annotations

# DATACLASSES - Password Hashing

from dataclasses import dataclass
import hashlib

@dataclass
class UserData:
    username: str
    nickname: str
    password_hash: str

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    

# PYDANTIC - Password Hashing

from pydantic import BaseModel, field_validator, ConfigDict

class UserDataPydanticValidator(BaseModel):
    username: str
    nickname: str
    pass_hash: str

    @field_validator("pass_hash", mode="before")
    @classmethod
    def hash_pass(cls, value:str) -> str:
        if not value or not isinstance(value, str):
            raise ValueError("Password must be a non-empty string!")
        
        return hashlib.sha256(value.encode()).hexdigest()


    model_config = ConfigDict(extra="forbid")


# PYDANTIC - Password Hashing (more advanced)

from pydantic import BeforeValidator, AfterValidator
from annotated_types import MinLen
from typing import Annotated

def _hash(v: str) -> str:
    """Hash password string to SHA-256"""
    return hashlib.sha256(v.encode()).hexdigest()

class UserDataPydanticTypes(BaseModel):
    username: str
    nickname: str
    pw_hash: Annotated[str, MinLen(8), AfterValidator(_hash)]
    model_config = ConfigDict(extra="forbid")



if __name__ == "__main__":
    # Dataclass Part
    print("===== Dataclass Example =====\n")
    password = "my_decret_password"
    password_hash = UserData.hash_password(password)

    user = UserData(
        username="JohnDoe",
        nickname="johnny",
        password_hash=password_hash
    )

    print(f"Username: {user.username}")
    print(f"Nickname: {user.nickname}")
    print(f"Password Hash: {user.password_hash}")
    print(f"\nNote: Password must be hashed manually before creating the instance.\n\n")
    

    # Pydantic Part
    print("===== Pydantic Example =====\n")
    user_pydantic = UserDataPydanticValidator(
        username="PaulWalker",
        nickname="Cop",
        pass_hash="my_secret_password"
    )

    print(f"Username: {user_pydantic.username}")
    print(f"Nickname: {user_pydantic.nickname}")
    print(f"Password Hash: {user_pydantic.pass_hash}")
    print(f"\nNote: Password was automatically hashed by the field_validator.\n\n")


    # More Advanced Pydantic Part
    print("===== More Advanced Pydantic Example =====\n")
    user_pydantical = UserDataPydanticTypes(
        username="MarkDJ",
        nickname="Marky",
        pw_hash="my_secret_password"
    )

    print(f"Username: {user_pydantical.username}")
    print(f"Nickname: {user_pydantical.nickname}")
    print(f"Password Hash: {user_pydantical.pw_hash}")
    print(f"\nNote: Password was validated (MinLen(8)) and automatically created.")

