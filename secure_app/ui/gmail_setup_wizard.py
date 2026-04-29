import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
from pathlib import Path

from assets.theme import Theme


class GmailSetupWizard:
    def __init__(self, root: tk.Tk, on_complete, on_skip):
        self.root = root
        self.on_complete = on_complete
        self.on_skip = on_skip
        self.frame = tk.Frame(root, bg=Theme.get_bg_color())
        self.current_step = 0
        self.steps = [
            self._show_welcome,
            self._show_gmail_account,
            self._show_cloud_console,
            self._show_credentials,
            self._show_config,
            self._show_test
        ]

        # Register as theme observer
        from assets.theme import theme_manager
        theme_manager.add_observer(self)

        self._build_ui()

    def _build_ui(self):
        # Main container
        container = tk.Frame(self.frame, bg=Theme.PANEL_COLOR, padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        self.title_label = tk.Label(
            container,
            text="Gmail Setup Wizard",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=Theme.TITLE_FONT,
        )
        self.title_label.pack(pady=(0, 20))

        # Content frame
        self.content_frame = tk.Frame(container, bg=Theme.PANEL_COLOR)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Navigation buttons
        nav_frame = tk.Frame(container, bg=Theme.PANEL_COLOR)
        nav_frame.pack(fill="x", pady=(20, 0))

        self.back_button = tk.Button(
            nav_frame,
            text="Back",
            command=self._go_back,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        self.back_button.pack(side="left")

        self.skip_button = tk.Button(
            nav_frame,
            text="Skip Setup",
            command=self._skip_setup,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        self.skip_button.pack(side="left", padx=(10, 0))

        self.next_button = tk.Button(
            nav_frame,
            text="Next",
            command=self._go_next,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            activebackground=Theme.BUTTON_ACTIVE,
            relief="flat",
            padx=15,
            pady=8,
        )
        self.next_button.pack(side="right")

        self.finish_button = tk.Button(
            nav_frame,
            text="Finish",
            command=self._finish_setup,
            bg=Theme.SUCCESS_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )

        self._show_current_step()

    def _show_current_step(self):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show current step
        self.steps[self.current_step]()

        # Update navigation
        self.back_button.config(state="normal" if self.current_step > 0 else "disabled")
        self.next_button.pack(side="right" if self.current_step < len(self.steps) - 1 else "left", fill="none")
        self.finish_button.pack_forget()

        if self.current_step == len(self.steps) - 1:
            self.next_button.pack_forget()
            self.finish_button.pack(side="right")

    def _go_next(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._show_current_step()

    def _go_back(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._show_current_step()

    def _skip_setup(self):
        if messagebox.askyesno("Skip Setup", "Are you sure you want to skip Gmail setup? You can set it up later."):
            self.on_skip()

    def _finish_setup(self):
        self.on_complete()

    def _show_welcome(self):
        """Step 1: Welcome and introduction"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        desc = tk.Label(
            content,
            text="Welcome to Gmail OTP Setup!\n\n"
                 "This wizard will guide you through setting up email-based\n"
                 "OTP verification using Gmail. This provides an additional\n"
                 "secure way to receive verification codes.\n\n"
                 "The setup process involves:\n"
                 "• Creating/enabling a Gmail account\n"
                 "• Setting up Google Cloud Console\n"
                 "• Configuring API credentials\n"
                 "• Testing the integration",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
            wraplength=400,
        )
        desc.pack(pady=(0, 20))

        benefits_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        benefits_frame.pack(fill="x")

        benefits_title = tk.Label(
            benefits_frame,
            text="Benefits of Gmail OTP:",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            font=("Segoe UI", 12, "bold"),
        )
        benefits_title.pack(anchor="w", pady=(0, 10))

        benefits = tk.Label(
            benefits_frame,
            text="• Secure OAuth 2.0 authentication\n"
                 "• No app passwords needed\n"
                 "• Direct Gmail integration\n"
                 "• Automatic token refresh\n"
                 "• Reliable email delivery",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            justify="left",
            anchor="w",
        )
        benefits.pack(anchor="w")

    def _show_gmail_account(self):
        """Step 2: Gmail account setup"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        step_title = tk.Label(
            content,
            text="Step 1: Gmail Account Setup",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        step_title.pack(pady=(0, 20))

        desc = tk.Label(
            content,
            text="You need a Gmail account to send OTP emails.\n"
                 "If you don't have one, create it now.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
        )
        desc.pack(pady=(0, 20))

        # Gmail account status
        status_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        status_frame.pack(fill="x", pady=(0, 20))

        self.gmail_status = tk.Label(
            status_frame,
            text="Do you have a Gmail account?",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
        )
        self.gmail_status.pack(anchor="w", pady=(0, 10))

        button_frame = tk.Frame(status_frame, bg=Theme.CARD_COLOR)
        button_frame.pack(fill="x")

        create_button = tk.Button(
            button_frame,
            text="Create Gmail Account",
            command=self._open_gmail_signup,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=5,
        )
        create_button.pack(side="left")

        tk.Label(button_frame, text="   ", bg=Theme.CARD_COLOR).pack(side="left")

        self.have_account_button = tk.Button(
            button_frame,
            text="I Have Gmail Account",
            command=self._confirm_gmail_account,
            bg=Theme.SUCCESS_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=5,
        )
        self.have_account_button.pack(side="left")

        # Instructions
        instructions = tk.Label(
            content,
            text="Instructions:\n"
                 "1. Click 'Create Gmail Account' to open Gmail signup\n"
                 "2. Complete the account creation process\n"
                 "3. Return here and click 'I Have Gmail Account'\n"
                 "4. Make sure 2-factor authentication is enabled\n"
                 "   (required for Google Cloud Console)",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
            anchor="w",
        )
        instructions.pack(anchor="w", pady=(20, 0))

    def _show_cloud_console(self):
        """Step 3: Google Cloud Console setup"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        step_title = tk.Label(
            content,
            text="Step 2: Google Cloud Console Setup",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        step_title.pack(pady=(0, 20))

        desc = tk.Label(
            content,
            text="Now you need to set up Google Cloud Console to enable\n"
                 "Gmail API access for your application.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
        )
        desc.pack(pady=(0, 20))

        # Cloud Console steps
        steps_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        steps_frame.pack(fill="x", pady=(0, 20))

        steps_title = tk.Label(
            steps_frame,
            text="Follow these steps:",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            font=("Segoe UI", 12, "bold"),
        )
        steps_title.pack(anchor="w", pady=(0, 10))

        steps_text = tk.Label(
            steps_frame,
            text="1. Go to Google Cloud Console\n"
                 "2. Create a new project (or select existing)\n"
                 "3. Enable Gmail API\n"
                 "4. Create OAuth 2.0 credentials\n"
                 "5. Download credentials.json file",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            justify="left",
            anchor="w",
        )
        steps_text.pack(anchor="w")

        button_frame = tk.Frame(content, bg=Theme.PANEL_COLOR)
        button_frame.pack(fill="x", pady=(0, 20))

        cloud_button = tk.Button(
            button_frame,
            text="Open Google Cloud Console",
            command=self._open_cloud_console,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        cloud_button.pack(side="left")

        tk.Label(button_frame, text="   ", bg=Theme.PANEL_COLOR).pack(side="left")

        self.cloud_done_button = tk.Button(
            button_frame,
            text="I've Completed Cloud Setup",
            command=self._confirm_cloud_setup,
            bg=Theme.SUCCESS_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        self.cloud_done_button.pack(side="left")

        # Detailed instructions
        detailed_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        detailed_frame.pack(fill="x")

        detailed_title = tk.Label(
            detailed_frame,
            text="Detailed Instructions:",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            font=("Segoe UI", 12, "bold"),
        )
        detailed_title.pack(anchor="w", pady=(0, 10))

        detailed_text = tk.Label(
            detailed_frame,
            text="• Project: Create new or select existing\n"
                 "• API: Search for 'Gmail API' and enable it\n"
                 "• Credentials: Create 'OAuth 2.0 Client IDs'\n"
                 "• Application type: 'Desktop application'\n"
                 "• Download: Save as 'credentials.json'",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            justify="left",
            anchor="w",
        )
        detailed_text.pack(anchor="w")

    def _show_credentials(self):
        """Step 4: Credentials file setup"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        step_title = tk.Label(
            content,
            text="Step 3: Credentials File",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        step_title.pack(pady=(0, 20))

        desc = tk.Label(
            content,
            text="You need to place the credentials.json file in the\n"
                 "application directory for Gmail API access.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
        )
        desc.pack(pady=(0, 20))

        # File status
        status_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        status_frame.pack(fill="x", pady=(0, 20))

        self.credentials_status = tk.Label(
            status_frame,
            text="Credentials file status: Not found",
            fg=Theme.DANGER_COLOR,
            bg=Theme.CARD_COLOR,
        )
        self.credentials_status.pack(anchor="w", pady=(0, 10))

        button_frame = tk.Frame(status_frame, bg=Theme.CARD_COLOR)
        button_frame.pack(fill="x")

        select_button = tk.Button(
            button_frame,
            text="Select credentials.json",
            command=self._select_credentials_file,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=5,
        )
        select_button.pack(side="left")

        tk.Label(button_frame, text="   ", bg=Theme.CARD_COLOR).pack(side="left")

        self.check_button = tk.Button(
            button_frame,
            text="Check File",
            command=self._check_credentials_file,
            bg=Theme.CARD_COLOR,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=5,
        )
        self.check_button.pack(side="left")

        # Instructions
        instructions = tk.Label(
            content,
            text="Instructions:\n"
                 "1. Locate the credentials.json file you downloaded\n"
                 "2. Click 'Select credentials.json' to choose the file\n"
                 "3. The file will be copied to the application directory\n"
                 "4. Click 'Check File' to verify it's properly placed",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
            anchor="w",
        )
        instructions.pack(anchor="w", pady=(20, 0))

    def _show_config(self):
        """Step 5: Configuration"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        step_title = tk.Label(
            content,
            text="Step 4: Configuration",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        step_title.pack(pady=(0, 20))

        desc = tk.Label(
            content,
            text="Now we'll configure the application to use Gmail API\n"
                 "for sending OTP emails.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
        )
        desc.pack(pady=(0, 20))

        # Config status
        config_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        config_frame.pack(fill="x", pady=(0, 20))

        self.config_status = tk.Label(
            config_frame,
            text="Configuration status: Ready to configure",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
        )
        self.config_status.pack(anchor="w", pady=(0, 10))

        config_button = tk.Button(
            config_frame,
            text="Configure Gmail API",
            command=self._configure_gmail_api,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        config_button.pack(anchor="w")

        # What happens next
        info_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        info_frame.pack(fill="x")

        info_title = tk.Label(
            info_frame,
            text="What happens next:",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            font=("Segoe UI", 12, "bold"),
        )
        info_title.pack(anchor="w", pady=(0, 10))

        info_text = tk.Label(
            info_frame,
            text="• Configuration file will be updated\n"
                 "• Gmail API will be enabled\n"
                 "• OAuth consent flow will run (opens browser)\n"
                 "• Authentication tokens will be saved",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
            justify="left",
            anchor="w",
        )
        info_text.pack(anchor="w")

    def _show_test(self):
        """Step 6: Testing"""
        content = tk.Frame(self.content_frame, bg=Theme.PANEL_COLOR)
        content.pack(fill="both", expand=True)

        step_title = tk.Label(
            content,
            text="Step 5: Test Integration",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        step_title.pack(pady=(0, 20))

        desc = tk.Label(
            content,
            text="Let's test that Gmail OTP integration is working properly.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.PANEL_COLOR,
            justify="left",
        )
        desc.pack(pady=(0, 20))

        # Test status
        test_frame = tk.Frame(content, bg=Theme.CARD_COLOR, padx=15, pady=15)
        test_frame.pack(fill="x", pady=(0, 20))

        self.test_status = tk.Label(
            test_frame,
            text="Test status: Ready to test",
            fg=Theme.TEXT_COLOR,
            bg=Theme.CARD_COLOR,
        )
        self.test_status.pack(anchor="w", pady=(0, 10))

        test_button = tk.Button(
            test_frame,
            text="Test Gmail OTP",
            command=self._test_gmail_otp,
            bg=Theme.BUTTON_BG,
            fg=Theme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=8,
        )
        test_button.pack(anchor="w")

        # Completion message
        completion_frame = tk.Frame(content, bg=Theme.SUCCESS_COLOR, padx=15, pady=15)
        completion_frame.pack(fill="x")

        completion_title = tk.Label(
            completion_frame,
            text="🎉 Setup Complete!",
            fg=Theme.TEXT_COLOR,
            bg=Theme.SUCCESS_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        completion_title.pack(anchor="w", pady=(0, 10))

        completion_text = tk.Label(
            completion_frame,
            text="Gmail OTP is now configured and ready to use.\n"
                 "Users can now receive OTP codes via email in addition\n"
                 "to QR codes and displayed codes.",
            fg=Theme.TEXT_COLOR,
            bg=Theme.SUCCESS_COLOR,
            justify="left",
            anchor="w",
        )
        completion_text.pack(anchor="w")

    # Action methods
    def _open_gmail_signup(self):
        webbrowser.open("https://accounts.google.com/signup")

    def _confirm_gmail_account(self):
        messagebox.showinfo("Gmail Account",
                          "Great! Make sure your Gmail account has 2-factor authentication enabled.\n"
                          "This is required for Google Cloud Console access.")

    def _open_cloud_console(self):
        webbrowser.open("https://console.cloud.google.com/")

    def _confirm_cloud_setup(self):
        messagebox.showinfo("Cloud Console",
                          "Perfect! Now make sure you have:\n"
                          "• Created/enabled a project\n"
                          "• Enabled Gmail API\n"
                          "• Created OAuth 2.0 credentials\n"
                          "• Downloaded credentials.json")

    def _select_credentials_file(self):
        file_path = filedialog.askopenfilename(
            title="Select credentials.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Copy file to app directory
                import shutil
                app_dir = Path(__file__).resolve().parent.parent
                dest_path = app_dir / "credentials.json"
                shutil.copy2(file_path, dest_path)
                self._check_credentials_file()
                messagebox.showinfo("Success", "credentials.json has been copied to the application directory!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy file: {e}")

    def _check_credentials_file(self):
        app_dir = Path(__file__).resolve().parent.parent
        credentials_path = app_dir / "credentials.json"
        if credentials_path.exists():
            self.credentials_status.config(
                text="Credentials file status: Found and ready",
                fg=Theme.SUCCESS_COLOR
            )
        else:
            self.credentials_status.config(
                text="Credentials file status: Not found",
                fg=Theme.DANGER_COLOR
            )

    def _configure_gmail_api(self):
        try:
            # Update config file
            config_path = Path(__file__).resolve().parent.parent / "email_config.txt"
            config_content = f"""# Email Configuration for OTP
# Gmail API has been configured automatically

EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com

# Gmail API Configuration
USE_GMAIL_API=true
CREDENTIALS_PATH=credentials.json
TOKEN_PATH=token.json
"""
            with open(config_path, 'w') as f:
                f.write(config_content)

            self.config_status.config(
                text="Configuration status: Gmail API enabled",
                fg=Theme.SUCCESS_COLOR
            )
            messagebox.showinfo("Configuration Complete",
                              "Gmail API has been enabled in the configuration.\n"
                              "The OAuth flow will run when you first use email OTP.")

        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to update configuration: {e}")

    def _test_gmail_otp(self):
        try:
            from auth.otp import OTPManager
            otp_manager = OTPManager()

            # Test with a dummy email
            test_email = "test@example.com"
            test_username = "TestUser"
            test_otp = "123456"

            if otp_manager.send_otp_email(test_email, test_username, test_otp):
                self.test_status.config(
                    text="Test status: Email sent successfully!",
                    fg=Theme.SUCCESS_COLOR
                )
                messagebox.showinfo("Test Successful",
                                  "Gmail OTP integration is working!\n"
                                  "Check the activity.log for details.")
            else:
                self.test_status.config(
                    text="Test status: Email failed (check configuration)",
                    fg=Theme.DANGER_COLOR
                )
                messagebox.showwarning("Test Failed",
                                     "Email sending failed. Check your configuration and try again.")

        except Exception as e:
            self.test_status.config(
                text=f"Test status: Error - {e}",
                fg=Theme.DANGER_COLOR
            )
            messagebox.showerror("Test Error", f"Testing failed: {e}")

    def on_theme_changed(self):
        """Handle theme changes"""
        self.frame.configure(bg=Theme.get_bg_color())
        self._update_ui_colors()

    def _update_ui_colors(self):
        """Update all UI colors when theme changes"""
        # Update main frame
        self.frame.configure(bg=Theme.get_bg_color())

        # Update container and all children recursively
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=Theme.get_panel_color())
                self._update_widget_colors(widget)

    def _update_widget_colors(self, parent_widget):
        """Recursively update colors of all child widgets"""
        for child in parent_widget.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=Theme.get_panel_color())
                self._update_widget_colors(child)
            elif isinstance(child, tk.Label):
                child.configure(bg=Theme.get_panel_color(), fg=Theme.get_text_color())
            elif isinstance(child, tk.Button):
                child.configure(bg=Theme.get_button_bg(), fg=Theme.get_text_color(),
                              activebackground=Theme.get_button_active())
            elif isinstance(child, tk.Entry):
                child.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color(),
                              insertbackground=Theme.get_text_color())

    def show(self):
        self.frame.place(relwidth=1, relheight=1)
        self.current_step = 0
        self._show_current_step()

    def hide(self):
        self.frame.place_forget()