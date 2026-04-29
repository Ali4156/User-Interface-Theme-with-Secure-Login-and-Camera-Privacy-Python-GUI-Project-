import tkinter as tk

from assets.theme import Theme
from auth.auth import AuthManager
from auth.otp import OTPManager
from camera.camera import CameraHandler
from security.logger import Logger
from security.limiter import LoginLimiter
from ui.login_ui import LoginUI
from ui.otp_ui import OTPUI
from ui.dashboard import DashboardUI
from ui.gmail_setup_wizard import GmailSetupWizard
from ui.theme_settings import ThemeSettingsUI


class SecureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Secure Login System")
        self.root.geometry("900x620")
        self.root.configure(bg=Theme.BG_COLOR)
        self.root.resizable(False, False)

        self.logger = Logger()
        self.limiter = LoginLimiter()
        self.auth_manager = AuthManager(self.logger, self.limiter)
        self.otp_manager = OTPManager(self.logger)
        self.camera_handler = CameraHandler(self.logger)

        self.current_user = None
        self.login_ui = LoginUI(self.root, self.auth_manager, self.logger, self.on_login_success, self.show_gmail_setup)
        self.otp_ui = OTPUI(
            self.root,
            self.auth_manager,
            self.otp_manager,
            self.logger,
            self.on_otp_verified,
            self.show_login_screen,
        )
        self.dashboard = DashboardUI(self.root, self.camera_handler, self.logger, self.on_logout, self.show_theme_settings)
        self.gmail_wizard = GmailSetupWizard(self.root, self.on_wizard_complete, self.on_wizard_skip)
        self.theme_settings = None

        self.show_login_screen()

    def show_login_screen(self) -> None:
        self.current_user = None
        self.otp_ui.hide()
        self.dashboard.hide()
        self.login_ui.show()

    def on_login_success(self, username: str) -> None:
        self.current_user = username
        self.login_ui.hide()
        self.otp_ui.show(username)

    def on_otp_verified(self, username: str) -> None:
        self.otp_ui.hide()
        self.dashboard.show(username)

    def on_logout(self) -> None:
        self.camera_handler.stop_camera()
        self.logger.log("SECURITY", f"User logged out: {self.current_user}")
        self.show_login_screen()

    def on_wizard_complete(self) -> None:
        self.gmail_wizard.hide()
        self.logger.log("SETUP", "Gmail setup wizard completed")
        self.show_login_screen()

    def on_wizard_skip(self) -> None:
        self.gmail_wizard.hide()
        self.logger.log("SETUP", "Gmail setup wizard skipped")
        self.show_login_screen()

    def show_theme_settings(self) -> None:
        if self.theme_settings is None or not self.theme_settings.window.winfo_exists():
            self.theme_settings = ThemeSettingsUI(self.root, self.on_theme_settings_close)
        else:
            self.theme_settings.window.lift()

    def on_theme_settings_close(self) -> None:
        self.theme_settings = None

    def show_gmail_setup(self) -> None:
        self.login_ui.hide()
        self.otp_ui.hide()
        self.dashboard.hide()
        self.gmail_wizard.show()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureApp(root)
    app.run()
