import serial

# Configuration du port série
port = '/dev/ttyUSB0'  # Remplacez par le nom de votre port série
baudrate = 9600  # Adapté à la vitesse en bauds de votre périphérique
timeout = 1

try:
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    # Commande à envoyer
    commande = "FREQUE,50\r\n"  # Remplacez par votre commande spécifique

    # Envoi de la commande sur le port série
    ser.write(commande.encode())

    # Attendez une courte période pour la réponse (facultatif)
    import time
    time.sleep(1)

    # Lecture de la réponse
    encodages_a_essayer = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252', 'cp850', 'utf-16']
    for encodage in encodages_a_essayer:
        try:
            reponse = ser.read(ser.in_waiting).decode(encodage)
            print(f"Réponse du périphérique (encodage {encodage}) : {reponse}")
            break  # Sortez de la boucle si vous avez réussi à décoder
        except UnicodeDecodeError:
            pass
except serial.serialutil.SerialException as e:
    print(f"Erreur lors de la communication avec le port série : {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()