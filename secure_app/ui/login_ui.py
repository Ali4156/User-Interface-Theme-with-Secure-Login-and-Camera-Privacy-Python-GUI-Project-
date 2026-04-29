import tkinter as tk
from tkinter import ttk

from assets.theme import Theme
from auth.auth import AuthManager
from security.logger import Logger


class LoginUI:
    def __init__(
        self,
        root: tk.Tk,
        auth_manager: AuthManager,
        logger: Logger,
        on_success,
        on_setup_gmail=None,
    ):
        self.root = root
        self.auth_manager = auth_manager
        self.logger = logger
        self.on_success = on_success
        self.on_setup_gmail = on_setup_gmail
        self.frame = tk.Frame(root, bg=Theme.get_bg_color())

        # Register as theme observer
        from assets.theme import theme_manager
        theme_manager.add_observer(self)

        self._build_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self.frame, bg=Theme.PANEL_COLOR, padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            container,
            text="Secure Login",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=Theme.TITLE_FONT,
        )
        title.pack(pady=(0, 14))

        self.message_label = tk.Label(
            container,
            text="Enter your credentials",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
        )
        self.message_label.pack(pady=(0, 18))

        self.username_entry = self._create_entry(container, "Username")
        self.password_entry = self._create_entry(container, "Password", show="*")

        login_button = tk.Button(
            container,
            text="Login",
            command=self._handle_login,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=12,
            pady=8,
        )
        login_button.pack(pady=(18, 0), fill="x")

        if self.on_setup_gmail:
            setup_button = tk.Button(
                container,
                text="Setup Gmail OTP",
                command=self._handle_setup,
                bg=Theme.CARD_COLOR,
                fg=Theme.TEXT_COLOR,
                relief="flat",
                padx=12,
                pady=8,
            )
            setup_button.pack(pady=(12, 0), fill="x")

    def _create_entry(self, parent, placeholder: str, show: str = "") -> tk.Entry:
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
            show=show,
            font=Theme.FONT,
        )
        entry.pack(fill="x", ipady=8)
        return entry

    def _handle_login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.message_label.config(
                text="Please enter both username and password.",
                fg=Theme.DANGER_COLOR,
            )
            return

        is_valid, error_message = self.auth_manager.validate_credentials(username, password)
        if is_valid:
            self.message_label.config(text="Login accepted. Proceed to MFA.", fg=Theme.SUCCESS_COLOR)
            self.on_success(username)
            return

        self.message_label.config(text=error_message or "Login failed.", fg=Theme.DANGER_COLOR)

    def _handle_setup(self) -> None:
        if self.on_setup_gmail:
            self.on_setup_gmail()

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

    def show(self) -> None:
        self.frame.place(relwidth=1, relheight=1)

    def hide(self) -> None:
        self.frame.place_forget()
