import serial

def upload_config_file(port, baudrate, filename):
    try:
        with serial.Serial(port, baudrate=baudrate, timeout=2) as ser:
            # Ouvrir le fichier de configuration en mode lecture
            with open(filename, 'r') as config_file:
                # Lire le contenu du fichier ligne par ligne
                for line in config_file:
                    # Envoyer chaque ligne au port série
                    ser.write(line.encode('utf-8'))
                    # Attendre une réponse (si nécessaire)
                    response = ser.readline().decode('utf-8')
                    print(f"Envoyé : {line.strip()}, Réponse : {response.strip()}")

        print("Téléchargement du fichier de configuration terminé.")
    except Exception as e:
        print(f"Erreur lors de la communication série : {e}")

# Exemple d'utilisation
port = '/dev/ttyUSB0'  # Remplacez par le bon port série
baudrate = 19200  # Ajustez la vitesse de baud en fonction de votre appareil
filename = 'config.txt'  # Remplacez par le nom du fichier de configuration

upload_config_file(port, baudrate, filename)