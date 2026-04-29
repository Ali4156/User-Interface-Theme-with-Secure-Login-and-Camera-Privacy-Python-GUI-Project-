import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

from assets.theme import Theme
from camera.camera import CameraHandler
from security.logger import Logger


class DashboardUI:
    def __init__(self, root: tk.Tk, camera_handler: CameraHandler, logger: Logger, on_logout, on_theme_settings=None):
        self.root = root
        self.camera_handler = camera_handler
        self.logger = logger
        self.on_logout = on_logout
        self.on_theme_settings = on_theme_settings
        self.frame = tk.Frame(root, bg=Theme.get_bg_color())
        self.video_job = None
        self.photo_image = None
        self.current_user = None

        # Register as theme observer
        from assets.theme import theme_manager
        theme_manager.add_observer(self)

        self._build_ui()

    def _build_ui(self) -> None:
        top_panel = tk.Frame(self.frame, bg=Theme.PANEL_COLOR, padx=20, pady=20)
        top_panel.pack(fill="x")

        self.welcome_label = tk.Label(
            top_panel,
            text="Welcome",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=Theme.TITLE_FONT,
        )
        self.welcome_label.pack(side="left")

        # Theme settings button
        if self.on_theme_settings:
            theme_button = tk.Button(
                top_panel,
                text="🎨 Theme",
                command=self._handle_theme_settings,
                bg=Theme.get_card_color(),
                fg=Theme.get_text_color(),
                relief="flat",
                padx=12,
                pady=8,
            )
            theme_button.pack(side="right", padx=(0, 10))

        logout_button = tk.Button(
            top_panel,
            text="Logout",
            command=self._handle_logout,
            bg=Theme.get_card_color(),
            fg=Theme.get_text_color(),
            relief="flat",
            padx=12,
            pady=8,
        )
        logout_button.pack(side="right")

        content = tk.Frame(self.frame, bg=Theme.BG_COLOR, pady=12)
        content.pack(fill="both", expand=True)

        left_panel = tk.Frame(content, bg=Theme.CARD_COLOR, padx=18, pady=18)
        left_panel.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        right_panel = tk.Frame(content, bg=Theme.CARD_COLOR, padx=18, pady=18)
        right_panel.pack(side="right", fill="y", padx=12, pady=12)

        self.camera_label = tk.Label(left_panel, bg=Theme.CARD_COLOR)
        self.camera_label.pack(fill="both", expand=True)

        self.status_label = tk.Label(
            left_panel,
            text="Camera is offline.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(10, 0))

        self.start_button = tk.Button(
            right_panel,
            text="Start Camera",
            command=self._start_camera,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=12,
            pady=10,
            width=18,
        )
        self.start_button.pack(pady=(0, 12))

        self.stop_button = tk.Button(
            right_panel,
            text="Stop Camera",
            command=self._stop_camera,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=12,
            pady=10,
            width=18,
        )
        self.stop_button.pack(pady=(0, 12))

        self.blur_button = tk.Button(
            right_panel,
            text="Blur ON",
            command=self._toggle_blur,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=12,
            pady=10,
            width=18,
        )
        self.blur_button.pack(pady=(0, 12))

        self.camera_status = tk.Label(
            right_panel,
            text="Face blur is enabled.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            wraplength=180,
            justify="left",
        )
        self.camera_status.pack(pady=(10, 0))

    def show(self, username: str) -> None:
        self.current_user = username
        self.welcome_label.config(text=f"Welcome, {username}")
        self.frame.place(relwidth=1, relheight=1)
        self._stop_camera()

    def hide(self) -> None:
        self._stop_camera()
        self.frame.place_forget()

    def _start_camera(self) -> None:
        try:
            self.camera_handler.start_camera()
            self.logger.log("CAMERA", f"Camera permission granted for {self.current_user}")
            self.status_label.config(text="Camera is online.", fg=Theme.SUCCESS_COLOR)
            self._schedule_frame()
        except RuntimeError as error:
            messagebox.showerror("Camera Error", str(error))
            self.status_label.config(text="Unable to open camera.", fg=Theme.DANGER_COLOR)

    def _stop_camera(self) -> None:
        self.camera_handler.stop_camera()
        if self.video_job is not None:
            self.root.after_cancel(self.video_job)
            self.video_job = None
        self.camera_label.config(image="")
        self.status_label.config(text="Camera is offline.", fg=Theme.TEXT_COLOR)

    def _toggle_blur(self) -> None:
        self.camera_handler.blur_faces = not self.camera_handler.blur_faces
        blur_state = "ON" if self.camera_handler.blur_faces else "OFF"
        self.blur_button.config(text=f"Blur {blur_state}")
        self.camera_status.config(
            text=f"Face blur is {'enabled' if self.camera_handler.blur_faces else 'disabled'}."
        )
        self.logger.log("CAMERA", f"Face blur set to {blur_state} for {self.current_user}")

    def _schedule_frame(self) -> None:
        if not self.camera_handler.running:
            return
        frame = self.camera_handler.get_frame()
        if frame is not None:
            image = Image.fromarray(frame)
            image = image.resize((560, 380), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(image)
            self.camera_label.config(image=self.photo_image)
        self.video_job = self.root.after(30, self._schedule_frame)

    def on_theme_changed(self):
        """Handle theme changes"""
        self.frame.configure(bg=Theme.get_bg_color())
        self._update_ui_colors()

    def _update_ui_colors(self):
        """Update all UI colors when theme changes"""
        # Update main frame
        self.frame.configure(bg=Theme.get_bg_color())

        # Update top panel
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=Theme.get_panel_color())
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=Theme.get_panel_color(), fg=Theme.get_text_color())
                    elif isinstance(child, tk.Button):
                        if "Logout" in child.cget("text"):
                            child.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())
                        else:
                            child.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())

        # Update content area
        for widget in self.frame.winfo_children():
            if hasattr(widget, 'configure') and 'bg' in widget.configure():
                if "content" in str(widget):
                    widget.configure(bg=Theme.get_bg_color())

        # Update camera controls
        self._update_camera_control_colors()

    def _update_camera_control_colors(self):
        """Update camera control colors"""
        try:
            # Find the right panel and update its children
            for widget in self.frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):  # right_panel
                            child.configure(bg=Theme.get_card_color())
                            for button in child.winfo_children():
                                if isinstance(button, tk.Button):
                                    if "Start" in button.cget("text") or "Blur" in button.cget("text"):
                                        button.configure(bg=Theme.get_button_bg(), fg=Theme.get_text_color(),
                                                       activebackground=Theme.get_button_active())
                                    else:
                                        button.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())
                                elif isinstance(button, tk.Label):
                                    button.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())
        except:
            pass  # Ignore errors during theme updates

    def _handle_logout(self) -> None:
        self._stop_camera()
        self.on_logout()

    def _handle_theme_settings(self) -> None:
        if self.on_theme_settings:
            self.on_theme_settings()
