from supabase import create_client, Client

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

def create_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_API_KEY")
    supabase: Client = create_client(url, key)
    return supabase
