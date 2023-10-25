import tkinter as tk
import serial.tools.list_ports
import serial

# Fonction pour rechercher un port
def search_port():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                search_result.set(port.device)  # Met à jour le champ de texte avec le port trouvé
                return
        except (OSError, serial.SerialException):
            continue

    search_result.set("Aucun port trouvé")  # Met à jour le champ de texte en cas d'absence de port

# Créer la fenêtre principale
root = tk.Tk()
root.title("GP102 Control Board")

# Créer le bouton "Search Port"
search_button = tk.Button(root, text="Search Port", command=search_port)
search_button.grid(row=0, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Search Port"
search_result = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_result)
search_entry.grid(row=0, column=2, sticky="ew")

# Démarrer la boucle principale de l'interface utilisateur
root.mainloop()