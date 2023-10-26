import tkinter as tk
from tkinter import filedialog
import os
import serial
import time
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)
#l'ordre compte
ser.write(bytes("OUTPUT,ON", 'utf-8') + b'\r')
ser.write(bytes("MODE,GAINPH", 'utf-8') + b'\r')
ser.write(bytes("FSWEEP,10,10,1000", 'utf-8') + b'\r')

ser.write(bytes("START", 'utf-8') + b'\r')
ser.write(bytes("*WAI", 'utf-8') + b'\r')

def upload_config():
    #global state
    results = ""
    ser.reset_input_buffer()
    ser.write(bytes("DAV?", 'UTF-8') + b'\r')
    time.sleep(0.5)
    while ser.in_waiting < 0:
        pass
    while ser.in_waiting > 0:
        data_ready = ser.read(ser.in_waiting).decode('ascii')
    if "15" in data_ready:
        ser.reset_input_buffer()
        ser.write(bytes("GAINPH?SWEEP", 'UTF-8') + b'\r')
        while ser.in_waiting <= 0:
            pass
        while ser.in_waiting > 0:
            results += ser.read(ser.in_waiting).decode('ascii')
            time.sleep(0.05)
        results = "Frequency,Magnitude_1,Magnitude_2,dB,Phase\n" + results
        print(results)
        with open('test.csv', "w", encoding="utf-8") as f:
            f.write(results.replace("\r", ""))