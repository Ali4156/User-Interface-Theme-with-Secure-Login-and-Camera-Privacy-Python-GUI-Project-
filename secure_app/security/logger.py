from pathlib import Path
from datetime import datetime


class Logger:
    def __init__(self):
        self.log_path = Path(__file__).resolve().parent.parent / "activity.log"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, category: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_path.open("a", encoding="utf-8") as stream:
            stream.write(f"{timestamp} | {category} | {message}\n")
