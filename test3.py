import serial.tools.list_ports

# Liste des ports série disponibles
ports = serial.tools.list_ports.comports()

# Nom du port série que vous cherchez
port_name = '/dev/ttyUSB0'  # Remplacez par le nom du port que vous cherchez

# Vérifiez si le port que vous cherchez est dans la liste des ports disponibles
port_found = any(port.device == port_name for port in ports)

if port_found:
    print(f"Le port série {port_name} est connecté.")
else:
    print(f"Le port série {port_name} n'est pas connecté.")