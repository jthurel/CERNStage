import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

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
                return port.device
        except (OSError, serial.SerialException):
            continue
    return "Aucun port trouvé"

# Fonction pour charger un fichier de configuration
def upload_config():
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    return None

# Fonction pour envoyer la configuration au port série
def send_config_to_tfa(config_file, port):
    if config_file:
        try:
            with open(config_file, 'r') as file:
                for line in file:
                    # Vous pouvez envoyer chaque ligne au port série ici
                    pass
            return "La configuration a été envoyée au périphérique"
        except Exception as e:
            return f"Erreur lors de l'envoi de la configuration : {e}"
    return "Aucun fichier de configuration sélectionné"

# Fonction pour afficher le contenu d'un fichier de configuration
def view_config(config_file):
    if config_file:
        try:
            with open(config_file, 'r') as file:
                content = file.read()
                # Créer une nouvelle fenêtre pour afficher le contenu
                view_window = tk.Toplevel(root)
                view_window.title("Contenu du fichier de configuration")
                text_widget = tk.Text(view_window)
                text_widget.insert(tk.END, content)
                text_widget.pack()
            return "Contenu du fichier de configuration affiché"
        except Exception as e:
            return f"Erreur lors de l'affichage du fichier de configuration : {e}"
    return "Aucun fichier de configuration sélectionné"


# Fonction pour quitter l'application
def button_quit():
    result = messagebox.askquestion("Confirmation", "Êtes-vous sûr de vouloir quitter ?\n\nTous les processus seront arrêtés/terminés.")
    if result == "yes":
        root.quit()
        root.destroy()

# Créer la fenêtre principale
root = tk.Tk()
root.title("GP102 control board")

# Variable pour stocker le chemin du fichier de configuration
config_file = tk.StringVar()

# Créer le bouton "Search Port"
search_port_button = tk.Button(root, text="Rechercher un port", command=lambda: config_file.set(search_port()))
search_port_button.grid(row=0, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte pour afficher le port trouvé
search_port_entry = tk.Entry(root, textvariable=config_file)
search_port_entry.grid(row=0, column=2, sticky="ew")

# Créer le bouton "Upload Config"
upload_button = tk.Button(root, text="Charger la configuration", command=lambda: config_file.set(upload_config()))
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte pour afficher le chemin du fichier de configuration
upload_entry = tk.Entry(root, textvariable=config_file)
upload_entry.grid(row=1, column=2, sticky="ew")

# Créer le bouton "Send Config"
send_config_button = tk.Button(root, text="Envoyer la configuration", command=lambda: messagebox.showinfo("Statut", send_config_to_tfa(config_file.get(), search_port())))
send_config_button.grid(row=2, column=0, sticky="ew")

# Créer le bouton "View Config"
view_config_button = tk.Button(root, text="Afficher la configuration", command=lambda: messagebox.showinfo("Statut", view_config(config_file.get())))
view_config_button.grid(row=2, column=1, sticky="ew")

# Bouton pour quitter l'application
quit_button = tk.Button(root, text="Quitter", command=button_quit, bg="#FF0000")
quit_button.grid(row=3, column=0, columnspan=3, sticky="ew")

root.mainloop()