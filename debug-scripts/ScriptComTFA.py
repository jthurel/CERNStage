import serial

# Port série à utiliser
port_name = '/dev/ttyUSB0'  # Remplacez par le nom de votre port série

# Configuration du port série
baudrate = 19200  # Adapté à la vitesse en bauds de votre périphérique
timeout = 2

ser = serial.Serial(port_name, baudrate=baudrate, timeout=timeout)

    # Commande à envoyer
commande = "AMPLIT,2.0\r\n"  # Commande "AMPLIT,50" suivie d'un retour chariot et d'un saut de ligne

    # Envoi de la commande sur le port série
#ser.write(commande.encode())
#ser.write(bytes("AMPLIT,2", 'UTF-8') + b'\r')
ser.write(bytes("*IDN?", 'utf-8') + b'\r')
response = ser.readline().decode('ascii')
print (response)

ser.write(bytes("AMPLIT, 1.5", 'utf-8') + b'\r')


if 'ser' in locals() and ser.is_open:
    ser.close()