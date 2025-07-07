from typing import Optional
from datetime import datetime

class User:
    def __init__(self, id: str, email: str, password_hash: str, first_name: str, last_name: str, role: str = 'user', organization_id: Optional[str] = None, last_login: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.organization_id = organization_id
        self.last_login = last_login
