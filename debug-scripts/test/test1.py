# Write your code here :-)
import pyvisa

import serial.tools.list_ports

# Liste des ports série disponibles
ports = serial.tools.list_ports.comports()

if len(ports) > 0:
    print("Ports série disponibles :")
    for port, desc, hwid in sorted(ports):
        print(f"Port : {port}, Description : {desc}")
else:
    print("Aucun port série connecté.")