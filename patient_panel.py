import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import sqlite3
import chatbot

class PatientPanel:
    def __init__(self, master):
        self.master = master
        self.master.title("Patient Panel")
        self.master.geometry("700x600")
        self.master.configure(bg='#f2f2f2')
        self.main_frame = None
        self.image_path = None
        self.create_database()
        self.show_main_menu()

    def create_database(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        db_path = os.path.join('data', 'users_data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE,
                date TEXT NOT NULL,
                address TEXT NOT NULL,
                mobile TEXT NOT NULL UNIQUE,
                image_path TEXT NOT NULL,
                feedback TEXT DEFAULT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def show_main_menu(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        
        # Main frame with background color
        self.main_frame = tk.Frame(self.master, bg="#ffebcd")  # Light peach background
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label with stylish font and color
        title_label = tk.Label(
            self.main_frame, 
            text="🩺 Patient Panel 🏥", 
            font=("Arial", 26, 'bold'), 
            fg="#4a148c", 
            bg="#ffebcd"
        )
        title_label.grid(row=0, column=0, pady=20, columnspan=2)

        # Define button style
        btn_style = {
            "font": ("Arial", 14, "bold"),
            "width": 25,
            "height": 2,
            "relief": "raised",
            "borderwidth": 3,
            "activebackground": "#ffc107",
            "activeforeground": "black"
        }

        # Buttons with colors and icons
        chatbot_btn = tk.Button(
            self.main_frame, 
            text="💬 Chatbot", 
            command=self.open_chatbot, 
            bg="#1e88e5", 
            fg="white", 
            **btn_style
        )
        chatbot_btn.grid(row=1, column=0, pady=10, padx=10)

        upload_btn = tk.Button(
            self.main_frame, 
            text="📤 Upload Data & Image", 
            command=self.open_upload_window, 
            bg="#43a047", 
            fg="white", 
            **btn_style
        )
        upload_btn.grid(row=1, column=1, pady=10, padx=10)

        feedback_btn = tk.Button(
            self.main_frame, 
            text="📄 View Data & Feedback", 
            command=self.open_feedback_window, 
            bg="#d32f2f", 
            fg="white", 
            **btn_style
        )
        feedback_btn.grid(row=2, column=0, pady=10, padx=10, columnspan=2)

        # Adding a decorative footer label
        footer_label = tk.Label(
            self.main_frame, 
            text="✨ Stay Healthy & Take Care ✨", 
            font=("Arial", 14, "italic"), 
            fg="#880e4f", 
            bg="#ffebcd"
        )
        footer_label.grid(row=3, column=0, columnspan=2, pady=20)

    def open_chatbot(self):
        chatbot_window = tk.Toplevel(self.master)
        chatbot.Chatbot(chatbot_window)

    
    

    def open_upload_window(self):
        upload_window = tk.Toplevel(self.master)
        upload_window.title("Upload Data & Image")
        upload_window.geometry("700x600")
        upload_window.configure(bg="#ffebcd")  # Light peach background

        frame = ttk.Frame(upload_window, padding="20")
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(frame, text="Upload Patient Data & Image", font=("Arial", 18, "bold"), fg="#4a148c", bg="#ffebcd")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Name", "Age", "Email", "Date", "Address", "Mobile No."]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", font=("Arial", 12, "bold"), fg="#880e4f", bg="#ffebcd").grid(row=i + 1, column=0, pady=5, sticky="w", padx=10)
            entry = tk.Entry(frame, width=40, font=("Arial", 12), bg="#fff3e0", fg="#311b92", highlightbackground="#6a1b9a", highlightthickness=1)
            entry.grid(row=i + 1, column=1, pady=5, padx=10)
            self.entries[label] = entry

        upload_btn = tk.Button(frame, text="📤 Upload Image", command=self.upload_image, width=25, bg="#ff6f00", fg="black", font=("Arial", 12, "bold"), relief="raised", activebackground="#ff9800")
        upload_btn.grid(row=7, column=0, pady=20, padx=10)

        submit_btn = tk.Button(frame, text="✅ Submit", command=self.submit_data, width=25, bg="#1e88e5", fg="white", font=("Arial", 12, "bold"), relief="raised", activebackground="#1565c0")
        submit_btn.grid(row=7, column=1, pady=20, padx=10)


    def open_feedback_window(self):
        feedback_window = tk.Toplevel(self.master)
        feedback_window.title("View Data & Feedback")
        feedback_window.geometry("900x700")
        feedback_window.configure(bg="#e3f2fd")  # Light Blue background

        frame = ttk.Frame(feedback_window, padding="20")
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(frame, text="View Your Data & Feedback", font=("Arial", 18, "bold"), fg="#d84315", bg="#e3f2fd")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Enter Your Name:", font=("Arial", 14, "bold"), fg="#4e342e", bg="#e3f2fd").grid(row=1, column=0, pady=10, sticky="w", padx=10)
        self.name_entry = tk.Entry(frame, width=40, font=("Arial", 12), bg="#fce4ec", fg="#880e4f", highlightbackground="#d81b60", highlightthickness=1)
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)

        submit_btn = tk.Button(frame, text="🔍 Submit", command=lambda: self.show_patient_data(feedback_window), width=25, bg="#43a047", fg="white", font=("Arial", 12, "bold"), relief="raised", activebackground="#2e7d32")
        submit_btn.grid(row=2, column=0, columnspan=2, pady=20)


    def show_data_submission_screen(self, frame):
        labels = ["Name", "Age", "Email", "Date", "Address", "Mobile No."]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label + ":", font=("Arial", 12)).grid(row=i, column=0, pady=5, sticky="w")
            entry = ttk.Entry(frame, width=40, font=("Arial", 12))
            entry.grid(row=i, column=1, pady=5)
            self.entries[label] = entry
        
        ttk.Button(frame, text="Upload Image", command=self.upload_image, width=30).grid(row=6, column=0, pady=20, padx=10)
        ttk.Button(frame, text="Submit", command=self.submit_data, width=30).grid(row=7, column=1, pady=20)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Upload", "Image uploaded successfully!")

    def submit_data(self):
        values = [self.entries[key].get() for key in self.entries]
        if "" in values or not self.image_path:
            messagebox.showerror("Error", "Please fill in all fields and upload an image.")
            return

        # Ensure upload directory exists
        upload_dir = os.path.join("assets", "images")
        os.makedirs(upload_dir, exist_ok=True)

        # Normalize path format before storing
        image_name = os.path.basename(self.image_path)
        destination_path = os.path.abspath(os.path.join(upload_dir, image_name)).replace("\\", "/")

        shutil.copy(self.image_path, destination_path)  # Copy image

        # Debugging: Check stored path format
        print(f"🔍 Debug: Stored Image Path - {destination_path}")

        # Insert into database
        conn = sqlite3.connect("data/users_data.db")
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO patients (name, age, email, date, address, mobile, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            values + [destination_path]
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Data Submitted Successfully!")


    def show_patient_name_entry(self, frame):
        ttk.Label(frame, text="Enter Your Name to View Data", font=("Arial", 18, 'bold')).grid(row=0, column=0, pady=20, columnspan=2)
        self.name_entry = ttk.Entry(frame, width=40, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, pady=10)
        ttk.Button(frame, text="Submit", command=lambda: self.show_patient_data(frame), width=30).grid(row=2, column=0, pady=20, columnspan=2)

    def show_patient_data(self, frame):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        conn = sqlite3.connect('data/users_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name = ?", (name,))
        data = cursor.fetchone()
        conn.close()

        if data:
            details_frame = ttk.Frame(frame, padding=20)
            details_frame.pack(pady=10, fill="both", expand=True)  # Use pack instead of grid

            ttk.Label(details_frame, text="Patient Details", font=("Arial", 16, 'bold')).pack(pady=10)

            # Correct column indices
            fields = ["Name", "Age", "Email", "Date", "Address", "Mobile", "Feedback"]
            data_indices = [1, 2, 3, 4, 5, 6, 8]  # Skip index 7 (image_path)

            for field, index in zip(fields, data_indices):
                row_frame = ttk.Frame(details_frame)
                row_frame.pack(fill="x", pady=2)  # Use pack instead of grid

                ttk.Label(row_frame, text=f"{field}:", font=("Arial", 12, 'bold')).pack(side="left", padx=10)
                ttk.Label(row_frame, text=data[index] if data[index] else "N/A", font=("Arial", 12)).pack(side="left", padx=10)
        else:
            messagebox.showerror("Error", "No data found for this patient.")