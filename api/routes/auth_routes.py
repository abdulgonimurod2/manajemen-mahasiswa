from fastapi import APIRouter
from pydantic import BaseModel
from api.models.mahasiswa import User
from api.models.exceptions import AuthenticationError

router = APIRouter()

# Data User Admin
admin_user = User("admin", "Admin123", "Administrator Sistem")

class LoginRequest(BaseModel):
    username: str
    password: str

# Endpoint API untuk auth atau login
@router.post("/login")
def login(req: LoginRequest):
    if req.username == admin_user._username and admin_user.check_password(req.password):
        return {"message": "Login berhasil", "token": "contoh_token", "user": admin_user.get_info()}
    raise AuthenticationError("Username atau password salah")

# Endpoint API untuk logout
@router.post("/logout")
def logout():
    return {"message": "Logout berhasil"}
