import tkinter as tk
import serial

# Définition de la fonction Stop_Sweep
def Stop_Sweep():
    with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
        ser.write(bytes("STOP", 'utf-8') + b'\r')

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Contrôle de la séquence")

# Création d'un bouton "Stop"
stop_button = tk.Button(root, text="Stop", command=Stop_Sweep)
stop_button.pack(pady=20)

# Lancer la boucle principale de tkinter
root.mainloop()