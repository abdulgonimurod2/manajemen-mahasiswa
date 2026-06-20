from fastapi import APIRouter
from pydantic import BaseModel
import time

from api.models.mahasiswa import Mahasiswa
from api.services.file_service import read_students_data, write_students_data
from api.services.validation_service import validate_mahasiswa_data
from api.services.search_service import search_data
from api.services.sort_service import sort_data
from api.models.exceptions import DataNotFoundError, DuplicateNIMError

router = APIRouter()

class MahasiswaModel(BaseModel):
    nim: str
    nama: str
    jurusan: str
    angkatan: int
    ipk: float
    email: str
    no_telp: str
    status: str

@router.get("/")
def get_all_mahasiswa():
    start = time.perf_counter()
    data = read_students_data()
    dicts = [m.to_dict() for m in data]
    duration = (time.perf_counter() - start) * 1000
    return {"data": dicts, "execution_time_ms": duration}

@router.get("/search")
def search_mahasiswa(query: str = "", method: str = "linear", field: str = "nama"):
    start = time.perf_counter()
    data = read_students_data()
    results = search_data(data, method, query, field)
    dicts = [m.to_dict() for m in results]
    duration = (time.perf_counter() - start) * 1000
    return {"data": dicts, "execution_time_ms": duration, "method": method}

@router.get("/sort")
def sort_mahasiswa(field: str = "nim", method: str = "bubble", order: str = "asc"):
    start = time.perf_counter()
    data = read_students_data()
    results = sort_data(data, method, field, order)
    dicts = [m.to_dict() for m in results]
    duration = (time.perf_counter() - start) * 1000
    return {"data": dicts, "execution_time_ms": duration, "method": method, "order": order}

@router.get("/{nim}")
def get_mahasiswa(nim: str):
    data = read_students_data()
    for m in data:
        if m._nim == nim:
            return {"data": m.to_dict()}
    raise DataNotFoundError("Data mahasiswa tidak ditemukan")

@router.post("/")
def create_mahasiswa(req: MahasiswaModel):
    data_dict = req.model_dump() if hasattr(req, 'model_dump') else req.dict()
    validate_mahasiswa_data(data_dict)
    data = read_students_data()
    
    if any(m._nim == req.nim for m in data):
        raise DuplicateNIMError("NIM sudah terdaftar dalam sistem")
        
    new_mhs = Mahasiswa.from_dict(data_dict)
    
    from api.services.database import supabase
    supabase.table("students").insert(data_dict).execute()
    
    return {"message": "Data mahasiswa berhasil ditambahkan", "data": new_mhs.to_dict()}

@router.put("/{nim}")
def update_mahasiswa(nim: str, req: MahasiswaModel):
    data_dict = req.model_dump() if hasattr(req, 'model_dump') else req.dict()
    validate_mahasiswa_data(data_dict)
    data = read_students_data()
    
    found = any(m._nim == nim for m in data)
            
    if not found:
        raise DataNotFoundError("Data mahasiswa tidak ditemukan")
        
    from api.services.database import supabase
    supabase.table("students").update(data_dict).eq("nim", nim).execute()
    
    return {"message": "Data mahasiswa berhasil diupdate"}

@router.delete("/{nim}")
def delete_mahasiswa(nim: str):
    data = read_students_data()
    found = any(m._nim == nim for m in data)
    if not found:
        raise DataNotFoundError("Data mahasiswa tidak ditemukan")
        
    from api.services.database import supabase
    supabase.table("students").delete().eq("nim", nim).execute()
    
    return {"message": "Data mahasiswa berhasil dihapus"}
