import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

# Fonction pour gérer l'action du bouton "Upload Config"
def upload_config():
    selected_file = []  # Initialize selected_file as an empty list
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        selected_file.append(file_name)  # Append the file name to the list
        selected_file.append(file_path)  # Append the file path to the list
    return selected_file

fileofinterest = upload_config()
print(fileofinterest[0])
print(fileofinterest[1])