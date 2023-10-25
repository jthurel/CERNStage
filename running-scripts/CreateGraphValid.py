import numpy as np
import matplotlib.pyplot as plt

def ViewSignal(Type, amplit, offset, freqStart, freqEnd):
    # Période d'échantillonnage
    Period_start = 1.0 / freqStart # periode du signal de départ (le temps d'avoir une sinus complete)
    Period_end= 1.0 / freqEnd      # periode du signal de fin (le temps d'avoir une sinus complete) T_end << T_start

    # Créer un tableau de temps pour une période de chaque sinus
    table_start = 1*np.linspace(0, Period_start, 1000) # disposer d'un nombre de points suffisamment important pour tracer la sinus (1000 point par défaut)
    table_end = 5*np.linspace(0, Period_end, 1000)

    if Type == "sinus":
        # Créer les signaux sinusoidaux
        signal_start = amplit * np.sin(2 * np.pi * freqStart * table_start) + offset
        signal_end = amplit * np.sin(2 * np.pi * freqEnd * table_end) + offset

        # Créer la fenêtre du graphique
        fig, ax = plt.subplots(figsize=(10, 6))

        # Tracer le premier signal à gauche (en bleu par exemple)
        ax.plot(table_start, signal_start, color='darkblue')

        # Tracer le deuxième signal à droite (en bleu pour avoir la même couleur)
        ax.plot(table_end + 2*Period_start, signal_end, color='darkblue') # table_end + 2*Period_start > chaque point de table_end est décalé de 2xPeriod_start

        # Ajouter des étiquettes d'axe
        ax.set_xlabel("Temps")
        ax.set_ylabel("Amplitude")

        # Ajouter les valeurs d'amplitude, de fréquence de début et de fréquence de fin en dessous du graphique
        plt.text(-0.61*Period_start / 2, offset + (amplit / 2 ), f"Amplitude: {amplit}", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(Period_start/2.5, -amplit+0.2, f"Fréq. de début: {freqStart} Hz", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(2.0* Period_start, -amplit+0.2, f"Fréq. de fin: {freqEnd} Hz", fontsize=12, color='darkblue', horizontalalignment='center')

        # Afficher le graphique
        plt.show()
    else:
        print("Type de signal non pris en charge. Utilisez 'sinus'.")

# Exemple d'utilisation de la fonction
ViewSignal("sinus", 5, 2, 1, 100)