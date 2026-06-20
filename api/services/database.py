import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://gzopfvyryijiibtzdwos.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_LV6w3H0p0vpIs3o3f5BFng_DdK1Lk8f")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
