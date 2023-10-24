import serial.tools.list_ports

def port_detect():
    # Recherche de tous les ports série disponibles
    available_ports = list(serial.tools.list_ports.comports())

    # Parcourir la liste des ports pour trouver le bon
    for port in available_ports:
        try:
            # Ouvrir le port série
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)

            # Envoyer la commande "*IDN?" et lire la réponse
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            print (response)

            # Fermer le port série
            ser.close()

            # Si la réponse contient "GP102", retourner le port
            if "GP102" in response:
                return port.device
        except (OSError, serial.SerialException):
            pass

    # Si aucun port correspondant n'est trouvé, retourner None
    return None

# Exemple d'utilisation
detected_port = port_detect()
if detected_port:
    print(f"Le port série correspondant est : {detected_port}")
else:
    print("Aucun port série correspondant trouvé.")


