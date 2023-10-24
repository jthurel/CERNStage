import serial

# Port série à utiliser
port_name = '/dev/ttyUSB0'  # Remplacez par le nom de votre port série

# Configuration du port série
baudrate = 9600  # Adapté à la vitesse en bauds de votre périphérique
timeout = 1

try:
    ser = serial.Serial(port_name, baudrate=baudrate, timeout=timeout)

    # Commande à envoyer
    commande = "AMPLIT,50\r\n"  # Commande "AMPLIT,50" suivie d'un retour chariot et d'un saut de ligne

    # Envoi de la commande sur le port série
    ser.write(commande.encode())

    # Lecture de la réponse de l'appareil
    reponse = ser.read(ser.in_waiting)
    print("Réponse de l'appareil : " + reponse.ddecode('utf-8'))ecode('utf-8'))

except serial.SerialException as e:
    print(f"Erreur lors de la communication avec le port série : {e}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()