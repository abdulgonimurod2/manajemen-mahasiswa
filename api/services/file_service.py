import os
from api.models.exceptions import FileIOError
from api.models.mahasiswa import Mahasiswa
from api.services.database import supabase

def read_students_data() -> list:
    try:
        response = supabase.table("students").select("*").execute()
        return [Mahasiswa.from_dict(d) for d in response.data]
    except Exception as e:
        raise FileIOError(f"Gagal membaca data dari Supabase: {str(e)}")

def write_students_data(mahasiswa_list: list) -> None:
    # Not used anymore ideally, but kept for compatibility.
    pass

