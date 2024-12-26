import customtkinter as ctk
import tkinter as tk
from keyauth import api
import time
import sys
from config import *
import threading
import tkinter.messagebox as messagebox

class LoaderApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.title(WINDOW_TITLE)
        self.window.configure(fg_color=BACKGROUND_COLOR)
        self.window.resizable(False, False)
        
        # Initialize KeyAuth
        self.keyauth = api(
            name=KEYAUTH_NAME,
            ownerid=KEYAUTH_OWNERID,
            secret=KEYAUTH_SECRET,
            version="1.0"
        )
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Logo label (can be replaced with an image)
        self.logo_label = ctk.CTkLabel(
            self.main_frame,
            text="SECURE LOADER",
            font=("Roboto", 24, "bold"),
            text_color=ACCENT_COLOR
        )
        self.logo_label.pack(pady=20)
        
        # Login frame
        self.login_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=BACKGROUND_COLOR
        )
        self.login_frame.pack(pady=20)
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
            width=250,
            height=40,
            border_color=ACCENT_COLOR,
            fg_color="#2a2a2a"
        )
        self.username_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Password",
            width=250,
            height=40,
            border_color=ACCENT_COLOR,
            fg_color="#2a2a2a",
            show="•"
        )
        self.password_entry.pack(pady=10)
        
        # Key entry
        self.key_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="License Key",
            width=250,
            height=40,
            border_color=ACCENT_COLOR,
            fg_color="#2a2a2a"
        )
        self.key_entry.pack(pady=10)
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="LOGIN",
            width=250,
            height=40,
            fg_color=ACCENT_COLOR,
            hover_color="#5269a7",
            command=self.login
        )
        self.login_button.pack(pady=20)
        
        # Loading bar (hidden by default)
        self.progress_bar = ctk.CTkProgressBar(
            self.login_frame,
            width=250,
            height=15,
            fg_color="#2a2a2a",
            progress_color=ACCENT_COLOR
        )
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color=TEXT_COLOR
        )
        self.status_label.pack(pady=10)
        
    def animate_loading(self):
        self.progress_bar.pack(pady=10)
        for i in range(101):
            if not hasattr(self, 'loading'):
                break
            self.progress_bar.set(i / 100)
            time.sleep(0.03)
        if hasattr(self, 'loading'):
            self.progress_bar.pack_forget()
            
    def login(self):
        self.login_button.configure(state="disabled")
        self.status_label.configure(text="Authenticating...", text_color=ACCENT_COLOR)
        
        # Start loading animation
        self.loading = True
        threading.Thread(target=self.animate_loading, daemon=True).start()
        
        # Get input values
        username = self.username_entry.get()
        password = self.password_entry.get()
        key = self.key_entry.get()
        
        try:
            # Attempt login with KeyAuth
            self.keyauth.login(username, password, key)
            
            # Stop loading animation
            if hasattr(self, 'loading'):
                delattr(self, 'loading')
            
            self.status_label.configure(text="Login successful!", text_color=SUCCESS_COLOR)
            self.window.after(1000, self.on_login_success)
            
        except Exception as e:
            if hasattr(self, 'loading'):
                delattr(self, 'loading')
            self.status_label.configure(text=f"Login failed: {str(e)}", text_color=ERROR_COLOR)
            self.login_button.configure(state="normal")
            
    def on_login_success(self):
        # Hide main window
        self.window.withdraw()
        
        # Show success popup
        success_window = ctk.CTkToplevel()
        success_window.title("Success")
        success_window.geometry("300x150")
        success_window.configure(fg_color=BACKGROUND_COLOR)
        
        # Center the window
        success_window.update_idletasks()
        x = (success_window.winfo_screenwidth() - success_window.winfo_width()) // 2
        y = (success_window.winfo_screenheight() - success_window.winfo_height()) // 2
        success_window.geometry(f"+{x}+{y}")
        
        # Success message
        success_label = ctk.CTkLabel(
            success_window,
            text="Logged in Successfully",
            font=("Roboto", 18, "bold"),
            text_color=SUCCESS_COLOR
        )
        success_label.pack(expand=True)
        
        # Close button
        close_button = ctk.CTkButton(
            success_window,
            text="Close",
            command=lambda: self.close_app(success_window),
            fg_color=ACCENT_COLOR,
            hover_color="#5269a7"
        )
        close_button.pack(pady=20)
        
        success_window.protocol("WM_DELETE_WINDOW", lambda: self.close_app(success_window))
        
    def close_app(self, window):
        window.destroy()
        sys.exit()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = LoaderApp()
    app.run() 