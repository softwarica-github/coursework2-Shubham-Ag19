import os
import tkinter as tk
from tkinter import filedialog

def is_file_corrupted(file_path, expected_signature):
    try:
        with open(file_path, 'rb') as file:
            actual_signature = file.read(len(expected_signature))
            return actual_signature == expected_signature

    except FileNotFoundError:
        return f"File not found: {file_path}"

    except Exception as e:
        return f"An error occurred while checking {file_path}: {e}"

def scan_files(directory, expected_signature):
    output_text.delete(1.0, tk.END)  # Clear previous output
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            output_text.insert(tk.END, file_path + "\n")
            if is_file_corrupted(file_path, expected_signature):
                output_text.insert(tk.END, "File is not corrupted.\n")
            else:
                output_text.insert(tk.END, "File may be corrupted.\n")

def browse_directory():
    global target_directory
    target_directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, target_directory)

def scan_button_clicked():
    global target_directory, expected_signature
    target_directory = directory_entry.get()
    expected_signature = signature_entry.get().encode()
    scan_files(target_directory, expected_signature)

root = tk.Tk()
root.title("Antivirus")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

directory_label = tk.Label(frame, text="Target Directory:")
directory_label.grid(row=0, column=0, padx=(0, 10))

directory_entry = tk.Entry(frame, width=50, textvariable=tk.StringVar())
directory_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2, padx=(10, 0))

signature_label = tk.Label(frame, text="Expected Signature (hex):")
signature_label.grid(row=1, column=0, padx=(0, 10))

signature_entry = tk.Entry(frame, width=50, textvariable=tk.StringVar())
signature_entry.grid(row=1, column=1)

scan_button = tk.Button(frame, text="Scan", command=scan_button_clicked)
scan_button.grid(row=2, column=1, pady=(10, 0))

output_text = tk.Text(root, height=20, width=60)
output_text.pack(pady=10)

root.mainloop()
