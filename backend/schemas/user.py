from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    organization_id: Optional[str]

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class UserRoleUpdate(BaseModel):
    user_id: str
    role: str

class UserInvite(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"
