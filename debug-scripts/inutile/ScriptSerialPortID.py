import serial

# Liste des noms de ports série que vous souhaitez vérifier
port_names = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyS0']  # Remplacez par les noms des ports que vous voulez vérifier

# Fonction pour envoyer la requête "*IDN?" et vérifier la réponse
def check_port(port_name):
    try:
        with serial.Serial(port_name, baudrate=19200, timeout=2) as ser:
            ser.rts = True
            ser.reset_input_buffer()
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            print (response)
    except serial.SerialException:
        pass
    return f"Port {port_name}: Aucun appareil trouvé"

# Parcourir la liste des ports et afficher les résultats
for port_name in port_names:
    result = check_port(port_name)
    print(result)