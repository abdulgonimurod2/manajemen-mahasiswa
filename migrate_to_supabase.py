import json
import os
from api.services.database import supabase

FILE_PATH = "data/students.json"

def migrate():
    if not os.path.exists(FILE_PATH):
        print(f"File {FILE_PATH} tidak ditemukan.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("File JSON kosong atau format tidak valid.")
            return

    if not data:
        print("Tidak ada data untuk dimigrasi (JSON kosong).")
        return

    print(f"Ditemukan {len(data)} data mahasiswa. Mulai proses migrasi ke Supabase...")
    
    success_count = 0
    error_count = 0

    for mhs in data:
        try:
            # Gunakan mapping yang sesuai dengan model atau langsung jika formatnya pas.
            # Saat sebelumnya disimpan ke JSON, keys mungkin masih ada underscore dsb jika serialize dict langsung dari obyek atau plain dari frontend.
            # Berdasarkan file_service.py lama, ini memanggil `m.to_dict()`. Biasanya fieldnya:
            # nim, nama, jurusan, angkatan, ipk, email, no_telp, status
            
            # Prepare data to insert
            insert_data = {
                "nim": mhs.get("nim", ""),
                "nama": mhs.get("nama", ""),
                "jurusan": mhs.get("jurusan", ""),
                "angkatan": mhs.get("angkatan", 0),
                "ipk": mhs.get("ipk", 0.0),
                "email": mhs.get("email", ""),
                "no_telp": mhs.get("no_telp", ""),
                "status": mhs.get("status", "")
            }

            response = supabase.table("students").insert(insert_data).execute()
            if response.data:
                success_count += 1
                print(f"[OK] {mhs.get('nim')} - {mhs.get('nama')}")
            else:
                error_count += 1
                print(f"[FAIL] Gagal masukkan {mhs.get('nim')}")

        except Exception as e:
            error_count += 1
            print(f"[ERROR] {mhs.get('nim')}: {str(e)}")
            
    print("\n--- MIGRASI SELESAI ---")
    print(f"Berhasil: {success_count}")
    print(f"Gagal/Error: {error_count}")
    print("------------------------")

if __name__ == "__main__":
    migrate()
