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
    version="1.2.0",
    redirect_slashes=False
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

# SMTP Credentials configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "zionai3636@gmail.com")

# CRITICAL SECURITY CLEANUP: Automatically strips accidental spaces from the 16-character code
RAW_PASSWORD = os.getenv("SENDER_PASSWORD", "jrdo odow duwq wvlz")
SENDER_PASSWORD = RAW_PASSWORD.replace(" ", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("CRITICAL ERROR: Supabase environment credentials missing or invalid.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------------------------
# MAILING HELPER INFRASTRUCTURE
# -------------------------------------------------------------------------
def send_payment_received_email(client_email: str, remark_id: str) -> bool:
    """Dispatches a direct transaction confirmation instantly upon manual signup submission."""
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Zion AI Solvency Systems <{SENDER_EMAIL}>"
    msg['To'] = client_email
    msg['Subject'] = "💳 Zion AI | Payment Submission Processing"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0E1117; color: #c9d1d9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #161B22; border: 1px solid #C5A059; padding: 30px; border-radius: 10px;">
            <h2 style="color: #C5A059; text-align: center; border-bottom: 1px solid #C5A059; padding-bottom: 10px;">PAYMENT REGISTRATION RECEIVED</h2>
            <p>Thank you for choosing <strong>Zion AI Solutions</strong>.</p>
            <p>Your ₹7,999 payment registration details have been securely logged. Our ledger team is currently verifying your transaction reference token:</p>
            <div style="background-color: #0E1117; padding: 15px; border-radius: 5px; border-left: 4px solid #C5A059; font-family: monospace; font-size: 16px; margin: 20px 0; color: #fff;">
                {remark_id}
            </div>
            <p><strong>Next Steps:</strong> Once our manual audit loop finishes verification (typically 5 to 6 hours), your core terminal node workspace will activate automatically. You will receive an initialized handbook instructions email right here as soon as authorization clears.</p>
            <p style="font-size: 12px; text-align: center; color: #8e949e; margin-top: 30px; border-top: 1px solid #30363d; padding-top: 10px;">
                © 2026 Zion AI Solvency Matrix Systems. Core Data Streams Secure.
            </p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        print(f"SMTP SUCCESS: Dispatched payment pending validation notice to {client_email}")
        return True
    except Exception as e:
        print(f"SMTP ERROR in manual-signup email layer for {client_email}: {str(e)}")
        return False

def send_welcome_email(client_email: str) -> bool:
    """Dispatches the clean, point-by-point setup guide to active subscribers using rich responsive HTML layout framing."""
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Zion AI Solvency Systems <{SENDER_EMAIL}>"
    msg['To'] = client_email
    msg['Subject'] = "🔒 Access Granted: Your Imperium Terminal Guide"

    html_body = """
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0E1117; color: #c9d1d9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #161B22; border: 1px solid #C5A059; padding: 30px; border-radius: 10px;">
            <h2 style="color: #C5A059; text-align: center; border-bottom: 1px solid #C5A059; padding-bottom: 10px;">IMPERIUM ENGINE NODE CLEARED</h2>
            <p>Dear User,</p>
            <p>Your ₹7,999 payment registration has been verified! Your premium node access is now active for <strong>30 days continuous timeline</strong>.</p>
            
            <h3 style="color: #C5A059; margin-top: 25px;">🚀 HOW TO ACCESS AND USE YOUR ENGINE WORKSPACE:</h3>
            <ol style="line-height: 1.8; padding-left: 20px;">
                <li><strong>How to Access the Terminal:</strong> Go to the main interface workspace, click <strong>"SIGN IN"</strong> at the top right, and log in with your registered corporate credentials.</li>
                <li><strong>Input Your Company Data:</strong> Locate the control sidebar panel on the left and enter your Corporate Entity Name, Sector, and Enterprise Fundamentals (Liquid Reserves, Revenue, Operating Costs).</li>
                <li><strong>Set Up Your Risk Situation:</strong> Scroll down the left sidebar to the "Black Swan Suite" and check the economic hazard boxes you wish to test (e.g., Banking Collapse, Trade Route Closures).</li>
                <li><strong>Execute Your System Analysis:</strong> Click the large gold button marked <strong>"EXECUTE SYSTEM ANALYSIS"</strong>. The model will instantly render your Net Flow, Resilience Index, and exact Survival Month Runway.</li>
                <li><strong>Generate AI Advanced Strategies:</strong> Go to the bottom left section of the dashboard page and click <strong>"ACTIVATE AI WAR ROOM STRATEGY"</strong> to output 5 custom corporate tactics from Llama-3 AI.</li>
                <li><strong>Export an Executive Board PDF:</strong> Click <strong>"DOWNLOAD BOARD-READY PDF"</strong> at the bottom right section to instantly download a complete physical layout containing diagnostic dark-themed charts.</li>
            </ol>

            <div style="background-color: #0E1117; padding: 15px; border-radius: 5px; border-left: 4px solid #8E6D29; margin-top: 25px;">
                <p style="margin: 0; font-size: 12px; color: #8e949e;">
                    <strong>⚠️ System Expiration Guardrail:</strong> Your database entry will automatically transition to an expired status exactly 30 days from activation. Core metrics will lock automatically if renewals are not logged.
                </p>
            </div>
            
            <p style="font-size: 12px; text-align: center; color: #8e949e; margin-top: 30px; border-top: 1px solid #30363d; padding-top: 10px;">
                © 2026 Zion AI Solvency Matrix Systems. Core Data Streams Secure.
            </p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        print(f"SMTP SUCCESS: Dispatched terminal instructions handbook onboarding email smoothly to {client_email}")
        return True
    except Exception as e:
        print(f"SMTP ERROR in welcome notification layer for {client_email}: {str(e)}")
        return False

def send_expiry_warning_email(client_email: str, days_left: int) -> bool:
    """Dispatches warning notifications when a user subscription is approaching sunset."""
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Zion AI Solvency Systems <{SENDER_EMAIL}>"
    msg['To'] = client_email
    msg['Subject'] = f"⚠️ Alert: Your Zion AI Subscription Expires in {days_left} Days"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0E1117; color: #c9d1d9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #161B22; border: 1px solid #D65A5A; padding: 30px; border-radius: 10px;">
            <h2 style="color: #D65A5A; text-align: center; border-bottom: 1px solid #D65A5A; padding-bottom: 10px;">⚠️ CRISIS ACCELERATION TIMELINE DETECTED</h2>
            <p>Dear User,</p>
            <p>This is an automated tracking alert: Your current 30-day allocation node cycle is expiring in <span style="color: #D65A5A; font-weight: bold;">{days_left} days</span>.</p>
            <p>To avoid service disruptions and prevent an absolute lockout from your Imperium Dashboard workspace, please submit your standard ₹7,999 renewal fee via the gateway node portal as soon as possible.</p>
            <p>If a validated renewal is not logged within your timeline window, access will be denied automatically by the core gatekeeper logic.</p>
            <p style="font-size: 12px; text-align: center; color: #8e949e; margin-top: 30px; border-top: 1px solid #30363d; padding-top: 10px;">
                © 2026 Zion AI Solvency Matrix Systems. Core Data Streams Secure.
            </p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        print(f"SMTP SUCCESS: Dispatched expiry threat warning reminder to {client_email}")
        return True
    except Exception as e:
        print(f"SMTP ERROR in automated warning cron layer for {client_email}: {str(e)}")
        return False

# -------------------------------------------------------------------------
# API APPLICATION ROUTING ENDPOINTS
# -------------------------------------------------------------------------
@app.route("/", methods=["GET", "HEAD"])
async def read_root(request):
    """
    Root gateway endpoint handling both browser GET requests and 
    automated uptime health monitor HEAD handshakes cleanly.
    """
    return {"status": "online", "engine": "Zion AI Imperium Node v1.2.0"}

@app.post("/manual-signup")
async def manual_signup(
    email: str = Form(...), 
    password: str = Form(...), 
    remark_id: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        clean_email = email.strip().lower()
        clean_remark = remark_id.strip()
        
        payload = {
            "email": clean_email,
            "password_hash": password,  
            "transaction_remark_id": clean_remark,
            "status": "pending_verification",
            "expires_at": None 
        }
        
        response = supabase.table("subscriptions").insert(payload).execute()
        
        if hasattr(response, 'data') and len(response.data) > 0:
            # FIXED: Triggers a notification email automatically in the background when payment is submitted
            background_tasks.add_task(send_payment_received_email, clean_email, clean_remark)
            
            return {
                "status": "success", 
                "message": "Transaction verified and logged into administrative authorization ledger.",
                "remark_id": clean_remark
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
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            if now > expires_at:
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
            
            supabase.table("subscriptions").update({
                "expires_at": thirty_days_later.isoformat()
            }).eq("email", clean_email).execute()
            
            # Non-blocking background onboarding instructions email execution loop
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
@app.get("/check-subscriptions")
async def check_subscriptions(background_tasks: BackgroundTasks):
    """
    Cron endpoint designed to run once daily. It auto-expires over-due accounts
    and handles email warnings for accounts running out of time.
    """
    try:
        now = datetime.now(timezone.utc)
        warning_window = now + timedelta(days=3)
        
        # 1. Automatic Cleanup
        expired_query = supabase.table("subscriptions").select("email").eq("status", "active").lt("expires_at", now.isoformat()).execute()
        for rec in expired_query.data:
            supabase.table("subscriptions").update({"status": "expired"}).eq("email", rec["email"]).execute()
            
        # 2. Warning Reminders
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
        return {"status": "error", "detail": f"Automation Cron Error: {str(e)}"}
