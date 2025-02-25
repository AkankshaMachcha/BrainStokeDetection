import tkinter as tk
from tkinter import ttk
from patient_panel import PatientPanel
from admin_panel import AdminPanel

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Stroke Detection")
        self.root.geometry("800x600")
        self.root.configure(bg="#e3f2fd")  # Light blue background
        
        self.show_login_screen()

    def show_login_screen(self):
        # Create a frame for login
        login_frame = tk.Frame(self.root, bg="#e3f2fd")
        login_frame.pack(pady=100)

        # Title label
        title_label = tk.Label(
            login_frame, 
            text="🧠 Brain Stroke Detection 🏥", 
            font=("Arial", 22, "bold"), 
            fg="#1565c0", 
            bg="#e3f2fd"
        )
        title_label.pack(pady=20)

        # Button styling
        btn_style = {
            "font": ("Arial", 14, "bold"),
            "width": 20,
            "height": 2,
            "relief": "raised",
            "borderwidth": 3,
            "activebackground": "#ffb74d",
            "activeforeground": "black"
        }

        # Patient button
        patient_btn = tk.Button(
            login_frame, 
            text="🩺 Patient Panel", 
            command=self.open_patient_panel, 
            bg="#1e88e5", 
            fg="white", 
            **btn_style
        )
        patient_btn.pack(pady=15)

        # Admin button
        admin_btn = tk.Button(
            login_frame, 
            text="🔑 Admin Panel", 
            command=self.open_admin_panel, 
            bg="#d32f2f", 
            fg="white", 
            **btn_style
        )
        admin_btn.pack(pady=15)

        # Footer message
        footer_label = tk.Label(
            login_frame, 
            text="Stay Safe & Healthy! ❤️", 
            font=("Arial", 12, "italic"), 
            fg="#880e4f", 
            bg="#e3f2fd"
        )
        footer_label.pack(pady=20)

    def open_patient_panel(self):
        self.root.destroy()  # Destroy the current window
        patient_window = tk.Tk()
        PatientPanel(patient_window)
    
    def open_admin_panel(self):
        self.root.destroy()
        admin_window = tk.Tk()
        AdminPanel(admin_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
