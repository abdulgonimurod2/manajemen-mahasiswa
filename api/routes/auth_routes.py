from fastapi import APIRouter
from pydantic import BaseModel
from api.models.mahasiswa import User
from api.models.exceptions import AuthenticationError

router = APIRouter()

admin_user = User("admin", "Admin123", "Administrator Sistem")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    if req.username == admin_user._username and admin_user.check_password(req.password):
        return {"message": "Login berhasil", "token": "dummy_token_123", "user": admin_user.get_info()}
    raise AuthenticationError("Username atau password salah")

@router.post("/logout")
def logout():
    return {"message": "Logout berhasil"}
