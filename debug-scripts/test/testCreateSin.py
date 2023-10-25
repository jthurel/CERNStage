import numpy as np
import matplotlib.pyplot as plt

# Fonction pour générer un signal triangle wave
def generate_triangle_wave(t, amplit, offset, freq):
    return amplit * (1 - 4 * abs((t * freq + 0.25) - np.floor(t * freq + 0.25)) - 1) + offset

# Fonction pour générer un signal square wave
def generate_square_wave(t, amplit, offset, freq):
    return amplit * (np.sign(np.sin(2 * np.pi * freq * t))) + offset

# Fonction pour générer un signal leading sawtooth
def generate_leading_sawtooth(t, amplit, offset, freq):
    return amplit * (2 * ((t * freq - np.floor(t * freq)) - 0.5)) + offset

# Fonction pour générer un signal trailing sawtooth
def generate_trailing_sawtooth(t, amplit, offset, freq):
    return amplit * (2 * (t * freq - np.floor(t * freq) - 0.5)) + offset

def ViewSignal(Type, amplit, offset, freq):
    # Période d'échantillonnage
    T = 1.0 / freq

    # Créer un tableau de temps pour une période de chaque signal
    t = np.linspace(0, T, 1000)

    if Type == "triangle":
        signal = generate_triangle_wave(t, amplit, offset, freq)
    elif Type == "square":
        signal = generate_square_wave(t, amplit, offset, freq)
    elif Type == "leading_sawtooth":
        signal = generate_leading_sawtooth(t, amplit, offset, freq)
    elif Type == "trailing_sawtooth":
        signal = generate_trailing_sawtooth(t, amplit, offset, freq)
    else:
        print("Type de signal non pris en charge.")
        return

    # Créer la fenêtre du graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    # Tracer le signal
    ax.plot(t, signal, color='darkblue')

    # Ajouter des étiquettes d'axe
    ax.set_xlabel("Temps")
    ax.set_ylabel("Amplitude")

    # Ajouter les valeurs d'amplitude, de fréquence et de type de signal en dessous du graphique
    plt.text(T / 2, -2.5, f"Amplitude: {amplit}", fontsize=12, color='darkblue', horizontalalignment='center')
    plt.text(T / 2, -3, f"Fréquence: {freq} Hz", fontsize=12, color='darkblue', horizontalalignment='center')
    plt.text(T / 2, -3.5, f"Type: {Type}", fontsize=12, color='darkblue', horizontalalignment='center')

    # Afficher le graphique
    plt.show()

# Exemple d'utilisation de la fonction pour un signal triangle wave
#ViewSignal("leading_sawtooth", 3, 1, 2)

# Exemple d'utilisation de la fonction pour un signal square wave
ViewSignal("trailing_sawtooth", 5, 2, 1)
