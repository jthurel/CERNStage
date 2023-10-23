
# Ouvrir le fichier en mode lecture
with open("Data_files", "r") as file:
    # Lire toutes les lignes du fichier dans une liste
    lines = file.readlines()

# Ouvrir le fichier en mode écriture
with open("Data_files_without_comment.txt", "w") as output_file:
    for line in lines:
        # Exclure les lignes commençant par le caractère "#"
        if not line.strip().startswith("#"):
            # Écrire les lignes non exclues dans le fichier de sortie
            output_file.write(line)