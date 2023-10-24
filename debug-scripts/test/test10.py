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

# Exemple d'utilisation
filepath = "votre_fichier.txt"  # Remplacez par le chemin de votre fichier
lignes_sans_commentaires = lire_fichier_sans_commentaires(filepath)

for ligne in lignes_sans_commentaires:
    print(ligne)