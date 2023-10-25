def find(fichier, mot, position):
    try:
        with open(fichier, 'r') as file:
            for line in file:
                if mot in line:
                    parts = line.split(',')
                    if len(parts) > position:
                        value = parts[position].strip()
                        if value.isnumeric():
                            return int(value)
                        elif value.replace('.', '', 1).isdigit():
                            return float(value)
        return None  # Si le mot n'est pas trouvé ou la position est invalide
    except FileNotFoundError:
        print(f"Le fichier '{fichier}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

# Exemple d'utilisation
fichier = '/home/jthurel/Documents/CERNScripts/config file/Data_files'  # Remplacez par le nom de votre fichier
mot = 'FSWEEP'  # Remplacez par le mot que vous voulez chercher
position = 3  # Remplacez par le nombre de virgules à ignorer

valeur = find(fichier, mot, position)

if valeur is not None:
    print(f"La valeur numérique après '{mot}' à la position {position} est : {valeur}")
else:
    print(f"Le mot '{mot}' n'a pas été trouvé dans le fichier.")

# Exemple d'utilisation

valeur = find(fichier,'AMPLIT',1)