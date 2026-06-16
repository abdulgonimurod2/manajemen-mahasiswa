from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import seluruh router API
from api.routes import auth_routes, mahasiswa_routes

# Import custom exception
from api.models.exceptions import (
    AppException, ValidationError, DataNotFoundError, 
    DuplicateNIMError, FileIOError, AuthenticationError
)

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Manajemen Mahasiswa API")

# Konfigurasi CORS untuk mengizinkan akses dari seluruh domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Exception Handlers
# =========================

# Error validasi data
@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})

# Error data tidak ditemukan
@app.exception_handler(DataNotFoundError)
def not_found_exception_handler(request: Request, exc: DataNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# Error data duplikat
@app.exception_handler(DuplicateNIMError)
def duplicate_nim_exception_handler(request: Request, exc: DuplicateNIMError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

# Error file
@app.exception_handler(FileIOError)
def file_io_exception_handler(request: Request, exc: FileIOError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Error login
@app.exception_handler(AuthenticationError)
def auth_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

# Fallback untuk seluruh error yang tidak tertangani
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "Terjadi kesalahan internal pada server"})

# =========================
# Registrasi Router
# =========================

# Endpoint API untuk auth atau login
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])

# Endpoint API untuk manajemen mahasiswa
app.include_router(mahasiswa_routes.router, prefix="/api/mahasiswa", tags=["mahasiswa"])

@app.get("/api")
def read_root():
    return {"message": "Welcome to Manajemen Data Mahasiswa API"}

# Mount frontend files untuk Local Development Server
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint untuk halaman login
@app.get("/")
def get_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Server berjalan. Halaman beranda HTML belum dibuat."}

# Endpoint untuk halaman dashboard
@app.get("/dashboard.html")
def get_dashboard():
    if os.path.exists("dashboard.html"):
        return FileResponse("dashboard.html")
    return {"message": "Server berjalan. Dashboard HTML belum dibuat."}
