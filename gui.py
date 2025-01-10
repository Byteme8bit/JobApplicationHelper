import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from tkinter import ttk
from utils import generate_document, load_config #Import functions from utils


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

    labelCol = 0
    buttonA = 1
    textboxCol = 2
    scrollbarCol = 3
    buttonB = 4

    #Config file browse button
    config_browse_button = ttk.Button(root, text="Browse", command=browse_config_file)
    config_browse_button.grid(row=0, column=1, padx=5, pady=5)
    config_path_entry = ttk.Entry(root, textvariable=config_path)
    config_path_entry.grid(row=0, column=0, padx=5, pady=5)
    config_path_label = ttk.Label(root, text="Config File Path:")
    config_path_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    #Template file browse button
    template_browse_button = ttk.Button(root, text="Browse", command=browse_template_file)
    template_browse_button.grid(row=1, column=1, padx=5, pady=5)
    template_path_entry = ttk.Entry(root, textvariable=template_path)
    template_path_entry.grid(row=1, column=0, padx=5, pady=5)
    template_path_label = ttk.Label(root, text="Template File Path:")
    template_path_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

    #Output file name entry
    output_filename_entry = ttk.Entry(root, textvariable=output_filename)
    output_filename_entry.grid(row=2, column=0, padx=5, pady=5)
    output_filename_label = ttk.Label(root, text="Output File Name:")
    output_filename_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

    #Placeholders text area
    placeholders_text = tk.Text(root, height=10, width=30)
    placeholders_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    placeholders_label = ttk.Label(root, text="Placeholders (JSON):")
    placeholders_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

    #Add placeholder button
    placeholder_entry = ttk.Entry(root, textvariable=placeholder_var)
    placeholder_entry.grid(row=5, column=0, padx=5, pady=5)
    placeholder_label = ttk.Label(root, text="Placeholder:")
    placeholder_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

    replace_with_entry = ttk.Entry(root, textvariable=replace_with_var)
    replace_with_entry.grid(row=6, column=0, padx=5, pady=5)
    replace_with_label = ttk.Label(root, text="Replace With:")
    replace_with_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)

    add_placeholder_button = ttk.Button(root, text="Add Placeholder", command=add_placeholder)
    add_placeholder_button.grid(row=7, column=0, padx=5, pady=5)

    # Generate button
    generate_button = ttk.Button(root, text="Generate Document", command=generate_document_from_gui)
    generate_button.grid(row=8, column=0, columnspan=2, pady=10)

    root.mainloop()
