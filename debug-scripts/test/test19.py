def send_config():
    #global file_path
    #file_path = filedialog.askopenfilename()
    ##selected_file_path = fileofinterest[1]
    retour="The data has been received by the device"
    global fileofinterest  # Declare fileofinterest as a global variable
    if fileofinterest:
        selected_file_path = fileofinterest[1]
    #if file_path:
        lignes_sans_commentaires = lire_fichier_sans_commentaires(selected_file_path)
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
                if response.strip() != '0': #If the answer is not 0 that means there is a probleme in the config file
                    print("problem on your config file : ",command, response) #Where is the probleme in the config file
                    retour= "please correct your config file"
                #if ser.readline().decode('ascii')!=0:  # problème reponse=0 mais !=0 car 0 ascii != 0
                #    print ( command , ser.readline().decode('ascii'))
    return(retour)
    print (retour)