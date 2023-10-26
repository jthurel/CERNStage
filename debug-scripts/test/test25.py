import tkinter as tk
from tkinter import filedialog
import os
import time
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

class GP102ControlApp:
    def __init__(self, root):
        self.root = root
        root.title("GP102 control board")
        self.port = None
        self.ser = None
        self.source = []
        self.Folder = []

        search_result = tk.StringVar()
        search_port_button = tk.Button(root, text="Search Port", command=self.update_search_result)
        search_port_button.grid(row=0, column=0, columnspan=2, sticky="ew")

        search_port_entry = tk.Entry(root, textvariable=search_result)
        search_port_entry.grid(row=0, column=2, sticky="ew")

        source = []
        upload_button = tk.Button(root, text="Upload Config", command=lambda: [source.append(self.upload_config()), self.update_entry(source, text_source)])
        upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

        text_source = tk.StringVar()
        upload_entry = tk.Entry(root, textvariable=text_source)
        upload_entry.grid(row=1, column=2, sticky="ew")

        send_config_button = tk.Button(root, text="Send Config to TFA", command=self.send_config)
        send_config_button.grid(row=2, column=0, sticky="ew")

        view_config_button = tk.Button(root, text="View Config file", command=self.view_config)
        view_config_button.grid(row=2, column=1, sticky="ew")

        view_signal_button = tk.Button(root, text="View sinusoidal signal", command=self.view_signal)
        view_signal_button.grid(row=2, column=2, sticky="ew")

        start_sweep_button = tk.Button(root, text="Start Sweep", command=self.start_sweep)
        start_sweep_button.grid(row=4, column=0, columnspan=1, sticky="ew")

        start_sweep_result = tk.StringVar()
        start_sweep_entry = tk.Entry(root, textvariable=start_sweep_result)
        start_sweep_entry.grid(row=4, column=2, sticky="ew")

        abort_sweep_button = tk.Button(root, text="Abort Sweep", command=self.abort_sweep)
        abort_sweep_button.grid(row=4, column=1, columnspan=1, sticky="ew")

        label = tk.Label(root, text="Generator control:")
        label.grid(row=3, column=0)
        generator_on_button = tk.Button(root, text="ON", command=self.turn_on)
        generator_on_button.grid(row=3, column=1, columnspan=1, sticky="ew")
        generator_off_button = tk.Button(root, text="OFF", command=self.turn_off)
        generator_off_button.grid(row=3, column=2, columnspan=1, sticky="ew")

        data_folder_button = tk.Button(root, text="Select data folder", command=lambda: [self.Folder.extend(self.select_folder()), self.update_folder_entry(self.Folder, data_folder_result)])
        data_folder_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        data_folder_result = tk.StringVar()
        data_folder_entry = tk.Entry(root, textvariable=data_folder_result)
        data_folder_entry.grid(row=5, column=2, sticky="ew")

        download_data_button = tk.Button(root, text="Download data", command=self.download_data)
        download_data_button.grid(row=6, column=0, columnspan=2, sticky="ew")

        download_data_result = tk.StringVar()
        download_data_entry = tk.Entry(root, textvariable=download_data_result)
        download_data_entry.grid(row=6, column=2, sticky="ew")

        bouton_quit = tk.Button(root, text="Quit", command=self.button_quit, bg="#FF0000")
        bouton_quit.grid(row=7, column=2)

    def search_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            try:
                ser = serial.Serial(port.device, baudrate=19200, timeout=2)
                ser.write(bytes("*IDN?", 'utf-8') + b'\r')
                response = ser.readline().decode('ascii')
                ser.close()
                if "GP102" in response:
                    return port.device
            except (OSError, serial.SerialException):
                continue
        return "Aucun port trouvé"

    def update_search_result(self):
        self.port = self.search_port()
        search_result.set(self.port)

    def upload_config(self):
        selected_file = []
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            selected_file.append(file_name)
            selected_file.append(file_path)
            selected_file.append(os.path.dirname(file_path))
            selected_file.append(os.path.getsize(file_path))
        return selected_file

    def send_config(self):
        status = "The data has been received by the device"
        if self.source:
            selected_file_path = self.source[1]
            lignes_sans_commentaires = self.lire_fichier_sans_commentaires(selected_file_path)
            for line in lignes_sans_commentaires:
                parts = line.strip().split(',')
                if 1 <= len(parts) <= 4:
                    command = parts[0]
                    values = parts[1:]
                    self.ser.write(f"{command},{','.join(values)}\n".encode())
                    self.ser.write(bytes("*ESR?", 'utf-8') + b'\r')
                    response = self.ser.readline().decode('ascii')
                    if response.strip() != '0':
                        print("Problème dans votre fichier de configuration:", command, response)
                        status = "Veuillez corriger votre fichier de configuration"
        return status

    def view_config(self):
        if self.source:
            try:
                with open(self.source[1], 'r') as file:
                    content = file.read()
                    view_window = tk.Toplevel(self.root)
                    view_window.title("Contenu du fichier de configuration")
                    text_widget = tk.Text(view_window)
                    text_widget.insert(tk.END, content)
                    text_widget.pack()
                return "Contenu du fichier de configuration affiché"
            except Exception as e:
                return f"Erreur lors de l'affichage du fichier de configuration : {e}"
        return "Aucun fichier de configuration sélectionné"

def view_signal(self):
        # Implement the view_signal function here

    def start_sweep(self):
        with serial.Serial(self.port, baudrate=19200, timeout=2) as ser:
            ser.write(bytes("START", 'utf-8') + b'\r')
        start_sweep_result.set("Sweeping")

    def abort_sweep(self):
        with serial.Serial(self.port, baudrate=19200, timeout=2) as ser:
            ser.write(bytes("ABORT", 'utf-8') + b'\r')
        start_sweep_result.set("Aborted")

    def turn_on(self):
        self.send_command("ON")

    def turn_off(self):
        self.send_command("OFF")

    def select_folder(self):
        selected_folder = []
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            selected_folder.append(folder_path)
        return selected_folder

    def update_folder_entry(self, variable, upload_data):
        if variable:
            upload_data.set(variable[0])
        else:
            upload_data.set("")

    def download_data(self):
        results = ""
        self.ser.reset_input_buffer()
        self.ser.write(bytes("DAV?", 'UTF-8') + b'\r')
        time.sleep(0.5)
        while self.ser.in_waiting < 0:
            pass
        while self.ser.in_waiting > 0:
            data_ready = self.ser.read(self.ser.in_waiting).decode('ascii')
        if "15" in data_ready:
            self.ser.reset_input_buffer()
            self.ser.write(bytes("GAINPH?SWEEP", 'UTF-8') + b'\r')
            while self.ser.in_waiting <= 0:
                pass
            while self.ser.in_waiting > 0:
                results += self.ser.read(self.ser.in_waiting).decode('ascii')
                time.sleep(0.05)
            results = "Frequency,Magnitude_1,Magnitude_2,dB,Phase\n" + results
            print(results)
            with open('test.csv', "w", encoding="utf-8") as f:
                f.write(results.replace("\r", ""))

    def button_quit(self):
        result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?\n\nAll processes will be stopped/killed.")
        if result == "yes":
            if self.ser:
                self.ser.close()
            self.root.quit()
            self.root.destroy()

    def send_command(self, command):
        if self.ser != "Aucun port trouvé":
            if command == "ON":
                self.ser.write(bytes("OUTPUT,ON", 'utf-8') + b'\r')
            elif command == "OFF":
                self.ser.write(bytes("OUTPUT,OFF", 'utf-8') + b'\r')
        else:
            print("Aucun port série n'est défini.")

    def lire_fichier_sans_commentaires(self, file_path):
        lignes_lues = []
        try:
            with open(file_path, 'r') as fichier:
                for ligne in fichier:
                    ligne = ligne.strip()
                    if not ligne.startswith("#"):
                        lignes_lues.append(ligne)
        except FileNotFoundError:
            print(f"Le fichier '{file_path}' est introuvable.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
        return lignes_lues

if __name__ == "__main__":
    root = tk.Tk()
    app = GP102ControlApp(root)
    root.mainloop()