import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
#ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)


def search_port():
    #port.device=""
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                #search_result.set(port.device)
                return port.device # return the found port if existing
        except (OSError, serial.SerialException):
            continue

    #search_result.set("Aucun port trouvé")  # Met à jour le champ de texte en cas d'absence de port
    return "Aucun port trouvé"
port= search_port()
print (port)

# Mettez à jour le champ de texte lorsqu'un fichier est sélectionné
def update_search_result():
    port = search_port()
    search_result.set(port) #Effacez le champ de texte s'il n'y a pas de fichier sélectionné


root = tk.Tk()

# Create the "Search Port" button
search_result = tk.StringVar()
search_port_button = tk.Button(root, text="Search Port", command=update_search_result)
search_port_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Create the text field to display the found port
search_port_entry = tk.Entry(root, textvariable=search_result)
search_port_entry.grid(row=1, column=2, sticky="ew")

root.mainloop()

ser = serial.Serial(port, baudrate=19200, timeout=1)