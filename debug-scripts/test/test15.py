import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

def upload_config():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        #upload_result.set(file_name)
    return (file_name,file_path)