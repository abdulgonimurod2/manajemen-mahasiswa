import re

class Person:
    def __init__(self, nama: str, email: str, no_telp: str):
        self._nama = nama
        self._email = email
        self._no_telp = no_telp

    def get_info(self) -> str:
        return f"Nama: {self._nama}, Email: {self._email}, No Telp: {self._no_telp}"

    def validate_email(self) -> bool:
        if not self._email:
            return True # Allow for User where email logic is not applied directly
        regex = r"^[\w\.\-]+@[\w\-]+\.\w{2,6}$"
        return re.match(regex, self._email) is not None


class Mahasiswa(Person):
    def __init__(self, nim: str, nama: str, jurusan: str, angkatan: int, ipk: float, email: str, no_telp: str, status: str):
        super().__init__(nama, email, no_telp)
        self._nim = nim
        self._jurusan = jurusan
        self._angkatan = angkatan
        self._ipk = ipk
        self._status = status

    def get_info(self) -> str:
        return f"Mahasiswa: {self._nama} ({self._nim}) - Jurusan: {self._jurusan}"

    def to_dict(self) -> dict:
        return {
            "nim": self._nim,
            "nama": self._nama,
            "jurusan": self._jurusan,
            "angkatan": self._angkatan,
            "ipk": self._ipk,
            "email": self._email,
            "no_telp": self._no_telp,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Mahasiswa":
        return cls(
            nim=data.get("nim"),
            nama=data.get("nama"),
            jurusan=data.get("jurusan"),
            angkatan=int(data.get("angkatan", 0)),
            ipk=float(data.get("ipk", 0.0)),
            email=data.get("email"),
            no_telp=data.get("no_telp"),
            status=data.get("status")
        )

    def validate_nim(self) -> bool:
        regex = r"^\d{10}$"
        return re.match(regex, self._nim) is not None


class User(Person):
    def __init__(self, username: str, password: str, nama_lengkap: str):
        super().__init__(nama_lengkap, None, None)
        self._username = username
        self._password = password

    def get_info(self) -> str:
        return f"Admin User: {self._username} - Nama: {self._nama}"

    def check_password(self, password: str) -> bool:
        return self._password == password
