import serial
import time

# Créer une connexion série avec le bon port et le bon débit
ser = serial.Serial("/dev/ttyUSB0", baudrate=19200, timeout=1)

def check_operation_status():
    ser.write(bytes("START", 'utf-8') + b'\r')
    ser.reset_input_buffer()  # Efface le tampon d'entrée
    ser.write(bytes("*OPC?", 'utf-8') + b'\r')  # Envoie la commande "*OPC?"

    time.sleep(0.5)  # Attendez un peu pour la réponse

    response = ser.read(1).decode('ascii')  # Lit la réponse (1 caractère)

    # La réponse devrait être "1" si l'opération précédente est terminée, sinon c'est "0"
    if response == '1':
        return True  # Opération terminée
    else:
        return False  # Opération en cours

# Exemple d'utilisation de la fonction
if check_operation_status():
    print("L'opération précédente est terminée (1).")
else:
    print("L'opération précédente est en cours (0).")