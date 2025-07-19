import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

def translate_text():
    text_to_translate = entry_text.get("1.0", "end-1c")
    target_language = target_language_combobox.get()
    detected_language = detect_language(text_to_translate)
    source_language_combobox.set(LANGUAGES[detected_language])
    translated_text = translator.translate(text_to_translate, src=detected_language, dest=target_language).text
    english_version = translator.translate(translated_text, src=target_language, dest='en').text
    output_text.delete("1.0", "end")
    output_text.insert("1.0", f"{translated_text} (English version: {english_version})")

def save_translation():
    text_to_save = output_text.get("1.0", "end-1c")
    target_language = target_language_combobox.get()
    save_text.insert("end", f"Translated to {target_language}: {text_to_save}\n")

def clear_saved_text():
    save_text.delete("1.0", "end")

def detect_language(text):
    detected = translator.detect(text)
    return detected.lang

def filter_languages(event):
    search_query = search_bar.get().lower()
    filtered_languages = [lang for code, lang in LANGUAGES.items() if search_query in lang.lower()]
    target_language_combobox['values'] = filtered_languages

# Initialize the translator
translator = Translator()

# Create the main window
root = tk.Tk()
root.title("Language Translator")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Style settings
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="#000")
style.map("TButton", background=[("active", "#bbb")])

# Frame for input and output boxes
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Input text area and language selection
input_frame = tk.Frame(frame, bg="#f0f0f0")
input_frame.pack(side="left", fill="both", expand=True)

tk.Label(input_frame, text="Input Text", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
entry_text = tk.Text(input_frame, height=10, width=50, bg="#fff", relief="flat", borderwidth=0)
entry_text.pack(pady=10, padx=10, fill="both", expand=True)

source_language_combobox = ttk.Combobox(input_frame, values=list(LANGUAGES.values()), state="readonly")
source_language_combobox.set("Auto Detect")
source_language_combobox.pack(pady=10)

# Output text area and language selection
output_frame = tk.Frame(frame, bg="#f0f0f0")
output_frame.pack(side="right", fill="both", expand=True)

tk.Label(output_frame, text="Output Text", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
output_text = tk.Text(output_frame, height=10, width=50, bg="#fff", fg="black", relief="flat", borderwidth=0)
output_text.pack(pady=10, padx=10, fill="both", expand=True)

# Search bar for language selection
search_frame = tk.Frame(output_frame, bg="#f0f0f0")
search_frame.pack(pady=10)

search_bar = tk.Entry(search_frame, font=("Helvetica", 12))
search_bar.pack(side="left", fill="x", expand=True, padx=10)
search_bar.bind("<KeyRelease>", filter_languages)

target_language_combobox = ttk.Combobox(search_frame, values=list(LANGUAGES.values()), state="readonly")
target_language_combobox.set("Urdu")  # Default language Urdu
target_language_combobox.pack(side="left", fill="x", expand=True)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

# Translate button
translate_button = ttk.Button(button_frame, text="Translate", command=translate_text)
translate_button.pack(side="left", padx=10)

# Save button
save_button = ttk.Button(button_frame, text="Save", command=save_translation)
save_button.pack(side="left", padx=10)

# Clear button
clear_button = ttk.Button(button_frame, text="Clear", command=clear_saved_text)
clear_button.pack(side="left", padx=10)

# Save text area
tk.Label(root, text="Saved Translations", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
save_text = tk.Text(root, height=10, width=50, bg="#fff", relief="flat", borderwidth=0)
save_text.pack(pady=20, padx=20, fill="both", expand=True)

# Center alignment
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()