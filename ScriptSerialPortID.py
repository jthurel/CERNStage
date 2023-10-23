import serial

# Liste des noms de ports série que vous souhaitez vérifier
port_names = ['COM1', 'COM2', 'COM3', '/dev/ttyUSB0']  # Remplacez par les noms des ports que vous voulez vérifier

# Fonction pour envoyer la requête "*IDN?" et vérifier la réponse
def check_port(port_name):
    try:
        with serial.Serial(port_name, baudrate=9600, timeout=2) as ser:
            ser.reset_input_buffer()
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            #ser.write(b'*IDN?\n')
            response = ser.readline().decode('utf-8').strip()
            if response:
                return f"Port {port_name}: {response}"
    except serial.SerialException:
        pass
    return f"Port {port_name}: Aucun appareil trouvé"

# Parcourir la liste des ports et afficher les résultats
for port_name in port_names:
    result = check_port(port_name)
    print(result)