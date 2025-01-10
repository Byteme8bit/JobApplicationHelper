import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from tkinter import ttk
from mainDev import generate_document, load_config # Import necessary functions


def browse_config_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        config_path.set(file_path)
        load_config_file()


def browse_template_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx"), ("Text files", "*.txt")])
    if file_path:
        template_path.set(file_path)


def load_config_file():
    config_path_val = config_path.get()
    if not os.path.exists(config_path_val):
        messagebox.showerror("Error", "Config file not found.")
        return
    config = load_config(config_path_val)
    template_path.set(config.get("templateFilePath", ""))
    output_filename.set(config.get("outputFilePath", ""))
    placeholders_text.delete("1.0", tk.END)
    placeholders_text.insert(tk.END, json.dumps(config.get("placeholders", {}), indent=4))


def add_placeholder():
    placeholder = placeholder_var.get()
    replace_with = replace_with_var.get()
    if placeholder and replace_with:
        placeholders_text.insert(tk.END, f"{placeholder}: {replace_with}\n")
        placeholder_var.set("")
        replace_with_var.set("")
    else:
        messagebox.showerror("Error", "Both fields must be filled out.")


def generate_document_from_gui():
    template_path_val = template_path.get()
    output_filename_val = output_filename.get()
    placeholders_text_val = placeholders_text.get("1.0", tk.END).strip()

    if not template_path_val or not output_filename_val or not placeholders_text_val:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        placeholders = json.loads(placeholders_text_val)
        generate_document(template_path_val, output_filename_val, placeholders)
        messagebox.showinfo("Success", "Document generated successfully!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format in placeholders.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def run_gui():
    global config_path, template_path, output_filename, placeholder_var, replace_with_var, placeholders_text

    root = tk.Tk()
    root.title("Job Application Helper")

    config_path = tk.StringVar()
    template_path = tk.StringVar()
    output_filename = tk.StringVar()
    placeholder_var = tk.StringVar()
    replace_with_var = tk.StringVar()

    # ... (rest of your GUI code remains the same) ...

    # Generate button
    generate_button = ttk.Button(root, text="Generate Document", command=generate_document_from_gui)
    generate_button.grid(row=8, column=2, columnspan=2, pady=10)

    root.mainloop()

