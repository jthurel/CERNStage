import numpy as np
import matplotlib.pyplot as plt

def ViewSignal(Type, amplit, offset, freqStart, freqEnd):
    # Période d'échantillonnage
    T = 1.0 / min(freqStart, freqEnd)

    # Créer un tableau de temps pour une période de chaque sinus
    t_start = np.linspace(0, T, 1000)
    t_end = np.linspace(0, T, 1000)

    if Type == "sinus":
        # Créer les signaux sinusoidaux
        signal_start = amplit * np.sin(2 * np.pi * freqStart * t_start) + offset
        signal_end = amplit * np.sin(2 * np.pi * freqEnd * t_end) + offset

        # Créer la fenêtre du graphique
        fig, ax = plt.subplots(figsize=(10, 6))

        # Tracer le premier signal à gauche (en bleu par exemple)
        ax.plot(t_start, signal_start, color='darkblue')

        # Tracer le deuxième signal à droite (en bleu pour avoir la même couleur)
        ax.plot(t_start + 2*T, signal_end, color='darkblue')

        # Ajouter des étiquettes d'axe
        ax.set_xlabel("Temps")
        ax.set_ylabel("Amplitude")

        # Ajouter les valeurs d'amplitude, de fréquence de début et de fréquence de fin en dessous du graphique
        plt.text(-0.5*T / 2, -4.8, f"Amplitude: {amplit}", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(T / 2, -4.8, f"Fréq. de début: {freqStart} Hz", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(2.5 * T, -4.8, f"Fréq. de fin: {freqEnd} Hz", fontsize=12, color='darkblue', horizontalalignment='center')

        # Afficher le graphique
        plt.show()
    else:
        print("Type de signal non pris en charge. Utilisez 'sinus'.")

# Exemple d'utilisation de la fonction
ViewSignal("sinus", 5, 2, 1, 100)