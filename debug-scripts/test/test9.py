import serial.tools.list_ports

def find_serial_port(device_name):
    ports = list(serial.tools.list_ports.comports())
    for port, desc, hwid in ports:
        try:
            with serial.Serial(port, timeout=2) as ser:
                ser.write(b"*IDN?\n")
                response = ser.readline().decode('ascii')
                if device_name in response:
                    return port
        except serial.SerialException:
            pass
    return None

device_name = "GP102"  # Remplacez par le nom recherché dans la réponse
serial_port = find_serial_port(device_name)

if serial_port is not None:
    print(f"Port série trouvé : {serial_port}")
else:
    print(f"Aucun port série trouvé pour l'appareil contenant '{device_name}' dans la réponse.")