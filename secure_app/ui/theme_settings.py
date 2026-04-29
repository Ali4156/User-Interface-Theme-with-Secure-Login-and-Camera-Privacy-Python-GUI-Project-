import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from assets.theme import theme_manager, Theme


class ThemeSettingsUI:
    def __init__(self, root: tk.Tk, on_close=None):
        self.root = root
        self.on_close = on_close
        self.window = tk.Toplevel(root)
        self.window.title("Theme Settings")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.configure(bg=Theme.get_bg_color())

        # Register as theme observer
        theme_manager.add_observer(self)

        self._build_ui()
        self._load_current_settings()

        # Center the window
        self.window.transient(root)
        self.window.grab_set()

    def on_theme_changed(self):
        """Handle theme changes"""
        self.window.configure(bg=Theme.get_bg_color())
        self._update_ui_colors()

    def _update_ui_colors(self):
        """Update all UI colors when theme changes"""
        self.window.configure(bg=Theme.get_bg_color())

        # Update main container
        self.main_container.configure(bg=Theme.get_panel_color())

        # Update title
        self.title_label.configure(bg=Theme.get_panel_color(), fg=Theme.get_text_color())

        # Update theme selector frame
        self.theme_frame.configure(bg=Theme.get_card_color())
        self.theme_label.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())

        # Update custom colors frame
        self.custom_frame.configure(bg=Theme.get_card_color())
        self.custom_label.configure(bg=Theme.get_card_color(), fg=Theme.get_text_color())

        # Update buttons
        for button in [self.apply_button, self.reset_button, self.close_button]:
            button.configure(
                bg=Theme.get_button_bg(),
                fg=Theme.get_text_color(),
                activebackground=Theme.get_button_active()
            )

        # Update color entry fields
        for entry in self.color_entries.values():
            entry.configure(
                bg=Theme.get_entry_bg(),
                fg=Theme.get_text_color(),
                insertbackground=Theme.get_text_color()
            )

    def _build_ui(self):
        # Main container
        self.main_container = tk.Frame(self.window, bg=Theme.get_panel_color(), padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)

        # Title
        self.title_label = tk.Label(
            self.main_container,
            text="🎨 Theme Settings",
            font=Theme.get_title_font(),
            bg=Theme.get_panel_color(),
            fg=Theme.get_text_color()
        )
        self.title_label.pack(pady=(0, 20))

        # Theme selector
        self.theme_frame = tk.Frame(self.main_container, bg=Theme.get_card_color(), padx=15, pady=15)
        self.theme_frame.pack(fill="x", pady=(0, 15))

        self.theme_label = tk.Label(
            self.theme_frame,
            text="Select Theme:",
            font=("Segoe UI", 12, "bold"),
            bg=Theme.get_card_color(),
            fg=Theme.get_text_color()
        )
        self.theme_label.pack(anchor="w", pady=(0, 10))

        # Theme selection
        self.theme_var = tk.StringVar(value=theme_manager.current_theme)
        theme_container = tk.Frame(self.theme_frame, bg=Theme.get_card_color())
        theme_container.pack(fill="x")

        self.theme_buttons = {}
        themes = theme_manager.get_available_themes()
        for i, theme_name in enumerate(themes):
            display_name = theme_manager.get_theme_display_name(theme_name)
            rb = tk.Radiobutton(
                theme_container,
                text=display_name,
                variable=self.theme_var,
                value=theme_name,
                command=self._on_theme_selected,
                bg=Theme.get_card_color(),
                fg=Theme.get_text_color(),
                selectcolor=Theme.get_card_color(),
                activebackground=Theme.get_card_color(),
                activeforeground=Theme.get_text_color()
            )
            rb.pack(anchor="w", pady=2)
            self.theme_buttons[theme_name] = rb

        # Custom colors section
        self.custom_frame = tk.Frame(self.main_container, bg=Theme.get_card_color(), padx=15, pady=15)
        self.custom_frame.pack(fill="x", pady=(0, 20))

        self.custom_label = tk.Label(
            self.custom_frame,
            text="Customize Colors (Custom Mode Only):",
            font=("Segoe UI", 12, "bold"),
            bg=Theme.get_card_color(),
            fg=Theme.get_text_color()
        )
        self.custom_label.pack(anchor="w", pady=(0, 15))

        # Color customization grid
        colors_frame = tk.Frame(self.custom_frame, bg=Theme.get_card_color())
        colors_frame.pack(fill="x")

        self.color_entries = {}
        self.color_buttons = {}

        color_configs = [
            ("Background", "bg_color"),
            ("Panel", "panel_color"),
            ("Card", "card_color"),
            ("Text", "text_color"),
            ("Button", "button_bg"),
            ("Success", "success_color"),
            ("Danger", "danger_color"),
            ("Highlight", "highlight_color"),
        ]

        for i, (label, key) in enumerate(color_configs):
            row = i // 2
            col = i % 2

            # Label
            lbl = tk.Label(
                colors_frame,
                text=f"{label}:",
                bg=Theme.get_card_color(),
                fg=Theme.get_text_color(),
                width=10,
                anchor="w"
            )
            lbl.grid(row=row, column=col*3, padx=(0, 5), pady=5, sticky="w")

            # Entry
            entry = tk.Entry(
                colors_frame,
                width=12,
                bg=Theme.get_entry_bg(),
                fg=Theme.get_text_color(),
                insertbackground=Theme.get_text_color()
            )
            entry.grid(row=row, column=col*3+1, padx=(0, 5), pady=5)
            self.color_entries[key] = entry

            # Color picker button
            btn = tk.Button(
                colors_frame,
                text="🎨",
                width=3,
                command=lambda k=key: self._pick_color(k),
                bg=Theme.get_button_bg(),
                fg=Theme.get_text_color()
            )
            btn.grid(row=row, column=col*3+2, pady=5)
            self.color_buttons[key] = btn

        # Buttons
        buttons_frame = tk.Frame(self.main_container, bg=Theme.get_panel_color())
        buttons_frame.pack(fill="x", pady=(20, 0))

        self.apply_button = tk.Button(
            buttons_frame,
            text="Apply Changes",
            command=self._apply_changes,
            bg=Theme.get_button_bg(),
            fg=Theme.get_text_color(),
            activebackground=Theme.get_button_active(),
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )
        self.apply_button.pack(side="left", padx=(0, 10))

        self.reset_button = tk.Button(
            buttons_frame,
            text="Reset to Default",
            command=self._reset_custom_theme,
            bg=Theme.get_card_color(),
            fg=Theme.get_text_color(),
            padx=20,
            pady=8
        )
        self.reset_button.pack(side="left", padx=(0, 10))

        self.close_button = tk.Button(
            buttons_frame,
            text="Close",
            command=self._close,
            bg=Theme.get_card_color(),
            fg=Theme.get_text_color(),
            padx=20,
            pady=8
        )
        self.close_button.pack(side="right")

    def _load_current_settings(self):
        """Load current theme settings into UI"""
        # Set current theme
        self.theme_var.set(theme_manager.current_theme)

        # Load custom colors
        if theme_manager.current_theme == "custom":
            current_theme = theme_manager.get_current_theme()
            for key, entry in self.color_entries.items():
                color = current_theme.get(key, "")
                entry.delete(0, tk.END)
                entry.insert(0, color)

        self._update_custom_colors_visibility()

    def _on_theme_selected(self):
        """Handle theme selection"""
        selected_theme = self.theme_var.get()
        theme_manager.set_theme(selected_theme)
        self._update_custom_colors_visibility()

    def _update_custom_colors_visibility(self):
        """Show/hide custom colors based on selected theme"""
        is_custom = self.theme_var.get() == "custom"
        state = "normal" if is_custom else "disabled"

        for entry in self.color_entries.values():
            entry.config(state=state)

        for button in self.color_buttons.values():
            button.config(state=state)

        if is_custom:
            # Load custom colors
            current_theme = theme_manager.get_current_theme()
            for key, entry in self.color_entries.items():
                color = current_theme.get(key, "")
                entry.delete(0, tk.END)
                entry.insert(0, color)

    def _pick_color(self, color_key):
        """Open color picker for a specific color"""
        current_color = self.color_entries[color_key].get()
        try:
            # Try to parse current color
            if current_color.startswith("#"):
                initial_color = current_color
            else:
                initial_color = "#ffffff"
        except:
            initial_color = "#ffffff"

        color = colorchooser.askcolor(title=f"Choose {color_key.replace('_', ' ').title()} Color",
                                     initialcolor=initial_color)
        if color and color[1]:
            self.color_entries[color_key].delete(0, tk.END)
            self.color_entries[color_key].insert(0, color[1])

    def _apply_changes(self):
        """Apply the current settings"""
        selected_theme = self.theme_var.get()

        if selected_theme == "custom":
            # Update custom colors
            for key, entry in self.color_entries.items():
                color_value = entry.get().strip()
                if color_value:
                    theme_manager.update_custom_color(key, color_value)

        theme_manager.set_theme(selected_theme)
        messagebox.showinfo("Success", "Theme settings applied successfully!")

    def _reset_custom_theme(self):
        """Reset custom theme to default dark theme"""
        if messagebox.askyesno("Reset Custom Theme",
                              "This will reset all custom colors to the default dark theme. Continue?"):
            # Reset custom theme to dark theme defaults
            dark_theme = theme_manager.themes["dark"].copy()
            theme_manager.themes["custom"] = dark_theme
            theme_manager.themes["custom"]["name"] = "Custom Mode"

            if theme_manager.current_theme == "custom":
                theme_manager.notify_observers()

            self._load_current_settings()
            messagebox.showinfo("Reset Complete", "Custom theme has been reset to default.")

    def _close(self):
        """Close the settings window"""
        theme_manager.remove_observer(self)
        self.window.destroy()
        if self.on_close:
            self.on_close()