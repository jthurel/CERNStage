import tkinter as tk
from tkinter import filedialog
import os
import time
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox



ports = list(serial.tools.list_ports.comports())
print( ports)