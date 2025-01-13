import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from tkinter import ttk
from utils import generate_document, load_config


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

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Populate the listbox with placeholders
    placeholders = config.get("placeholders", {})
    for key, value in placeholders.items():
        listbox.insert(tk.END, f"{key}: {value}")

def generate_document_from_gui():
    template_path_val = template_path.get()
    output_filename_val = output_filename.get()
    placeholders_text_val = placeholder_var.get()

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

def add_placeholder():
    placeholder = placeholder_var.get()
    replace_with = replace_with_var.get()
    if placeholder and replace_with:
        existing_items = listbox.get(0, tk.END)
        updated = False
        for i, item in enumerate(existing_items):
            key, value = item.split(":", 1)
            if key.strip() == placeholder:
                listbox.delete(i)
                listbox.insert(i, f"{placeholder}: {replace_with}")
                updated = True
                break
        if not updated:
            listbox.insert(tk.END, f"{placeholder}: {replace_with}")
        placeholder_var.set("")
        replace_with_var.set("")
    else:
        messagebox.showerror("Error", "Both fields must be filled out.")

def edit_placeholder(event):
    try:
        selected_index = listbox.curselection()[0]
        item = listbox.get(selected_index)
        key, value = item.split(":", 1)
        placeholder_var.set(key.strip())
        replace_with_var.set(value.strip())
        listbox.delete(selected_index)
    except (IndexError, ValueError):
        messagebox.showerror("Error", "Invalid item selected.")

def remove_placeholder():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        placeholder_var.set("")
        replace_with_var.set("")
    except IndexError:
        messagebox.showerror("Error", "No item selected.")

def insert_placeholder():
    placeholder = placeholder_var.get()
    replace_with = replace_with_var.get()
    if placeholder and replace_with:
        try:
            selected_index = listbox.curselection()[0] + 1
            listbox.insert(selected_index, f"{placeholder}: {replace_with}")
            placeholder_var.set("")
            replace_with_var.set("")
        except IndexError:
            messagebox.showerror("Error", "No item selected.")
    else:
        messagebox.showerror("Error", "Both fields must be filled out.")

def run_gui():
    global config_path, template_path, output_filename, placeholder_var, replace_with_var, listbox

    root = tk.Tk()
    root.title("Job Application Helper")

    config_path = tk.StringVar()
    template_path = tk.StringVar()
    output_filename = tk.StringVar()
    placeholder_var = tk.StringVar()
    replace_with_var = tk.StringVar()

    labelCol = 0
    textboxCol = 1
    textboxColumnspan = 2
    buttonA = textboxCol + 5
    buttonB = textboxCol + 7
    buttonColumnspan = 2

    # Config file browse button
    config_path_label = ttk.Label(root, text="Config File Path:")
    config_path_label.grid(row=0, column=labelCol, sticky=tk.W, padx=5, pady=2)
    config_path_entry = ttk.Entry(root, textvariable=config_path, width=50)
    config_path_entry.grid(row=0, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="ew")
    config_browse_button = ttk.Button(root, text="Browse", command=browse_config_file)
    config_browse_button.grid(row=0, column=buttonA, columnspan=buttonColumnspan, padx=5, pady=2)
    load_config_button = ttk.Button(root, text="Load Config", command=load_config_file)
    load_config_button.grid(row=0, column=buttonB, columnspan=buttonColumnspan, padx=5, pady=2)

    # Template file browse button
    template_path_label = ttk.Label(root, text="Template File Path:")
    template_path_label.grid(row=1, column=labelCol, sticky=tk.W, padx=5, pady=2)
    template_path_entry = ttk.Entry(root, textvariable=template_path, width=50)
    template_path_entry.grid(row=1, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="ew")
    template_browse_button = ttk.Button(root, text="Browse", command=browse_template_file)
    template_browse_button.grid(row=1, column=buttonA, columnspan=buttonColumnspan, padx=5, pady=2)

    # Output file name entry
    output_filename_label = ttk.Label(root, text="Output File Name:")
    output_filename_label.grid(row=2, column=labelCol, sticky=tk.W, padx=5, pady=2)
    output_filename_entry = ttk.Entry(root, textvariable=output_filename, width=50)
    output_filename_entry.grid(row=2, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="ew")

    # Placeholders listbox
    placeholders_label = ttk.Label(root, text="Placeholders:")
    placeholders_label.grid(row=3, column=labelCol, sticky=tk.W, padx=5, pady=2)
    listbox = tk.Listbox(root, height=10, width=50)
    listbox.grid(row=3, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="nsew")
    listbox.bind("<ButtonRelease-1>", edit_placeholder)

    # Add placeholder button and entries
    placeholder_label = ttk.Label(root, text="Placeholder:")
    placeholder_label.grid(row=4, column=labelCol, sticky=tk.W, padx=5, pady=2)
    placeholder_entry = ttk.Entry(root, textvariable=placeholder_var, width=50)
    placeholder_entry.grid(row=4, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="ew")

    replace_with_label = ttk.Label(root, text="Replace With:")
    replace_with_label.grid(row=5, column=labelCol, sticky=tk.W, padx=5, pady=2)
    replace_with_entry = ttk.Entry(root, textvariable=replace_with_var, width=50)
    replace_with_entry.grid(row=5, column=textboxCol, columnspan=textboxColumnspan, padx=5, pady=2, sticky="ew")

    add_placeholder_button = ttk.Button(root, text="Add", command=add_placeholder)
    add_placeholder_button.grid(row=4, column=buttonA, columnspan=buttonColumnspan, padx=5, pady=2)

    clear_placeholder_button = ttk.Button(root, text="Clear", command=remove_placeholder)
    clear_placeholder_button.grid(row=4, column=buttonA + 2, columnspan=buttonColumnspan, padx=5, pady=2)

    insert_placeholder_button = ttk.Button(root, text="Insert", command=insert_placeholder)
    insert_placeholder_button.grid(row=5, column=buttonA, columnspan=buttonColumnspan, padx=5, pady=2)

    remove_placeholder_button = ttk.Button(root, text="Remove", command=remove_placeholder)
    remove_placeholder_button.grid(row=5, column=buttonA + 2, columnspan=buttonColumnspan, padx=5, pady=2)

    # Generate button
    generate_button = ttk.Button(root, text="Generate Document", command=generate_document_from_gui)
    generate_button.grid(row=6, column=labelCol, columnspan=10, pady=10, sticky="ew")

    root.columnconfigure(textboxCol, weight=1)
    root.mainloop()
