import numpy as np
import matplotlib.pyplot as plt

def ViewSignal(Type, amplit, offset, freqStart, freqEnd):
    # Période d'échantillonnage
    T = 1.0 / max(freqStart, freqEnd)

    # Créer un tableau de temps pour une période de la première sinus
    t_start = np.linspace(0, T, 1000)

    # Créer un tableau de temps pour une période de la deuxième sinus
    t_end = np.linspace(0, T, 1000)

    if Type == "sinus":
        # Créer les signaux sinusoidaux
        signal_start = amplit * np.sin(2 * np.pi * freqStart * t_start) + offset
        signal_end = amplit * np.sin(2 * np.pi * freqEnd * t_end) + offset

        # Créer l'espace vide entre les deux signaux de la longueur d'une période de la première sinus
        empty_space = [0] * len(t_start)

        # Concaténer les signaux
        combined_signal = np.concatenate((signal_start, empty_space, signal_end))

        # Créer la fenêtre du graphique
        plt.figure(figsize=(10, 6))

        # Tracer le signal combiné
        plt.plot(np.arange(len(combined_signal)), combined_signal)

        # Ajouter des légendes et des étiquettes d'axe
        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")

        # Afficher le graphique
        plt.show()
    else:
        print("Type de signal non pris en charge. Utilisez 'sinus'.")

# Exemple d'utilisation de la fonction
ViewSignal("sinus", 5, 2, 1, 100)