import re
from api.models.exceptions import ValidationError

def validate_nim(nim: str):
    if not re.match(r"^\d{10}$", str(nim)):
        raise ValidationError("Format NIM tidak valid (Tepat 10 digit angka)")

def validate_nama(nama: str):
    if not re.match(r"^[A-Za-z\s\.]{3,50}$", str(nama)):
        raise ValidationError("Format Nama tidak valid")

def validate_email(email: str):
    if not re.match(r"^[\w\.\-]+@[\w\-]+\.\w{2,6}$", str(email)):
        raise ValidationError("Format Email tidak valid")

def validate_no_telp(no_telp: str):
    if not re.match(r"^(\+62|0)[0-9]{9,12}$", str(no_telp)):
        raise ValidationError("Format No. Telepon tidak valid")

def validate_angkatan(angkatan: str):
    if not re.match(r"^20[0-9]{2}$", str(angkatan)):
        raise ValidationError("Format Angkatan tidak valid (2000-2099)")

def validate_ipk(ipk: str):
    if not re.match(r"^([0-3](\.\d{1,2})?|4(\.0{1,2})?)$", str(ipk)):
        raise ValidationError("Format IPK tidak valid (0.00 - 4.00)")

def validate_mahasiswa_data(data: dict):
    validate_nim(data.get("nim", ""))
    validate_nama(data.get("nama", ""))
    validate_email(data.get("email", ""))
    validate_no_telp(data.get("no_telp", ""))
    validate_angkatan(str(data.get("angkatan", "")))
    validate_ipk(str(data.get("ipk", "")))
