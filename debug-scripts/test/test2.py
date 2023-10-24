import serial

# Spécifiez le port série (comporte) et la vitesse en bauds
port = serial.Serial('/dev/ttyUSB0', baudrate=9600)

# Données à envoyer
data_to_send = "AMPLIT 0.5\r\n"  # Exemple : envoie "AMPLIT 50" suivi d'un retour chariot et d'une nouvelle ligne

# Envoyez les données sur le port série
port.write(data_to_send.encode())

# Assurez-vous de fermer la connexion lorsque vous avez terminé
port.close()