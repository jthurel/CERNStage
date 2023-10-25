import tkinter as tk

# Fonctions pour obtenir le texte en fonction de la ligne
def get_text_for_line(line_number):
    if line_number == 1:
        return "Texte pour la ligne 1"
    elif line_number == 2:
        return "Texte pour la ligne 2"
    elif line_number == 3:
        return "Texte pour la ligne 3"
    elif line_number == 4:
        return "Texte pour la ligne 4"
    elif line_number == 5:
        return "Texte pour la ligne 5"
    elif line_number == 6:
        return "Texte pour la ligne 6"
    elif line_number == 7:
        return "Texte pour la ligne 7"
    elif line_number == 8:
        return "Texte pour la ligne 8"
    else:
        return "Ligne inconnue"

# Fonction pour mettre à jour le label avec le texte correspondant
def update_label(line_number):
    text = get_text_for_line(line_number)
    label.config(text=text)

# Créer une fenêtre
window = tk.Tk()
window.title("Exemple de fenêtre avec boutons")

# Créer 8 lignes avec un bouton et un label
for line_number in range(1, 9):
    line_frame = tk.Frame(window)
    line_frame.pack()

    button = tk.Button(line_frame, text=f"Ligne {line_number}", command=lambda num=line_number: update_label(num))
    button.pack(side=tk.LEFT)

    label = tk.Label(line_frame, text="Cliquez sur un bouton pour afficher le texte")
    label.pack(side=tk.LEFT)

# Lancer la fenêtre
window.mainloop()