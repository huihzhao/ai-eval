from dataclasses import dataclass
from typing import Optional
import hashlib
import os

@dataclass
class User:
    username: str
    password_hash: str
    api_key: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.getenv('PASSWORD_SALT', 'default_salt')
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)

# Simple in-memory user store for demonstration
users = {}
