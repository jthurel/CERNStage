import serial

with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
    ser.rts = True
    ser.write(bytes("AMPLIT, 1000000", 'utf-8') + b'\r')
# Configuration du port série (ajustez les paramètres en fonction de votre appareil)
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

# Envoyez la commande *OPC?
ser.write(b"*OPC?\n")

# Attendez la réponse (ajustez le nombre d'octets en fonction de votre réponse attendue)
response = ser.read(10)  # Ici, nous attendons 10 octets

# Affichez la réponse reçue
print(f"Réponse : {response.decode('utf-8')}")

# Fermez la connexion série lorsque vous avez terminé
ser.close()