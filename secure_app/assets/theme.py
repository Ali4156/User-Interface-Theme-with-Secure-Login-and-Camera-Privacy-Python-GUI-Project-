import tkinter as tk
from typing import Dict, Any


class ThemeManager:
    def __init__(self):
        self.themes = {
            "dark": {
                "name": "Dark Mode",
                "bg_color": "#111424",
                "panel_color": "#1f2640",
                "card_color": "#252f4b",
                "text_color": "#e7eaf3",
                "highlight_color": "#5d7fff",
                "danger_color": "#ff5f7a",
                "success_color": "#3ccf91",
                "entry_bg": "#171f34",
                "entry_border": "#3e4c7d",
                "button_bg": "#4f6dff",
                "button_active": "#7288ff",
                "font": ("Segoe UI", 11),
                "title_font": ("Segoe UI", 16, "bold"),
                "border_radius": 8,
                "shadow_color": "#000000",
            },
            "light": {
                "name": "Light Mode",
                "bg_color": "#f8f9fa",
                "panel_color": "#ffffff",
                "card_color": "#f1f3f4",
                "text_color": "#202124",
                "highlight_color": "#1a73e8",
                "danger_color": "#ea4335",
                "success_color": "#34a853",
                "entry_bg": "#ffffff",
                "entry_border": "#dadce0",
                "button_bg": "#1a73e8",
                "button_active": "#1557b0",
                "font": ("Segoe UI", 11),
                "title_font": ("Segoe UI", 16, "bold"),
                "border_radius": 8,
                "shadow_color": "#000000",
            },
            "custom": {
                "name": "Custom Mode",
                "bg_color": "#111424",
                "panel_color": "#1f2640",
                "card_color": "#252f4b",
                "text_color": "#e7eaf3",
                "highlight_color": "#5d7fff",
                "danger_color": "#ff5f7a",
                "success_color": "#3ccf91",
                "entry_bg": "#171f34",
                "entry_border": "#3e4c7d",
                "button_bg": "#4f6dff",
                "button_active": "#7288ff",
                "font": ("Segoe UI", 11),
                "title_font": ("Segoe UI", 16, "bold"),
                "border_radius": 8,
                "shadow_color": "#000000",
            }
        }
        self.current_theme = "dark"
        self.custom_colors = {}
        self.observers = []

    def add_observer(self, observer):
        """Add observer to be notified of theme changes"""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove theme change observer"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        """Notify all observers of theme change"""
        for observer in self.observers:
            if hasattr(observer, 'on_theme_changed'):
                observer.on_theme_changed()

    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.notify_observers()

    def get_current_theme(self) -> Dict[str, Any]:
        """Get the current theme configuration"""
        return self.themes[self.current_theme]

    def update_custom_color(self, color_key: str, color_value: str):
        """Update a custom theme color"""
        if self.current_theme == "custom":
            self.themes["custom"][color_key] = color_value
            self.notify_observers()

    def get_color(self, color_key: str) -> str:
        """Get a color value from current theme"""
        theme = self.get_current_theme()
        return theme.get(color_key, "#000000")

    def get_font(self, font_key: str = "font"):
        """Get a font from current theme"""
        theme = self.get_current_theme()
        return theme.get(font_key, ("Segoe UI", 11))

    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())

    def get_theme_display_name(self, theme_name: str) -> str:
        """Get display name for a theme"""
        return self.themes.get(theme_name, {}).get("name", theme_name.title())

    def create_gradient_bg(self, widget, color1: str, color2: str):
        """Create a gradient background effect"""
        # This would require canvas implementation for true gradients
        # For now, return solid color
        return color1

    def apply_shadow_effect(self, widget):
        """Apply shadow effect to widget"""
        # Placeholder for shadow effects
        pass


# Global theme manager instance
theme_manager = ThemeManager()

# Backward compatibility - keep old Theme class for existing code
class Theme:
    @staticmethod
    def get_bg_color():
        return theme_manager.get_color("bg_color")

    @staticmethod
    def get_panel_color():
        return theme_manager.get_color("panel_color")

    @staticmethod
    def get_card_color():
        return theme_manager.get_color("card_color")

    @staticmethod
    def get_text_color():
        return theme_manager.get_color("text_color")

    @staticmethod
    def get_highlight_color():
        return theme_manager.get_color("highlight_color")

    @staticmethod
    def get_danger_color():
        return theme_manager.get_color("danger_color")

    @staticmethod
    def get_success_color():
        return theme_manager.get_color("success_color")

    @staticmethod
    def get_entry_bg():
        return theme_manager.get_color("entry_bg")

    @staticmethod
    def get_entry_border():
        return theme_manager.get_color("entry_border")

    @staticmethod
    def get_button_bg():
        return theme_manager.get_color("button_bg")

    @staticmethod
    def get_button_active():
        return theme_manager.get_color("button_active")

    @staticmethod
    def get_font():
        return theme_manager.get_font("font")

    @staticmethod
    def get_title_font():
        return theme_manager.get_font("title_font")

    # Keep old constants for backward compatibility
    BG_COLOR = "#111424"
    PANEL_COLOR = "#1f2640"
    CARD_COLOR = "#252f4b"
    TEXT_COLOR = "#e7eaf3"
    HIGHLIGHT_COLOR = "#5d7fff"
    DANGER_COLOR = "#ff5f7a"
    SUCCESS_COLOR = "#3ccf91"
    ENTRY_BG = "#171f34"
    ENTRY_BORDER = "#3e4c7d"
    BUTTON_BG = "#4f6dff"
    BUTTON_ACTIVE = "#7288ff"
    FONT = ("Segoe UI", 11)
    TITLE_FONT = ("Segoe UI", 16, "bold")
