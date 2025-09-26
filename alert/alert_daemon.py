import dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from backend_enum.attack_types import AttackType

dotenv.load_dotenv()

SENDGRID_API_KEY: str = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL: str = os.getenv('SENDER_EMAIL') # you guys can remove from .env

def alert(attack_type: str):
    pass

attack_type = AttackType.BRUTE_FORCE.value
print(attack_type)
target_email = "ram19870101@gmail.com"
attack_time = "14:32:18 - 14:34:52 UTC"
attempts_detected = 10
status="blocked"

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Alert - Attack Blocked</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #000; margin: 0; padding: 0;">
    <div style="background: #f8f8f8; padding: 20px; min-height: 100vh;">
        <div style="max-width: 600px; margin: 0 auto; background: #fff; border-radius: 6px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
            
            <div style="background: #dc3545; color: white; padding: 30px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);">
                <h1 style="font-size: 24px; font-weight: bold; margin: 0 0 8px 0;">SECURITY ALERT</h1>
                <p style="font-size: 16px; opacity: 0.95; margin: 0;">Suspicious Activity Detected & Blocked</p>
            </div>
            
            <div style="padding: 30px;">
                <div style="background: #000; color: white; padding: 15px; border-radius: 4px; margin-bottom: 25px; text-align: center; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);">
                    <div style="font-size: 16px; font-weight: bold;">
                        Attack Successfully Blocked - Your Account is Secured
                    </div>
                </div>
                
                <div style="background: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 20px; margin-bottom: 25px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);">
                    <h2 style="font-size: 18px; font-weight: bold; color: #000; margin: 0 0 15px 0; border-bottom: 1px solid #eee; padding-bottom: 8px;">Attack Details</h2>
                    <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5;">
                        <span style="font-weight: bold; color: #333;">Attack Type:</span>
                        <span style="color: #000; font-family: monospace; background: #f5f5f5; padding: 4px 8px; border-radius: 3px; box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);">{attack_type}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5;">
                        <span style="font-weight: bold; color: #333;">Target Account:</span>
                        <span style="color: #000; font-family: monospace; background: #f5f5f5; padding: 4px 8px; border-radius: 3px; box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);">{target_email}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5;">
                        <span style="font-weight: bold; color: #333;">Attack Timing:</span>
                        <span style="color: #000; font-family: monospace; background: #f5f5f5; padding: 4px 8px; border-radius: 3px; box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);">{attack_time}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5;">
                        <span style="font-weight: bold; color: #333;">Attempts Detected:</span>
                        <span style="color: #000; font-family: monospace; background: #f5f5f5; padding: 4px 8px; border-radius: 3px; box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);">{attempts_detected} failed login attempts</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 12px 0;">
                        <span style="font-weight: bold; color: #333;">Status:</span>
                        <span style="color: white; font-family: monospace; background: #dc3545; padding: 4px 8px; border-radius: 3px; box-shadow: 0 1px 3px rgba(220, 53, 69, 0.3);">{status}</span>
                    </div>
                </div>
                
                <div style="background: #fff; border: 1px solid #ddd; color: #000; padding: 20px; border-radius: 4px; margin-bottom: 25px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);">
                    <h3 style="font-size: 18px; font-weight: bold; margin: 0 0 12px 0; color: #000;">Your Account is Now Secured</h3>
                    <p style="margin: 0 0 15px 0;">Our security systems have detected and blocked this suspicious activity. The malicious request attempting to compromise your account has been neutralized.</p>
                    
                    <ul style="list-style: none; padding: 0; margin: 15px 0 0 0;">
                        <li style="padding: 6px 0; padding-left: 20px; position: relative; color: #333;">
                            <span style="position: absolute; left: 0; color: #000; font-weight: bold;">•</span>
                            All unauthorized access attempts have been blocked
                        </li>
                        <li style="padding: 6px 0; padding-left: 20px; position: relative; color: #333;">
                            <span style="position: absolute; left: 0; color: #000; font-weight: bold;">•</span>
                            Your account credentials remain secure
                        </li>
                        <li style="padding: 6px 0; padding-left: 20px; position: relative; color: #333;">
                            <span style="position: absolute; left: 0; color: #000; font-weight: bold;">•</span>
                            Enhanced monitoring is now active on your account
                        </li>
                        <li style="padding: 6px 0; padding-left: 20px; position: relative; color: #333;">
                            <span style="position: absolute; left: 0; color: #000; font-weight: bold;">•</span>
                            No further action is required from you
                        </li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #000; color: #ccc; padding: 20px; text-align: center; box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 16px; font-weight: bold; color: #fff; margin-bottom: 8px;">Security Operations Center</div>
                <p style="font-size: 14px; color: #aaa; margin: 0 0 12px 0;">
                    This alert was generated by our automated security monitoring system.
                </p>
                <div style="font-size: 12px; color: #888; font-family: monospace;">
                    Alert Generated: <span id="timestamp"></span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
"""

# message = Mail(
#     from_email=SENDER_EMAIL,
#     to_emails=target_email,
#     subject="SECURITY ALERT!",
#     html_content=html_content,
# )

# try:
#     sg = SendGridAPIClient(SENDGRID_API_KEY)
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)
