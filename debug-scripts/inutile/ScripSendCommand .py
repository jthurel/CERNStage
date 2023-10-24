import serial

# Configuration du port série (ajustez les paramètres en fonction de votre appareil)
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

# Lisez le fichier contenant les commandes et les valeurs ligne par ligne
with open('Data_files', 'r') as file:
    for line in file:
        # Divisez chaque ligne en deux parties (nom de commande et valeur)
        parts = line.strip().split(',')
        if len(parts) == 2:
            command, value = parts
            # Envoyez la commande et la valeur via le port série
            ser.write(f"{command},{value}\n".encode())

# Fermez la connexion série lorsque vous avez terminé
ser.close()