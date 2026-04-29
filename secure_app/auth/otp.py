import pyotp
import qrcode
from io import BytesIO
from PIL import Image
import yagmail
import os
import base64
from email.mime.text import MIMEText
from pathlib import Path
from security.logger import Logger

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False


class OTPManager:
    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger()
        self._load_email_config()
        self.gmail_service = None
        if GMAIL_API_AVAILABLE:
            self._setup_gmail_api()

    def _load_email_config(self):
        """Load email configuration from config file"""
        config_path = Path(__file__).resolve().parent.parent / "email_config.txt"
        self.email_config = {
            "user": "your-email@gmail.com",
            "password": "your-app-password",
            "server": "smtp.gmail.com",
            "use_gmail_api": False,
            "credentials_path": "credentials.json",
            "token_path": "token.json"
        }

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                key = key.strip().lower()
                                value = value.strip()
                                if key == 'email_user':
                                    self.email_config['user'] = value
                                elif key == 'email_password':
                                    self.email_config['password'] = value
                                elif key == 'smtp_server':
                                    self.email_config['server'] = value
                                elif key == 'use_gmail_api':
                                    self.email_config['use_gmail_api'] = value.lower() == 'true'
                                elif key == 'credentials_path':
                                    self.email_config['credentials_path'] = value
                                elif key == 'token_path':
                                    self.email_config['token_path'] = value
            except Exception as e:
                self.logger.log("AUTH", f"Error loading email config: {e}")

    def _setup_gmail_api(self):
        """Setup Gmail API service"""
        try:
            creds = None
            token_path = Path(__file__).resolve().parent.parent / self.email_config['token_path']
            credentials_path = Path(__file__).resolve().parent.parent / self.email_config['credentials_path']

            # Check if token.json exists
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), ['https://www.googleapis.com/auth/gmail.send'])

            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not credentials_path.exists():
                        self.logger.log("AUTH", "Gmail API credentials.json not found. Falling back to SMTP.")
                        return

                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(credentials_path), ['https://www.googleapis.com/auth/gmail.send'])
                    creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self.logger.log("AUTH", "Gmail API service initialized successfully")

        except Exception as e:
            self.logger.log("AUTH", f"Failed to setup Gmail API: {e}. Falling back to SMTP.")
            self.gmail_service = None

    def _create_message(self, sender, to, subject, message_text):
        """Create a message for an email"""
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def _send_gmail_message(self, message):
        """Send an email via Gmail API"""
        try:
            sent_message = self.gmail_service.users().messages().send(userId="me", body=message).execute()
            return sent_message
        except Exception as e:
            self.logger.log("AUTH", f"Gmail API send failed: {e}")
            return None

    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()

    def get_provisioning_uri(self, username: str, secret: str) -> str:
        issuer = "SecureApp MFA"
        self.logger.log("AUTH", f"Generated provisioning URI for {username}")
        return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)

    def create_qr_image(self, provisioning_uri: str) -> Image.Image:
        qr = qrcode.QRCode(border=1)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        return image

    def send_otp_email(self, email: str, username: str, otp_code: str) -> bool:
        """Send OTP code via email using Gmail API or SMTP fallback"""
        subject = "SecureApp - Your OTP Code"
        body = f"""
Hello {username},

Your One-Time Password (OTP) for SecureApp login is:

{otp_code}

This code will expire in 30 seconds.

If you didn't request this code, please ignore this email.

Best regards,
SecureApp Team
"""

        # Try Gmail API first if configured and available
        if (self.email_config.get('use_gmail_api', False) and
            self.gmail_service and
            GMAIL_API_AVAILABLE):

            try:
                message = self._create_message(self.email_config['user'], email, subject, body)
                result = self._send_gmail_message(message)
                if result:
                    self.logger.log("AUTH", f"OTP email sent via Gmail API to {email} for user {username}")
                    return True
            except Exception as e:
                self.logger.log("AUTH", f"Gmail API failed, falling back to SMTP: {e}")

        # Fallback to SMTP
        try:
            # Check if email is configured
            if self.email_config['user'] == 'your-email@gmail.com':
                self.logger.log("AUTH", "Email not configured - using default placeholder")
                return False

            yag = yagmail.SMTP(
                self.email_config['user'],
                self.email_config['password'],
                self.email_config['server']
            )
            yag.send(email, subject, body)
            self.logger.log("AUTH", f"OTP email sent via SMTP to {email} for user {username}")
            return True
        except Exception as e:
            self.logger.log("AUTH", f"Failed to send OTP email to {email}: {str(e)}")
            return False

    def _get_totp(self, secret: str) -> pyotp.TOTP:
        return pyotp.TOTP(secret)

    def verify_otp(self, secret: str, code: str) -> bool:
        if not secret:
            self.logger.log("AUTH", "OTP verification failed: missing secret")
            return False
        totp = self._get_totp(secret)
        valid = totp.verify(code.strip(), valid_window=1)
        self.logger.log("AUTH", f"OTP verification attempt: {'success' if valid else 'failure'}")
        return valid
