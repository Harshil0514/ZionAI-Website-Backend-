import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(
    title="Zion AI Core API",
    description="Institutional Risk Gateway Engine backend processing portal with automated subscription expiration controls.",
    version="1.2.0"
)

# -------------------------------------------------------------------------
# CORS SECURITY INTERFACE CONFIGURATION
# -------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# ENVIRONMENT VARIABLES & CLIENT CONFIGURATION
# -------------------------------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# SMTP Credentials configuration (Add these to your host environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "zionai3636@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "xxxx xxxx xxxx xxxx") # Secure 16-character App Password

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("CRITICAL ERROR: Supabase environment credentials missing or invalid.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------------------------
# MAILING HELPER INFRASTRUCTURE
# -------------------------------------------------------------------------
def send_welcome_email(client_email: str):
    """Dispatches the clean, point-by-point setup guide to active subscribers."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = client_email
    msg['Subject'] = "🔒 Access Granted: Your Imperium Terminal Guide"

    body = """Dear User,

Your ₹7,999 payment registration has been verified! Your premium node access is now active for 30 days.

Here is a simple, point-by-point guide showing exactly how to log in and use your terminal node:

1. HOW TO ACCESS THE TERMINAL
• Go to the main website link and click the "SIGN IN" button at the top right.
• Enter your registered corporate Email and Password. 
• Once authenticated, your live Terminal will instantly open up.

2. INPUT YOUR COMPANY DATA
• Look at the control sidebar panel on the left side of the terminal.
• Type in your "Corporate Entity Name" and select your specific "Industry Sector".
• Enter your core numbers under "Enterprise Fundamentals" (Liquid Reserves, Monthly Revenue, Operating Costs).
• Fill out your "Financial Health Ratios" fields directly below it.

3. SET UP YOUR RISK SITUATION
• Scroll down the left sidebar to the "Black Swan Suite".
• Check any economic hazard boxes you wish to test (such as Pandemic Lockdown, Banking Collapse, or Trade Route Closures).

4. EXECUTE YOUR SYSTEM ANALYSIS
• Click the large gold button at the very bottom of the sidebar marked "EXECUTE SYSTEM ANALYSIS".
• Wait a few seconds for the system loop to process.
• The model will instantly calculate and display your Net Flow, a Resilience Index, and your exact Survival Month Runway.

5. GENERATE AI ADVANCED STRATEGIES
• Scroll down to the bottom left section of the dashboard page.
• Click the button named "ACTIVATE AI WAR ROOM STRATEGY".
• Llama-3 AI will analyze your financial situation and output 5 custom corporate tactics.

6. EXPORT AN EXECUTIVE BOARD PDF
• Go to the bottom right section of the dashboard page.
• Click the button named "DOWNLOAD BOARD-READY PDF".
• This will instantly download a complete copy containing your calculated metrics, dark-themed diagnostic charts, and AI strategic briefs.

Please Note: Your workspace allocation node remains active for precisely 30 days. You will receive an automated alert when your timeline is near expiration.

Sincerely,
Operations Command
Zion AI Solutions
"""
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error sending welcome email to {client_email}: {str(e)}")
        return False

def send_expiry_warning_email(client_email: str, days_left: int):
    """Dispatches warning notifications when a user subscription is approaching sunset."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = client_email
    msg['Subject'] = f"⚠️ Alert: Your Zion AI Subscription Expirations in {days_left} Days"

    body = f"""Dear User,

This is an automated system tracking alert regarding your Zion AI subscription clearance.

Your current 30-day allocation node cycle is expiring in {days_left} days. To avoid service disruption and prevent an absolute lockout from the Imperium Dashboard, please submit your standard ₹7,999 renewal fee via the gateway node portal as soon as possible.

If a validated renewal is not logged within your timeline window, access will be denied automatically by the system core logic.

Sincerely,
Billing Node Control
Zion AI Solutions
"""
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error sending warning email to {client_email}: {str(e)}")
        return False

# -------------------------------------------------------------------------
# API APPLICATION ROUTING ENDPOINTS
# -------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"status": "online", "engine": "Zion AI Imperium Node v1.2.0"}

@app.post("/manual-signup")
async def manual_signup(
    email: str = Form(...), 
    password: str = Form(...), 
    remark_id: str = Form(...)
):
    try:
        payload = {
            "email": email.strip().lower(),
            "password_hash": password,  
            "transaction_remark_id": remark_id.strip(),
            "status": "pending_verification",
            "expires_at": None # Initialized empty until admin sets status to active
        }
        
        response = supabase.table("subscriptions").insert(payload).execute()
        
        if hasattr(response, 'data') and len(response.data) > 0:
            return {
                "status": "success", 
                "message": "Transaction verified and logged into administrative authorization ledger.",
                "remark_id": remark_id
            }
        else:
            raise HTTPException(status_code=400, detail="Database rejected resource layout commit map parameters.")
            
    except Exception as e:
        error_msg = str(e)
        if "duplicate key value" in error_msg:
            raise HTTPException(status_code=409, detail="This corporate email or transaction token reference is already active.")
        raise HTTPException(status_code=500, detail=f"Internal Gateway Error: {error_msg}")

@app.post("/verify-login")
async def verify_login(
    email: str = Form(...), 
    password: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        clean_email = email.strip().lower()
        now = datetime.now(timezone.utc)
        
        response = supabase.table("subscriptions").select("*").eq("email", clean_email).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="No profile matching this email address was found.")
            
        user_record = response.data[0]
        
        if user_record.get("password_hash") != password:
            raise HTTPException(status_code=401, detail="Access Denied: Invalid credential profiles.")
            
        current_status = user_record.get("status")
        expires_at_str = user_record.get("expires_at")
        
        # -------------------------------------------------------------------------
        # TIME EXPIRATION GATEKEEPER IMPLEMENTATION
        # -------------------------------------------------------------------------
        if expires_at_str:
            # Parse ISO timestamp string from database to timezone-aware object
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            
            if now > expires_at:
                # Update status to expired dynamically on-the-fly
                supabase.table("subscriptions").update({"status": "expired"}).eq("email", clean_email).execute()
                raise HTTPException(
                    status_code=403, 
                    detail="Access Denied: Your 30-day subscription has ended. Please pay ₹7,999 to renew your access."
                )

        if current_status == "expired":
            raise HTTPException(
                status_code=403, 
                detail="Access Denied: Your 30-day subscription has ended. Please pay ₹7,999 to renew your access."
            )
            
        # If administrative interface sets user to active for the first time, compute timeline limits
        if current_status == "active" and not expires_at_str:
            thirty_days_later = now + timedelta(days=30)
            
            # Apply strict validation timestamps
            supabase.table("subscriptions").update({
                "expires_at": thirty_days_later.isoformat()
            }).eq("email", clean_email).execute()
            
            # Use non-blocking background threads to dispatch emails without slowing client UI logins
            background_tasks.add_task(send_welcome_email, clean_email)
            
            return {"status": "approved", "message": "Access clearing authorized. Allocation window timeline stamped."}
            
        if current_status == "active":
            return {"status": "approved", "message": "Access clearing authorized."}
            
        else:
            return {
                "status": "pending", 
                "detail": "Account clearance pending. Manual transaction audit loops take 5 to 6 hours. Check back shortly."
            }
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Validation Fault: {str(e)}")

# -------------------------------------------------------------------------
# CHRONO-AUTOMATION DAEMON ENDPOINT
# -------------------------------------------------------------------------
@app.post("/check-subscriptions")
async def check_subscriptions(background_tasks: BackgroundTasks):
    """
    Cron endpoint designed to run once daily. It auto-expires over-due accounts
    and handles email warnings for accounts running out of time.
    """
    try:
        now = datetime.now(timezone.utc)
        warning_window = now + timedelta(days=3)
        
        # 1. Automatic Cleanup Query: Instantly terminate profiles past expiration
        expired_query = supabase.table("subscriptions").select("email").eq("status", "active").lt("expires_at", now.isoformat()).execute()
        for rec in expired_query.data:
            supabase.table("subscriptions").update({"status": "expired"}).eq("email", rec["email"]).execute()
            
        # 2. Advanced Reminder Query: Find accounts expiring within the next 3 days
        upcoming_expiry_query = supabase.table("subscriptions").select("email", "expires_at").eq("status", "active").gt("expires_at", now.isoformat()).lt("expires_at", warning_window.isoformat()).execute()
        
        emails_warned = 0
        for rec in upcoming_expiry_query.data:
            expiry_time = datetime.fromisoformat(rec["expires_at"].replace("Z", "+00:00"))
            days_left = max(1, (expiry_time - now).days)
            background_tasks.add_task(send_expiry_warning_email, rec["email"], days_left)
            emails_warned += 1
            
        return {
            "status": "success", 
            "auto_expired_count": len(expired_query.data),
            "warnings_dispatched": emails_warned
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation Cron Error: {str(e)}")
