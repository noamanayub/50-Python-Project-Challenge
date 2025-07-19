import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog
from tkinter import font as tkFont
from fuzzywuzzy import process
import os
import csv
import pdfplumber

def load_data(filepath):
    data = {}
    with open(filepath, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                question, answer = line.strip().split("|")
                data[question.lower()] = answer  # Convert question to lowercase
            except ValueError as e:
                print(f"Error parsing line {line_number}: {line.strip()}")
                print(f"Error message: {e}")
    return data

def save_data(filepath, data):
    with open(filepath, 'w') as file:
        for question, answer in data.items():
            file.write(f"{question}|{answer}\n")

def get_response(user_input, data):
    user_input = user_input.lower()  # Convert user input to lowercase
    for question in data:
        if question in user_input:
            return data[question]
    return None

def fuzzy_match(user_input, data):
    questions = list(data.keys())
    match, score = process.extractOne(user_input, questions)
    if score > 80:  # Adjust the threshold as needed
        return data[match]
    return None

def load_bad_words(filepath):
    bad_words = set()
    with open(filepath, 'r') as file:
        for line in file:
            bad_words.add(line.strip().lower())
    return bad_words

def contains_bad_words(text, bad_words):
    return any(word in text.lower() for word in bad_words)

def read_csv(filepath):
    data = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                question, answer = row
                data[question.lower()] = answer
    return data

def read_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadow AI")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        self.data = load_data("chatbot_data.txt")
        self.bad_words = load_bad_words("bad_words.txt")
        self.feedback_data = {}

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#ffffff", fg="#333333", font=("Helvetica", 12))
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.user_input = tk.Entry(self.input_frame, font=("Helvetica", 12), bg="#ffffff", fg="#333333", insertbackground="#333333")
        self.user_input.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key to send message

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff")
        self.send_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg="#45a049"))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg="#4CAF50"))

        self.feedback_button = tk.Button(self.input_frame, text="Feedback", command=self.show_feedback, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff")
        self.feedback_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.feedback_button.bind("<Enter>", lambda e: self.feedback_button.config(bg="#45a049"))
        self.feedback_button.bind("<Leave>", lambda e: self.feedback_button.config(bg="#4CAF50"))

        self.upload_button = tk.Button(self.input_frame, text="Upload File", command=self.upload_file, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff")
        self.upload_button.grid(row=0, column=3, sticky="e", padx=5, pady=5)
        self.upload_button.bind("<Enter>", lambda e: self.upload_button.config(bg="#45a049"))
        self.upload_button.bind("<Leave>", lambda e: self.upload_button.config(bg="#4CAF50"))

        self.clear_button = tk.Button(self.input_frame, text="Clear", command=self.clear_chat, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff")
        self.clear_button.grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#45a049"))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#4CAF50"))

        self.input_frame.columnconfigure(0, weight=1)

        self.last_user_input = ""
        self.last_response = ""

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()  # Remove extra spaces
        if contains_bad_words(user_text, self.bad_words):
            self.display_message("Shadow AI: I am not allowed to answer bad questions. To maintain a professional and respectful environment, it's important to avoid using inappropriate or offensive language.", logo="ai", color='blue')
        elif user_text:
            self.display_message("User: " + user_text, logo="user")
            response = get_response(user_text, self.data)
            if not response:
                response = fuzzy_match(user_text, self.data)
            if not response:
                response = "I'm sorry, I don't understand that."
            self.display_message("Shadow AI: " + response, logo="ai", color='blue')
            self.user_input.delete(0, tk.END)
            self.last_user_input = user_text
            self.last_response = response
            self.ask_for_details(user_text, response)

    def display_message(self, message, logo=None, color='black'):
        self.chat_window.config(state='normal')
        if logo == "ai":
            self.chat_window.insert(tk.END, "🤖 ", "logo")
        elif logo == "user":
            self.chat_window.insert(tk.END, "👤 ", "logo")
        self.chat_window.insert(tk.END, message + "\n", color)
        self.chat_window.tag_config("logo", foreground="grey")
        self.chat_window.tag_config(color, foreground=color)
        self.chat_window.config(state='disabled')
        self.chat_window.yview(tk.END)

    def show_feedback(self):
        if self.last_user_input and self.last_response:
            self.get_feedback(self.last_user_input, self.last_response)
        else:
            messagebox.showinfo("Feedback", "No recent message to provide feedback on.")

    def get_feedback(self, user_input, response):
        feedback = messagebox.askquestion("Feedback", f"Was this response helpful?\n\nUser Input: {user_input}\nResponse: {response}")
        if feedback == 'no':
            new_response = simpledialog.askstring("Feedback", "Please provide a better response:")
            if new_response:
                self.data[user_input.lower()] = new_response
                save_data("chatbot_data.txt", self.data)
                messagebox.showinfo("Feedback", "Thank you for your feedback! The new response has been added to my data.")

    def ask_for_details(self, user_input, response):
        if response == "I'm sorry, I don't understand that.":
            similar_questions = [q for q in self.data.keys() if user_input in q]
            if similar_questions:
                similar_question = similar_questions[0]
                confirm = messagebox.askquestion("Confirm", f"Did you mean: {similar_question}?")
                if confirm == 'yes':
                    self.display_message("Shadow AI: " + self.data[similar_question], logo="ai", color='blue')
                else:
                    messagebox.showinfo("Details", "Please provide more details so I can better assist you.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("PDF files", "*.pdf")])
        if file_path:
            if file_path.endswith(('.txt', '.csv')):
                if file_path.endswith('.txt'):
                    new_data = load_data(file_path)
                elif file_path.endswith('.csv'):
                    new_data = read_csv(file_path)
                self.data.update(new_data)
                save_data("chatbot_data.txt", self.data)
                messagebox.showinfo("Upload", "File uploaded and data updated successfully.")
            elif file_path.endswith('.pdf'):
                pdf_text = read_pdf(file_path)
                self.display_message("Shadow AI: PDF content extracted. You can now ask questions related to the content.", logo="ai", color='blue')
                self.data.update({"pdf_content": pdf_text})
            else:
                messagebox.showinfo("Upload", "File format not supported for updating data.")

    def clear_chat(self):
        self.chat_window.config(state='normal')
        self.chat_window.delete(1.0, tk.END)
        self.chat_window.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()