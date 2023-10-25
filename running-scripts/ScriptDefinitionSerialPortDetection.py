import serial
import serial.tools.list_ports

def port_detect():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                return port.device # return the found port if existing
        except (OSError, serial.SerialException):
            continue

    return None # return none if no port found

# Exemple d'utilisation
#port_trouve = port_detect()
#if port_trouve:
#    print(f"Port série correspondant trouvé : {port_trouve}")
#else:
#    print("Aucun port série correspondant trouvé.")

#port=port_detect()
#print(port)