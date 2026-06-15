import json
import os
from api.models.exceptions import FileIOError
from api.models.mahasiswa import Mahasiswa

FILE_PATH_STUDENTS = "data/students.json"

def read_students_data() -> list:
    try:
        if not os.path.exists(FILE_PATH_STUDENTS):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(FILE_PATH_STUDENTS), exist_ok=True)
            with open(FILE_PATH_STUDENTS, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []
        with open(FILE_PATH_STUDENTS, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Mahasiswa.from_dict(d) for d in data]
    except Exception as e:
        raise FileIOError(f"Gagal membaca file data: {str(e)}")

def write_students_data(mahasiswa_list: list) -> None:
    try:
        data = [m.to_dict() for m in mahasiswa_list]
        os.makedirs(os.path.dirname(FILE_PATH_STUDENTS), exist_ok=True)
        with open(FILE_PATH_STUDENTS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise FileIOError(f"Gagal menulis file data: {str(e)}")
