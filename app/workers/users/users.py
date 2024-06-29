from app.dependencies import supabase

# Check if a user exists in the database
def user_exists(key: str, value: str):
    res = supabase.from_("users").select("*").eq(key, value).execute()
    return len(res.data) > 0