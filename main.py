import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(
    title="Zion AI Core API",
    description="Institutional Risk Gateway Engine backend processing portal.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# CORS SECURITY INTERFACE CONFIGURATION
# -------------------------------------------------------------------------
# This enables your website hosted on GitHub Pages/Vercel to securely 
# communicate with this backend API on Render.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace ["*"] with ["https://zionai.in.net"] for strict access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# SUPABASE CONNECTION INITIALIZATION
# -------------------------------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("CRITICAL ERROR: Supabase environment credentials missing or invalid.")

# Establish connection client instance 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------------------------
# API APPLICATION ROUTING ENDPOINTS
# -------------------------------------------------------------------------
@app.get("/")
def read_root():
    """
    Heartbeat connection check root node.
    """
    return {"status": "online", "engine": "Zion AI Imperium Node v1.0.0"}

@app.post("/manual-signup")
async def manual_signup(
    email: str = Form(...), 
    password: str = Form(...), 
    remark_id: str = Form(...)
):
    """
    Receives frontend user registration alongside the generated UPI Transaction ID
    and commits them directly into the secure Supabase database tracking ledger.
    """
    try:
        # Construct the database entity dictionary model
        payload = {
            "email": email.strip().lower(),
            "password_hash": password,  # For production scale, run this through bcrypt.hash()
            "transaction_remark_id": remark_id.strip(),
            "status": "pending_verification"
        }
        
        # Execute query statement injection on the Supabase ledger table
        response = supabase.table("subscriptions").insert(payload).execute()
        
        # Confirm write accuracy pattern tracking validation
        if hasattr(response, 'data') and len(response.data) > 0:
            return {
                "status": "success", 
                "message": "Transaction verified and logged into administrative authorization ledger.",
                "remark_id": remark_id
            }
        else:
            raise HTTPException(status_code=400, detail="Database rejected resource layout commit map parameters.")
            
    except Exception as e:
        # Handle duplicate account entries or collision errors elegantly
        error_msg = str(e)
        if "duplicate key value" in error_msg:
            raise HTTPException(status_code=409, detail="This corporate email or transaction token reference is already active.")
        raise HTTPException(status_code=500, detail=f"Internal Gateway Error: {error_msg}")