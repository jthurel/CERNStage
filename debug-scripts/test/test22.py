import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

def search_port():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                return port.device  # return the found port if existing
        except (OSError, serial.SerialException):
            continue

    return None  # Return None if no port is found

def update_search_result():
    port = search_port()
    if port is not None:
        search_result.set(port)
    else:
        search_result.set("Aucun port trouvé")

ser = serial.Serial(port.device, baudrate=19200, timeout=2)


root = tk.Tk()

# Create the "Search Port" button
search_result = tk.StringVar()
search_port_button = tk.Button(root, text="Search Port", command=update_search_result)
search_port_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Create the text field to display the found port
search_port_entry = tk.Entry(root, textvariable=search_result)
search_port_entry.grid(row=1, column=2, sticky="ew")

root.mainloop()