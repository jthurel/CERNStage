import tkinter as tk
import serial

# Définition de la fonction Start_Sweep
def Start_Sweep():
    with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
        ser.write(bytes("START", 'utf-8') + b'\r')

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Contrôle de la séquence")

# Création d'un bouton "Start"
start_button = tk.Button(root, text="Start", command=Start_Sweep)
start_button.pack(pady=20)

# Lancer la boucle principale de tkinter
root.mainloop()