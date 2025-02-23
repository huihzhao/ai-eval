from dataclasses import dataclass
from typing import Dict
import hashlib
import os

@dataclass
class User:
    username: str
    password: str  # In production, this should be hashed

# Global dictionary to store users (replace with database in production)
users: Dict[str, User] = {}
