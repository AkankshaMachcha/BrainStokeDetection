import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from image_analysis import analyze_image  # Import the function that returns result & summary
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AdminPanel:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Panel")
        self.master.geometry("800x500")
        self.master.configure(bg="#f0f8ff")
        
        ttk.Label(self.master, text="Admin Panel - Patient Data", font=("Arial", 16, "bold"), background="#f0f8ff", foreground="#333").pack(pady=10)

        self.treeview_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.treeview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("ID", "Name", "Age", "Email", "Date", "Address", "Mobile", "Image Path", "Feedback"), show='headings')
        self.treeview.pack(fill="both", expand=True)
        
        for col in ("ID", "Name", "Age", "Email", "Date", "Address", "Mobile", "Image Path", "Feedback"):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)
        
        self.show_patient_data()
        
        analyze_button = ttk.Button(self.master, text="Analyze Selected Patient", command=self.analyze_selected_patient, style="TButton")
        analyze_button.pack(pady=10)
        
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        
    def show_patient_data(self):
        """Display all patients' data with increased font size."""
        if self.treeview is not None:
            self.treeview.destroy()

        # Configure style for larger text
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))  # Increase row text size
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))  # Increase header text size

        self.treeview = ttk.Treeview(self.master, columns=("ID", "Name", "Age", "Email", "Date", "Address", "Mobile", "Image Path", "Feedback", "Action"), style="Treeview")
        
        self.treeview.heading("#1", text="ID")
        self.treeview.heading("#2", text="Name")
        self.treeview.heading("#3", text="Age")
        self.treeview.heading("#4", text="Email")
        self.treeview.heading("#5", text="Date")
        self.treeview.heading("#6", text="Address")
        self.treeview.heading("#7", text="Mobile")
        self.treeview.heading("#8", text="Image Path")
        self.treeview.heading("#9", text="Feedback")
        self.treeview.heading("#10", text="Action")

        self.treeview.pack(fill="both", expand=True)
        self.treeview.column("#7", width=100)

        conn = sqlite3.connect('data/users_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        
        for patient in patients:
            self.treeview.insert("", "end", values=(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7], patient[8], "Analyze"))

        conn.close()

    
    def analyze_selected_patient(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to analyze.")
            return

        selected_patient = self.treeview.item(selected_item)["values"]
        patient_id = selected_patient[0]
        image_path = selected_patient[7]
        
        output = analyze_image(image_path)
        if not isinstance(output, tuple) or len(output) != 2:
            messagebox.showerror("Error", f"Unexpected return from analyze_image: {output}")
            return

        result, summary = output
        self.show_feedback_entry(patient_id, result, summary)
    
    def show_feedback_entry(self, patient_id, result, summary):
        feedback_window = tk.Toplevel(self.master)
        feedback_window.title(f"Feedback for Patient {patient_id}")
        feedback_window.geometry("500x400")
        feedback_window.configure(bg="#f5f5dc")
        
        ttk.Label(feedback_window, text="Feedback on Image Analysis:", font=("Arial", 12, "bold"), background="#f5f5dc").pack(pady=10)
        self.feedback_entry = tk.Text(feedback_window, height=4, width=50)
        self.feedback_entry.pack(pady=10)
        
        ttk.Label(feedback_window, text=f"Analysis Result: {result}", font=("Arial", 11, "bold"), background="#f5f5dc").pack(pady=10)
        
        summary_frame = ttk.Frame(feedback_window)
        summary_frame.pack(fill="both", expand=True, padx=10, pady=5)

        summary_text = tk.Text(summary_frame, wrap="word", height=5, width=50)
        summary_text.insert("1.0", summary)
        summary_text.config(state="disabled")
        summary_text.pack()

        submit_button = ttk.Button(feedback_window, text="Submit Feedback", command=lambda: self.submit_feedback(patient_id))
        submit_button.pack(pady=10)
    
    def submit_feedback(self, patient_id):
        feedback = self.feedback_entry.get("1.0", "end-1c")
        if not feedback.strip():
            messagebox.showerror("Error", "Please provide feedback.")
            return
        
        conn = sqlite3.connect('data/users_data.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET feedback = ? WHERE id = ?", (feedback, patient_id))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Feedback Submitted", "Your feedback has been successfully submitted!")
        self.send_email(patient_id)
        self.show_patient_data()
    
    def send_email(self, patient_id):
        conn = sqlite3.connect('data/users_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, email, date, address, mobile, feedback FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()

        if not patient:
            print("No patient found with the given ID.")
            return

        name, age, email, date, address, mobile, feedback = patient
        
        sender_email = "machchaakanksha30@gmail.com"  # Change to your email
        sender_password = "lecu kkig ibpf oggb"  # Use Gmail App Password
        receiver_email = email  # Patient's email

        subject = f"Brain Stroke Analysis Report for {name}"
        body = f"""
        Hello {name},

        Here is your Brain Stroke Analysis Report:

        Patient Details:
        - Name: {name}
        - Age: {age}
        - Email: {email}
        - Date: {date}
        - Address: {address}
        - Mobile: {mobile}

        Doctor's Feedback:
        {feedback}

        If you have any concerns, please reach out to our medical team.

        Regards,  
        Brain Stroke Detection Team
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            
            print(f"Email sent successfully to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

