import serial

# Configuration du port série
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)  # Assurez-vous que la vitesse en bauds est correcte

# Message à envoyer (ex. "AMPLIT 50\r\n")
message = "AMPLIT 50\r\n"

# Envoi du message sur le port série
ser.write(message.encode())

# Attendez une courte période (facultatif) pour permettre au périphérique de traiter la commande
# Peut être nécessaire en fonction de la réactivité du périphérique
import time
time.sleep(1)  # Attendre 1 seconde

# Fermez la connexion du port série
ser.close()