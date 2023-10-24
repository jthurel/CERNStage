# Initialisez une variable booléenne pour vérifier si validation est égal à zéro
validation_zero = False
import tkinter as tk
from tkinter import filedialog
import serial
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)
#validation = 0

def lire_fichier_sans_commentaires(filepath):
    lignes_lues = []

    try:
        with open(filepath, 'r') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()  # Supprimer les espaces et les sauts de ligne au début et à la fin
                if not ligne.startswith("#"):
                    lignes_lues.append(ligne)

    except FileNotFoundError:
        print(f"Le fichier '{filepath}' est introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")

    return lignes_lues

def select_file():
    global validation
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text=f"Fichier sélectionné : {file_path}")
        lignes_sans_commentaires = lire_fichier_sans_commentaires(file_path)

        for line in lignes_sans_commentaires:
            # Divisez chaque ligne en parties (nom de commande, valeur1, valeur2, valeur3)
            parts = line.strip().split(',')
            if 1 <= len(parts) <= 4:  # Vous pouvez avoir de 1 à 4 éléments
                command = parts[0]
                values = parts[1:]  # Les valeurs peuvent être vides si elles sont absentes
                # Envoyez la commande et les valeurs via le port série
                ser.write(f"{command},{','.join(values)}\n".encode())
                ser.write(bytes("*ESR?", 'utf-8') + b'\r')
                response = ser.readline().decode('ascii')
                #print (response)


                while True:
                    response = ser.readline().decode('ascii')
                    print(response)

                    if response.strip() == '0':
                        if not validation_zero:  # Si c'est la première fois que validation est zéro
                            validation_zero = True
                            print("Attention")
                    else:
                        validation_zero = False  # Réinitialisez la condition lorsque validation n'est pas zéro

                    #print(command, response)  # Faites ce que vous devez faire avec command et response ici


                #if response.strip() == 0:
                #    validation = 1
                #if response.strip() != '0': #If the answer is not 0 that means there is a probleme in the config file
                #    validation = 0
                #    print("problem on your config file : ",command, response) #Where is the probleme in the config file
                #if ser.readline().decode('ascii')!=0:  # problème reponse=0 mais !=0 car 0 ascii != 0
                #    print ( command , ser.readline().decode('ascii'))

# Création de la fenêtre principale
root = tk.Tk()
root.title("Selection of configuration file")

# Création d'un bouton pour sélectionner un fichier
select_button = tk.Button(root, text="Select a configuration file", command=select_file)
select_button.pack(pady=20)

# Création d'une étiquette pour afficher le chemin du fichier sélectionné
label = tk.Label(root, text="")
label.pack()

# Lancer la boucle principale de tkinter
root.mainloop()