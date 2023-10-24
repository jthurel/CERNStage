import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

if len(ports) > 0:
    print("Ports série disponibles :")
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
else:
    print("Aucun port série disponible.")