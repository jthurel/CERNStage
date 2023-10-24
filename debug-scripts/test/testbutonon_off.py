import tkinter as tk
import serial

# Configuration du port série (ajustez les paramètres en fonction de votre appareil)
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

# Fonction pour envoyer la commande en fonction du choix de l'utilisateur
def send_command(command):
    if command == "ON":
        ser.write(bytes("OUTPUT,ON", 'utf-8') + b'\r')
    elif command == "OFF":
        ser.write(bytes("OUTPUT,OFF", 'utf-8') + b'\r')

# Fonction appelée lorsque le bouton "ON" est cliqué
def turn_on():
    send_command("ON")

# Fonction appelée lorsque le bouton "OFF" est cliqué
def turn_off():
    send_command("OFF")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Contrôle de la sortie")

# Création de boutons pour activer/désactiver la sortie
on_button = tk.Button(root, text="ON", command=turn_on)
on_button.pack()

off_button = tk.Button(root, text="OFF", command=turn_off)
off_button.pack()

# Lancer la boucle principale de tkinter
root.mainloop()

# Fermez la connexion série lorsque vous avez terminé
ser.close()