# Secure App with MFA and Camera Privacy Protection

This project demonstrates a secure login application built with Python, Tkinter, OpenCV, and MFA using TOTP.

## Features

- Username/password login
- Multi-factor authentication using pyotp (TOTP)
- QR code setup for Google Authenticator
- **NEW:** Email OTP verification with Gmail API integration
- **NEW:** Interactive Gmail Setup Wizard
- Dark theme GUI with login, OTP, and dashboard screens
- Camera access permission and live webcam feed
- Face detection and blur using OpenCV Haar Cascade
- Login attempt limiting and account lockout
- Activity logging to `activity.log`
- Logout support and responsive UI

## Project Structure

```
secure_app/
├── main.py
├── requirements.txt
├── README.md
├── activity.log
├── auth/
│   ├── auth.py
│   ├── otp.py
│   └── __init__.py
├── camera/
│   ├── camera.py
│   ├── face_blur.py
│   └── __init__.py
├── security/
│   ├── logger.py
│   ├── limiter.py
│   └── __init__.py
├── ui/
│   ├── login_ui.py
│   ├── otp_ui.py
│   ├── dashboard.py
│   └── __init__.py
└── assets/
    ├── theme.py
    └── __init__.py
```

## Installation

1. Create a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Email OTP Configuration (Optional)

To enable email-based OTP verification:

### Option 1: Gmail API (Recommended for Gmail users)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API in the API Library
4. Create OAuth 2.0 credentials (Desktop application type)
5. Download `credentials.json` and place it in the app directory
6. Edit `email_config.txt`:
   ```
   USE_GMAIL_API=true
   CREDENTIALS_PATH=credentials.json
   TOKEN_PATH=token.json
   ```
7. First run will open browser for OAuth consent and create `token.json`

### Option 2: SMTP (Fallback method)
1. Edit `email_config.txt` with your SMTP credentials:
   ```
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   SMTP_SERVER=smtp.gmail.com
   USE_GMAIL_API=false
   ```

2. For Gmail SMTP:
   - Enable 2-factor authentication on your Google account
   - Generate an App Password: https://support.google.com/accounts/answer/185833
   - Use the App Password (not your regular password) in EMAIL_PASSWORD

3. Update user emails in `auth/auth.py` (currently set to example emails)

## Gmail Setup Wizard

The application includes an interactive Gmail Setup Wizard to guide you through the Gmail API configuration process.

### Accessing the Wizard:
- On the login screen, click "Setup Gmail OTP"
- The wizard will guide you through each step

### What the Wizard Does:
1. **Gmail Account Setup**: Guides you to create/enable Gmail account
2. **Google Cloud Console**: Step-by-step instructions for API setup
3. **Credentials Management**: Helps you select and place credentials.json
4. **Configuration**: Automatically configures the app for Gmail API
5. **Testing**: Verifies the integration works properly

### Manual Setup (Alternative):
If you prefer manual setup, follow the Gmail API instructions above.

## Run

```bash
python main.py
```

## Default Credentials

- Username: `student`
- Password: `Cyber@123`

or

- Username: `admin`
- Password: `1234`

## Notes

- The OTP screen offers three verification methods:
  1. Scan QR code with Google Authenticator (recommended)
  2. Use the displayed code directly
  3. **NEW:** Send code via email (requires email configuration)
- Camera feed requires permission via the Start Camera button.
- Logs are saved automatically to `activity.log`.
