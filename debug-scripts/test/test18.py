import tkinter as tk
from tkinter import filedialog
import os

def upload_config():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        fileofinterest.clear()  # Clear the list
        fileofinterest.append(file_name)  # Append the file name to the list
        fileofinterest.append(file_path)  # Append the file path to the list
        upload_entry.delete(0, tk.END)  # Clear the current text in the entry
        upload_entry.insert(0, file_name)  # Display the file name in the entry field

# Create the main tkinter window
root = tk.Tk()

# Global variable to store the selected file information
fileofinterest = []

# Create the "Upload Config" button
upload_button = tk.Button(root, text="Upload Config", command=upload_config)
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Create the text entry field to display the selected file
upload_entry = tk.Entry(root)
upload_entry.grid(row=1, column=2, sticky="ew")


# Start the tkinter main loop
root.mainloop()