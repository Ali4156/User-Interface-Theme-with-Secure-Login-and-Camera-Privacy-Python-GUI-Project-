from security.logger import Logger
from security.limiter import LoginLimiter
from .otp import OTPManager


class AuthManager:
    def __init__(self, logger: Logger = None, limiter: LoginLimiter = None):
        self.logger = logger or Logger()
        self.limiter = limiter or LoginLimiter()
        self.users = {
            "student": {
                "password": "Cyber@123",
                "otp_secret": None,
                "email": "student@example.com",  # Replace with actual email
            },
            "admin": {
                "password": "1234",
                "otp_secret": None,
                "email": "admin@example.com",  # Replace with actual email
            },
        }

    def validate_credentials(self, username: str, password: str) -> tuple[bool, str | None]:
        if username not in self.users:
            self.logger.log("AUTH", f"Unknown username attempt: {username}")
            return False, "Invalid username or password."

        if not self.limiter.can_attempt(username):
            message = self.limiter.get_lock_message(username)
            self.logger.log("AUTH", f"Locked account attempt for {username}")
            return False, message

        if self.users[username]["password"] == password:
            self.limiter.register_success(username)
            self.logger.log("AUTH", f"Login successful for {username}")
            if not self.users[username]["otp_secret"]:
                self.users[username]["otp_secret"] = OTPManager.generate_secret()
            return True, None

        self.limiter.register_failure(username)
        self.logger.log("AUTH", f"Incorrect password for {username}")
        message = self.limiter.get_lock_message(username)
        if message:
            return False, message

        return False, "Invalid username or password."

    def get_user_secret(self, username: str) -> str | None:
        return self.users.get(username, {}).get("otp_secret")

    def get_user_email(self, username: str) -> str | None:
        return self.users.get(username, {}).get("email")
