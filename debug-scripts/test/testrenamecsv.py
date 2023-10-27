
import datetime
import subprocess
import platform

fichier = "votre_fichier"

syst_os = platform.system()

if syst_os == "Linux":
    subprocess.run(["xdg-open", fichier])
elif syst_os == "Windows":
    subprocess.run(["start", fichier], shell=True)
else:
    print("Système d'exploitation non pris en charge.")


AMPLIT=1
OFFSET=2
STEPS=20
FREQSTART=10
FREQEND=1000
csvfilename = str(f"GainPhase_AMP{AMPLIT}Vpk_OFS{OFFSET}V_{STEPS}pts_{FREQSTART}-{FREQEND}Hz_datetime.now().strftime('%Y-%m-%d_%H.%M').csv")
path_to_logs= "/home/jthurel/Documents/CERNScripts/debug-scripts"
pathfile= f"{path_to_logs}/{csvfilename}"

print (pathfile)