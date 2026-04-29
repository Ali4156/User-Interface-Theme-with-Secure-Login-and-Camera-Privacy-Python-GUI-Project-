import time


class LoginLimiter:
    def __init__(self, max_attempts: int = 3, lock_seconds: int = 60):
        self.max_attempts = max_attempts
        self.lock_seconds = lock_seconds
        self.attempts: dict[str, int] = {}
        self.locked_until: dict[str, float] = {}

    def can_attempt(self, username: str) -> bool:
        locked_time = self.locked_until.get(username)
        if locked_time is None:
            return True
        if time.time() >= locked_time:
            self.attempts[username] = 0
            self.locked_until.pop(username, None)
            return True
        return False

    def register_failure(self, username: str) -> None:
        self.attempts[username] = self.attempts.get(username, 0) + 1
        if self.attempts[username] >= self.max_attempts:
            self.locked_until[username] = time.time() + self.lock_seconds

    def register_success(self, username: str) -> None:
        self.attempts[username] = 0
        self.locked_until.pop(username, None)

    def get_lock_message(self, username: str) -> str | None:
        locked_time = self.locked_until.get(username)
        if locked_time and time.time() < locked_time:
            remaining = int(locked_time - time.time())
            return f"Account locked. Try again in {remaining} seconds."
        return None
