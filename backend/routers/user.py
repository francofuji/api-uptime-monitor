from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from backend.schemas.user import (
    UserCreate, UserLogin, UserOut, UserUpdate, Token, PasswordChange, PasswordResetRequest, PasswordReset, UserRoleUpdate, UserInvite
)
from backend.repositories.user_repository import UserRepository
from backend.auth.password import hash_password, verify_password
from backend.auth.jwt import create_access_token, decode_access_token

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user = await UserRepository.find_by_id(payload["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await UserRepository.find_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = await UserRepository.create({
        **user.dict(),
        "password_hash": hash_password(user.password),
        "role": "user"
    })
    created = await UserRepository.find_by_id(user_id)
    return created

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await UserRepository.find_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.id, "role": db_user.role})
    await UserRepository.update_last_login(db_user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_me(updates: UserUpdate, current_user=Depends(get_current_user)):
    # Implement update logic in UserRepository
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/change-password")
async def change_password(data: PasswordChange, current_user=Depends(get_current_user)):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    # Implement password update in UserRepository
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/request-password-reset")
async def request_password_reset(data: PasswordResetRequest):
    # Send password reset email (placeholder)
    return {"message": "If the email exists, a reset link will be sent."}

@router.post("/reset-password")
async def reset_password(data: PasswordReset):
    # Implement password reset logic
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
async def list_users():
    # Implement list users in UserRepository
    raise HTTPException(status_code=501, detail="Not implemented")

@router.put("/role", dependencies=[Depends(admin_required)])
async def update_user_role(data: UserRoleUpdate):
    # Implement role update in UserRepository
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/invite", dependencies=[Depends(admin_required)])
async def invite_user(data: UserInvite):
    # Send invite email (placeholder)
    return {"message": f"Invite sent to {data.email}"}

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
async def delete_user(user_id: str):
    # Implement delete in UserRepository
    raise HTTPException(status_code=501, detail="Not implemented")
