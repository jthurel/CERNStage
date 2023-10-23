
import serial
import serial.tools.list_ports;
import time
import json
import copy

state = "init"

#Param name: [param value, param type(int or string), command name, command number]
parameters = {
    "Generator_amplitude":      [10E-3, 0, "AMPLIT", 49],
    "Generator_freq":           [1, 0, "FREQUE", 48],
    "Generator_offset":         [0, 0, "OFFSET", 50],
    "Generator_waveform":       ["sine", 1, "WAVEFO", 51],
    "Generator_output":         ["on", 1, "OUTPUT", 7],
    "Sweep_startFreq":          [1, 0, None, 19],
    "Sweep_stopFreq":           [100, 0, None, 20],
    "Sweep_steps":              [10, 0, None, 18],
    "Sweep_repetition":         ["single", 1, None, 21],
    "Sweep_phase":              ["0to360", 1, None, 6],
    "Analyser_speed":           ["medium", 1, "SPEED", 13],
    "Analyser_filter":          ["slow", 1, None, 14],
    "Analyser_filterDynamics":  ["auto", 1, None, 15],
    "Analyser_offset":          [0, 0, "ZERO,DB", 148],
    "Analyser_lowFreqOff":      ["off", 1, "LOWFRE", 11],
    "Channel_1_minRange":       [10E-3, 0, None, 26],
    "Channel_1_autoranging":    ["auto", 1, None, 28],
    "Channel_1_coupling":       ["ac+dc", 1, "COUPLI,CH1", 30],
    "Channel_1_scaling":        [1, 0, "SCALE,CH1", 32],
    "Channel_2_minRange":       [10E-3, 0, None, 27],
    "Channel_2_autoranging":    ["auto", 1, None, 29],
    "Channel_2_coupling":       ["ac+dc", 1, "COUPLI,CH2", 31],
    "Channel_2_scaling":        [1, 0, "SCALE,CH2", 33],
    "Trim_resolution":          ["auto", 1, "RESOLU", 41],
    "Trim_acTrim":              ["off", 1, None, 186],
    "Trim_acLevel":             [1, 0, None, 188],
    "Trim_tolerance":           [1, 0, None, 190]
}

def load_parameters():
    global parameters
    global state

    #Open parameter.json file
    try:
        with open("parameters.json") as parameter_file:
            temp_parameters = json.load(parameter_file)
    except:
        print("parameters.json file could not be opened. Make sure such file exists and has correct syntax\nDefault parameters will be used")
        return #If unsuccessful exit function

    #Check for invalind parameters and update parameters from file
    invalid_parameters = set(temp_parameters) - set(parameters)
    for param in invalid_parameters:
        temp_parameters.pop(param)
        print("Invalid parameter \"" + param + "\" will be ignored")
    print("\n")
    for key, value in temp_parameters.items():
        temp_value = parameters[key]
        temp_value[0] = value
        parameters[key] = temp_value
    for key, value in parameters.items():
        print(f'{key:<23}', ":", value[0])

    print("\n")

def init():
    global state
    global ser
    print("0: exit\n1: scan COM ports\n2: open COM port\n3: reload parameters")
    option = input()
    match option:
        case "0":
            state = "exit"
        case "1":
            comports = serial.tools.list_ports.comports()
            for comport in comports:
                print(comport.description)
            print("\n")
        case "2":
            print("enter COM port(COMx or /dev/tty)")
            option = input()
            try:
                ser = serial.Serial(option, 19200, timeout=1)
            except:
                print("Unable to open " + option + "\n")
            else:
                ser.rts = True
                print("port is open\n")
                state = "port_open"
        case "3":
            load_parameters()

def port_open():
    global state
    global ser
    print("0: close connection\n1: reload parameter file\n2: start sweep\n")
    option = input()
    match option:
        case "0":
            ser.close()
            print("connection closed\n")
            state = "init"
        case "1":
            load_parameters()
        case "2":
            state = "start_sweep"

def start_sweep():
    #Parameter value string to integer mapping
    ZERO = {'off', 'sine', 'very slow', 'single', '-180to180', 'auto reset', 'normal', 'auto', 'ac+dc'}
    ONE = {'on', 'triangle', 'slow', 'continuous', '0to360', 'fixed time', 'auto_up', 'ac_<10Vdc', 'ch1', 'fine'}
    TWO = {'square', 'medium', 'none', 'manual', 'ac_<500Vdc', 'ch2'}
    THREE = {'leading sawtooth', 'fast'}
    FOUR = {'trailing sawtooth'}
    global state
    global parameters
    global ser

    abort_sweep = False

    ser.write(bytes("ABORT", 'UTF-8') + b'\r')
    time.sleep(1)
    ser.write(bytes("MODE,GAINPH", 'UTF-8') + b'\r')
    time.sleep(3)
    
    for key, value in parameters.items():
        if value[1] == 1:
            if value[0] in ZERO:
                temp_value = 0
            elif value[0] in ONE:
                temp_value = 1
            elif value[0] in TWO:
                temp_value = 2
            elif value[0] in THREE:
                temp_value = 3
            else:
                abort_sweep = True
                print(str(value[0]) + " is not a valid value for: " + key)
                continue
        else:
            temp_value = value[0]
        ser.write(bytes("CONFIG," + str(value[3]) + "," + str(temp_value), 'UTF-8') + b'\r')
    if abort_sweep:
        state = "port_open"
        return
    print("Sweeping...")
    #ser.write(bytes("MODE,GAINPH", 'UTF-8') + b'\r')
    time.sleep(4)
    #ser.write(bytes("OUTPUT,ON", 'UTF-8') + b'\r')
    ser.write(bytes("START", 'UTF-8') + b'\r')
    state = "sweeping"
    #state = "port_open"

def sweeping():
    global state
    results = ""
    ser.reset_input_buffer()
    ser.write(bytes("DAV?", 'UTF-8') + b'\r')
    time.sleep(0.5)
    while ser.in_waiting < 0:
        pass
    while ser.in_waiting > 0:
        data_ready = ser.read(ser.in_waiting).decode('ascii')
    if "15" in data_ready:
        ser.reset_input_buffer()
        ser.write(bytes("GAINPH?SWEEP", 'UTF-8') + b'\r')
        while ser.in_waiting <= 0:
            pass
        while ser.in_waiting > 0:
            results += ser.read(ser.in_waiting).decode('ascii')
            time.sleep(0.05)
        results = "Frequency,Magnitude_1,Magnitude_2,dB,Phase\n" + results
        print(results)
        with open('test.csv', "w", encoding="utf-8") as f:
            f.write(results.replace("\r", ""))
        state = "port_open"

load_parameters()

while True:
    match state:
        case "init":
            init()
        case "port_open":
            port_open()
        case "start_sweep":
            start_sweep()
        case "sweeping":
            sweeping()
        case "exit":
            break
    
    
