import tkinter as tk
from tkinter import messagebox, scrolledtext

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Stroke Detection - Chatbot")
        self.root.geometry("550x550")
        self.root.configure(bg="#E3F2FD")  # Light blue background

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_label = tk.Label(self.root, text="🧠 Brain Stroke Chatbot", font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#0D47A1")
        title_label.pack(pady=10)

        # Chat history box with scrolling
        chat_frame = tk.Frame(self.root, bg="white", bd=2, relief="sunken")
        chat_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=15, width=50, state=tk.DISABLED, font=("Arial", 12))
        self.chat_history.pack(padx=5, pady=5, fill="both", expand=True)

        # Input field
        entry_frame = tk.Frame(self.root, bg="#E3F2FD")
        entry_frame.pack(pady=5)

        self.entry_field = tk.Entry(entry_frame, width=40, font=("Arial", 12))
        self.entry_field.pack(side="left", padx=5, pady=5, ipady=4)

        send_button = tk.Button(entry_frame, text="Send 📨", font=("Arial", 12, "bold"), bg="#0D47A1", fg="white",
                                relief="raised", padx=10, command=self.get_response)
        send_button.pack(side="right", padx=5)

        # Predefined questions label
        question_label = tk.Label(self.root, text="💡 Common Questions:", font=("Arial", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        question_label.pack(pady=5)

        # Listbox for predefined questions
        self.questions_listbox = tk.Listbox(self.root, height=5, width=55, font=("Arial", 12), bg="white", fg="black", bd=2, relief="groove")
        self.questions_listbox.pack(pady=5)

        # Add questions
        self.questions = [
            "What is a brain stroke?",
            "What are the symptoms of a brain stroke?",
            "How can I prevent a brain stroke?",
            "What should I do if I suspect a brain stroke?",
            "What care should I take after a stroke?"
        ]
        for question in self.questions:
            self.questions_listbox.insert(tk.END, question)

        # Bind click event on questions to provide answers
        self.questions_listbox.bind("<ButtonRelease-1>", self.on_question_click)

    def get_response(self):
        user_input = self.entry_field.get().strip()
        if not user_input:
            return
        
        # Display user input in the chat history
        self.display_message(f"👤 You: {user_input}")
        
        # Get chatbot's response
        response = self.generate_response(user_input)
        
        # Display chatbot response in the chat history
        self.display_message(f"🤖 Chatbot: {response}")
        
        # Clear the input field
        self.entry_field.delete(0, tk.END)

    def on_question_click(self, event):
        selected_question = self.questions_listbox.get(self.questions_listbox.curselection())
        self.display_message(f"👤 You: {selected_question}")
        response = self.generate_response(selected_question)
        self.display_message(f"🤖 Chatbot: {response}")

    def display_message(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview(tk.END)

    def generate_response(self, user_input):
        responses = {
            "What is a brain stroke?": "🧠 A brain stroke happens when blood flow to the brain is disrupted, causing brain cells to die.",
            "What are the symptoms of a brain stroke?": "⚠️ Symptoms include sudden numbness, confusion, trouble speaking, vision loss, and severe headache.",
            "How can I prevent a brain stroke?": "💪 Eat healthy, exercise regularly, control blood pressure, avoid smoking, and manage stress.",
            "What should I do if I suspect a brain stroke?": "🚑 Call emergency services immediately. Time is crucial for stroke treatment.",
            "What care should I take after a stroke?": "🏥 Recovery includes physical therapy, medication, a healthy diet, and regular check-ups."
        }
        return responses.get(user_input, "🤷 Sorry, I don't understand. Please ask something else.")
