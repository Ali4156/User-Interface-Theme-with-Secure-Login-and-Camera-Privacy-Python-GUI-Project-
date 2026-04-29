import tkinter as tk
from PIL import Image, ImageTk

from assets.theme import Theme
from auth.auth import AuthManager
from auth.otp import OTPManager
from security.logger import Logger


class OTPUI:
    def __init__(
        self,
        root: tk.Tk,
        auth_manager: AuthManager,
        otp_manager: OTPManager,
        logger: Logger,
        on_verified,
        on_back,
    ):
        self.root = root
        self.auth_manager = auth_manager
        self.otp_manager = otp_manager
        self.logger = logger
        self.on_verified = on_verified
        self.on_back = on_back
        self.frame = tk.Frame(root, bg=Theme.get_bg_color())
        self.qr_image = None
        self.current_user = None

        # Register as theme observer
        from assets.theme import theme_manager
        theme_manager.add_observer(self)

        self._build_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self.frame, bg=Theme.PANEL_COLOR, padx=24, pady=24)
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            container,
            text="Multi-Factor Authentication",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=Theme.TITLE_FONT,
        )
        title.pack(pady=(0, 10))

        self.message_label = tk.Label(
            container,
            text="Scan the QR code with Google Authenticator or get code via email.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
        )
        self.message_label.pack(pady=(0, 18))

        self.qr_label = tk.Label(container, bg=Theme.PANEL_COLOR)
        self.qr_label.pack(pady=(0, 16))

        self.secret_label = tk.Label(
            container,
            text="Secret: N/A",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            wraplength=260,
            justify="center",
        )
        self.secret_label.pack(pady=(0, 6))

        self.otp_code_label = tk.Label(
            container,
            text="Current code: N/A",
            fg=Theme.SUCCESS_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        self.otp_code_label.pack(pady=(0, 8))

        self.refresh_button = tk.Button(
            container,
            text="Refresh Code",
            command=self._refresh_code,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=12,
            pady=8,
        )
        self.refresh_button.pack(pady=(0, 12), fill="x")

        self.email_button = tk.Button(
            container,
            text="Send Code via Email",
            command=self._send_email_otp,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=12,
            pady=8,
        )
        self.email_button.pack(pady=(0, 12), fill="x")

        self.code_entry = self._create_entry(container, "Enter OTP code")

        verify_button = tk.Button(
            container,
            text="Verify OTP",
            command=self._handle_verify,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=12,
            pady=8,
        )
        verify_button.pack(pady=(16, 0), fill="x")

        self.back_button = tk.Button(
            container,
            text="Back to Login",
            command=self._back_to_login,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=12,
            pady=8,
        )
        self.back_button.pack(pady=(12, 0), fill="x")

    def _create_entry(self, parent, placeholder: str) -> tk.Entry:
        label = tk.Label(
            parent,
            text=placeholder,
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            anchor="w",
        )
        label.pack(fill="x", pady=(8, 4))

        entry = tk.Entry(
            parent,
            bg=Theme.ENTRY_BG,
            fg=Theme.TEXT_COLOR,
            insertbackground=Theme.TEXT_COLOR,
            relief="flat",
            font=Theme.FONT,
        )
        entry.pack(fill="x", ipady=8)
        return entry

    def on_theme_changed(self):
        """Handle theme changes"""
        self.frame.configure(bg=Theme.get_bg_color())
        self._update_ui_colors()

    def _update_ui_colors(self):
        """Update all UI colors when theme changes"""
        # Update main frame
        self.frame.configure(bg=Theme.get_bg_color())

        # Update container and all children
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=Theme.get_panel_color())
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=Theme.get_panel_color(), fg=Theme.get_text_color())
                    elif isinstance(child, tk.Button):
                        child.configure(bg=Theme.get_button_bg(), fg=Theme.get_text_color(),
                                      activebackground=Theme.get_button_active())
                    elif isinstance(child, tk.Entry):
                        child.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color(),
                                      insertbackground=Theme.get_text_color())

    def show(self, username: str) -> None:
        self.current_user = username
        self.frame.place(relwidth=1, relheight=1)
        self._update_qr()

    def hide(self) -> None:
        self.frame.place_forget()

    def _update_qr(self) -> None:
        secret = self.auth_manager.get_user_secret(self.current_user)
        if not secret:
            self.message_label.config(text="Unable to load MFA secret.", fg=Theme.DANGER_COLOR)
            return

        provisioning_uri = self.otp_manager.get_provisioning_uri(self.current_user, secret)
        qr_image = self.otp_manager.create_qr_image(provisioning_uri)
        qr_image = qr_image.resize((220, 220), Image.Resampling.LANCZOS)
        self.qr_image = ImageTk.PhotoImage(qr_image)
        self.qr_label.config(image=self.qr_image)
        self.code_entry.delete(0, tk.END)
        self.message_label.config(
            text="Use the code shown below, scan the QR code, or get code via email.",
            fg=Theme.TEXT_COLOR,
        )
        self._update_current_code(secret)

    def _handle_verify(self) -> None:
        code = self.code_entry.get().strip()
        secret = self.auth_manager.get_user_secret(self.current_user)
        if self.otp_manager.verify_otp(secret, code):
            self.message_label.config(text="OTP verified. Welcome!", fg=Theme.SUCCESS_COLOR)
            self.on_verified(self.current_user)
            return

        self.message_label.config(text="Invalid OTP code. Try again.", fg=Theme.DANGER_COLOR)

    def _update_current_code(self, secret: str) -> None:
        try:
            totp = self.otp_manager._get_totp(secret)
            self.otp_code_label.config(text=f"Current code: {totp.now()}")
            self.secret_label.config(text=f"Secret: {secret}")
        except Exception:
            self.otp_code_label.config(text="Current code: not available")
            self.secret_label.config(text=f"Secret: {secret}")

    def _refresh_code(self) -> None:
        secret = self.auth_manager.get_user_secret(self.current_user)
        if secret:
            self._update_current_code(secret)

    def _send_email_otp(self) -> None:
        secret = self.auth_manager.get_user_secret(self.current_user)
        email = self.auth_manager.get_user_email(self.current_user)

        if not secret or not email:
            self.message_label.config(
                text="Unable to send email: missing secret or email address.",
                fg=Theme.DANGER_COLOR
            )
            return

        # Generate current OTP code
        totp = self.otp_manager._get_totp(secret)
        current_code = totp.now()

        # Send email
        if self.otp_manager.send_otp_email(email, self.current_user, current_code):
            self.message_label.config(
                text=f"OTP code sent to {email}. Check your email!",
                fg=Theme.SUCCESS_COLOR
            )
        else:
            self.message_label.config(
                text="Failed to send email. Please try again or use QR code.",
                fg=Theme.DANGER_COLOR
            )

    def _back_to_login(self) -> None:
        self.hide()
        self.on_back()
