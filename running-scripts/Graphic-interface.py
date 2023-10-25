import tkinter as tk
from tkinter import messagebox
from time import sleep
import getpass
import subprocess
import psutil
from tkinter import simpledialog
from datetime import datetime, timedelta
import textwrap
import pyfgc
import math
import pyfgc_rbac
import json
import sys

sys.path.append('/user/pclpc/bin/python/scripts/GenericScripts')
import lpc_generic_functions as lpc

######################## Script arguments assignation ####################################################
# Variable passed to script
taskfile = sys.argv[1]

######################## Importing required all files ####################################################
# load task (specifying process + elements (converters)
task    = lpc.import_file(taskfile)
process = lpc.import_file(task.process_target)

######################## Internal variables ####################################################
global buttonkerberos

###########################################################################################################
# generic functions
###########################################################################################################
def collect_username():
    # collect username for sending email once test is completed
    global username
    username = str(getpass.getuser()) # str required for subprocess.Popen
    return username

def manage_email_settings():
    sender = str(f"{username}@cern.ch") # must be a valid cern address
    recipient = str(f"{username}@cern.ch") # "yves.thurel@cern.ch, benoit.favre@cern.ch"
    smtp_host = "cernmx.cern.ch" # cern default
    smtp_port = 25 # cern default

def renew_kerberos_ticket():
    global rbac_token
    # renew kerberos ticket on request
    password = simpledialog.askstring("Pass", "Please enter your password : ", show="*")
    if password:
        try:
            subprocess.run(['kinit'], input=password.encode(), check=True)
            rbac_token = pyfgc_rbac.get_token_kerberos()

        except subprocess.CalledProcessError as e:
            print("An error occurred during kerberos renewal process:", e)

def get_timing_of_kerberos_ticket():
    # calculate remaining time and date time of current kerberos ticket (returns two variables)
    # Execute the 'klist' command to retrieve Kerberos ticket information
    process = subprocess.Popen(['klist'], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # Convert the output to a string
    output_str = output.decode()

    # Search for lines containing ticket expiration dates
    if output_str == "":
        print("No valid Kerberos tickets found.")
        # no valid Kerberos found
        return "None", "None"

    else:
        lines = output_str.split('\n')
        expiration_times = []
        for line in lines:
            if 'renew until' in line.lower():
                expiration_time_str = line.split('renew until ')[1].strip()
                expiration_time = datetime.strptime(expiration_time_str, '%m/%d/%Y %H:%M:%S')
                time_remaining = expiration_time - datetime.now()
                expiration_time = expiration_time.replace(second=0)
                expiration_times.append(expiration_time)

            if expiration_times:
                # Retrieve the first expiration date
                first_expiration_time = expiration_times[0]
                first_expiration_time = first_expiration_time.strftime('%d %b %Y %H:%M')
                return first_expiration_time, time_remaining

#unused function
def is_process_running(process_target, arg):
    #Check if a specific process is already in use
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'python' and task.process_target in process.cmdline() and arg in process.cmdline():
            return True
    return False

def is_any_process_running(arg):
    #Check if a specific process is already in use
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'python' and arg in process.cmdline():
            return True
    return False

def run():
    # run button action. This function only acts if process is not already on. it also calculate the end date of the process when launched.
    button_values = [var_buttons[i].get() for i in range(len(task.elements))]
    for i, value in enumerate(button_values):
        if value:
            # Verify if process was launched with same target not to relaunch it on top of it
            if is_any_process_running(task.elements[i]):
                print(f"Process already launched for target {task.elements[i]}")
                buttons[i].config(text=str(f"{task.elements[i]} ON | REJECTED (IN USE)"), foreground="red");
            else:
                #collect user variable data
                get_values()
                collect_username()
                manage_email_settings()
                #recalculate the real duration of the chosen process
                process_duration = process.estimated_process_duration(launcher_user_inputs)
                # Launch process if not already launched and calculate end date (stored in table at corresponding index
                serialized_process_data = json.dumps(task.process_data) if task.process_data else "{}"
                serialized_process_meas = json.dumps(task.process_meas) if task.process_meas else "{}"
                command = ["python", task.process_target, task.elements[i], username, serialized_process_data, serialized_process_meas] + launcher_user_inputs
                subprocess.Popen(command)
                # calculation of end date
                dateend_calc = datetime.now() + timedelta(seconds=process_duration)
                process_end_date[i] = str(dateend_calc.strftime("%d-%b-%Y %H:%M"))

    return process_end_date

def kill_all():
    # find all subprocess and destroy them
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'python' and task.process_target in process.cmdline():
            process.terminate()

def kill_selected():
    # get the current values of the buttons
    button_values = [var_buttons[i].get() for i in range(len(task.elements))]
    # print the names of the selected task.elements
    for i, value in enumerate(button_values):
        if value:
            print(f"Selected element: {task.elements[i]} KILLING");
            # Verify if process was launched with same target
            for process in psutil.process_iter(['name']):
                if process.info['name'] == 'python' and task.process_target in process.cmdline() and  task.elements[i] in process.cmdline():
                    process.terminate()
                    buttons[i].config(text=str(f"{task.elements[i]} KILLING"));

def spcof_selected():
    # get the current values of the buttons
    button_values = [var_buttons[i].get() for i in range(len(task.elements))]
    # print the names of the selected task.elements
    for i, value in enumerate(button_values):
        if value:
            try:
                pyfgc.set(str(f"{task.elements[i]}"), "PC", "OF", rbac_token=rbac_token)
            except Exception as e:
               # manage case FGC target doesn't exist
               print("Device not accessible")

def refresh():
    global process_end_date
    global k_refresh
    global rbac_token

    # manage rbac_token refreshing from kerberos
    if k_refresh == 3600:
        # after 3600 cycles sleep (1sec), then 1 hour renew rbac_tokn from kerberos
        print("time to refresh rbac_token from kerberos")
        rbac_token = pyfgc_rbac.get_token_kerberos()
        k_refresh = 1
    else:
        k_refresh = k_refresh + 1

    #check rbac validity through kerberos validity
    end_date, time_remaining = get_timing_of_kerberos_ticket()

    if time_remaining == "None":
        # no valid kerberos, do not try to attempt FGC data (would create DOS)
        buttonkerberos.configure(text=str(f"Invalid Kerberos: please press."), bg="red",highlightbackground="red")
        button_values = [var_buttons[i].get() for i in range(len(task.elements))]
        # print the names of the selected task.elements
        for i, value in enumerate(button_values):
            print("Selected element:", task.elements[i]);
            buttons[i].config(text=str(f"{task.elements[i]} [NA; NA] | Invalid RBAC"), foreground="red");
            for process in psutil.process_iter(['name']):
                if process.info['name'] == 'python' and task.process_target in process.cmdline() and  task.elements[i] in process.cmdline():
                    process.terminate()
                    buttons[i].config(text=str(f"{task.elements[i]} [NA; NA] | Invalid RBAC"), foreground="red");
    else:
        # valid kerberos ticket, then rbac
        if time_remaining < timedelta(days=2):
            if time_remaining < timedelta(days=1):
                buttonkerberos.configure(text=str(f"RENEW Kerberos before: {end_date}"), bg="red", highlightbackground="red")
            else:
                buttonkerberos.configure(text=str(f"RENEW Kerberos before: {end_date}"), bg="orange", highlightbackground="orange")
        else:
            buttonkerberos.configure(text=str(f"RENEW Kerberos before: {end_date}"), bg="lightgray", highlightbackground="green")

        # since kerberos ticket is ok, go on with acquiring I,V,status & process
        # get the current values of the buttons
        button_values = [var_buttons[i].get() for i in range(len(task.elements))]
        # print the names of the selected task.elements
        for i, value in enumerate(button_values):

            try:
                vmeas = round(float((pyfgc.get(str(f"{task.elements[i]}"), "MEAS.V.VALUE", rbac_token=rbac_token).value)),1)
            except Exception as e:
            # manage case FGC target doesn't exist
                vmeas = "NA"

            try:
                imeas = round(float((pyfgc.get(str(f"{task.elements[i]}"), "MEAS.I.VALUE", rbac_token=rbac_token).value)),1)
            except Exception as e:
            # manage case FGC target doesn't exist
                imeas = "NA"

            try:
                state = str((pyfgc.get(str(f"{task.elements[i]}"), "STATE.PC", rbac_token=rbac_token).value))
                if state == "IDLE": state ="IL"
                if state == "OFF": state = "OF"
                if state == "FLT_OFF": state = "FO"
                if state == "ARMED": state = "AR"
                if state == "RUNNING": state = "RN"
                if state == "STARTING": state = "ST"
                if state == "TO_STANDBY": state = "SB"
                if state == "ABORTING": state = "AB"
                if state == "STOPPING": state = "SP"
                if state == "FLT_STOPPING": state = "FS"
                if state == "BLOCKING": state = "BK"
            except Exception as e:
            # manage case FGC target doesn't exist
                state = "NA"

            print("Selected element:", task.elements[i]);
            # first reset the button to non-running
            buttons[i].config(text=str(f"{task.elements[i]} [{imeas} A; {vmeas} V] | {state}"), foreground="black");

            # then correct its status if required
            for process in psutil.process_iter(['name']):
                if process.info['name'] == 'python' and task.elements[i] in process.cmdline():
                    buttons[i].config(text=str(f"{task.elements[i]} [{imeas} A; {vmeas} V] | {state} | END: {process_end_date[i]}"), foreground="black");
                    print("detected")

    window.after(1000, refresh)

def button_quit():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?\n\nOn ROG, all processes will be stopped/killed, converters not stopped properly.")
    if result == "yes":
        window.destroy()
        window.quit()


def resize_window():
    global is_maximized

    if is_maximized:
        window.geometry("{}x{}".format(window_width, window_height))  # Restaure la taille initiale de la fenêtre
        button_extra.config(text='▼')
        is_maximized = False
        extra_info.pack_forget()
        for frame in frames:
            frame.pack_forget()
    else:
        window.geometry("{}x{}".format(window_width, window_extra_height))  # Maximise la fenêtre
        button_extra.config(text='▲')
        is_maximized = True
        extra_info.pack(anchor='w', padx=2, pady=3)
        for frame in frames:
            frame.pack(anchor='w', padx=2, pady=3)

def display_text(text, window_width):
    global lines
    wrapper = textwrap.TextWrapper(width=window_width, expand_tabs=False, replace_whitespace=False)
    lines = textwrap.wrap(text, width=window_width)
    justified_lines = [wrapper.fill(line) for line in lines]
    wrapped_text = "\n".join(justified_lines)
    return wrapped_text


def get_values():
    global launcher_user_inputs
    launcher_user_inputs = []
    for entry in entries:
        value = entry.get()
        launcher_user_inputs.append(value)


###########################################################################################################
# Create the main graphical task.elements (window)
window = tk.Tk()
window.title(str(f"{task.converter_name} | {process.process_short_title} | {process.process_version}"))
window.configure(bg=process.process_color)

# Create a list of boolean variables for the check buttons
var_buttons = [tk.BooleanVar() for i in range(len(task.elements))]
# set them activated per default
for var in var_buttons:
    var.set(True)

element_width = 62
button_width=62
# Create the check buttons for each element in the converter list
buttons = []
padys = [5] * (len(task.elements))
for i, element in enumerate(task.elements):
    button = tk.Checkbutton(window, text=str(f"{element}"), variable=var_buttons[i], bg=process.process_color, anchor="w", width=element_width)
    button.pack(pady=padys[i])
    buttons.append(button)

# Create a button to get the current values of the check buttons
buttonrun = tk.Button(window, text="RUN  targeted process on SELECTED device(s)", command=run,  anchor="w", width=button_width)
buttonrun.pack()

# Create a button to kill selected process
buttonkill = tk.Button(window, text="KILL  targeted process on SELECTED device(s)", command=kill_selected, anchor="w", width=button_width)
buttonkill.pack()

# Create a button to Stop selected converters
buttonspcof = tk.Button(window, text="STOP (send S PC OF to)  SELECTED device(s)", command=spcof_selected, anchor="w", width=button_width)
buttonspcof.pack()

# Create a button to kill all process of same nature - unused
buttonkillall = tk.Button(window, text="KILL ALL running targeted processes", command=kill_all, anchor="w", width=button_width)
buttonkillall.pack_forget()

# Create a button to indicate end of ticket kerberos():
end_date, time_remaining = get_timing_of_kerberos_ticket()
buttonkerberos = tk.Button(window, text=str(f"RENEW Kerberos before: {end_date}"), command=renew_kerberos_ticket, anchor="w", width=button_width)
buttonkerberos.pack()

# Create a button to kill selected process
button = tk.Button(window, text="EXIT (not recommended with on-going process)", command=button_quit,  anchor="w", width=button_width)
button.pack()

# Add button for more choices
button_extra = tk.Button(window, text='▼', command=resize_window)
button_extra.pack(padx=(19,5), pady=10, side=tk.LEFT, anchor=tk.N)

# Add internet link
link_label = tk.Label(window, text=str(f"Process: {process.process_long_title} (EDMS link)"), cursor="hand2", font=("Arial",9), bg=process.process_color, foreground="blue")
link_label.pack(pady=15, anchor=tk.NW)
def open_link(event):
    # define the function to open the link in a web browser
    import webbrowser
    webbrowser.open_new(task.process_link)
link_label.bind("<Button-1>", open_link)    # bind the label to the function when clicked

# Create the extra info indication
wrapped_text = display_text(process.process_info, element_width+14) # justify the text and fit it in the window dimension.
extra_info = tk.Label(window, text=wrapped_text, anchor="w", justify="left", width=55, bg=process.process_color)
extra_info.pack_forget()

# Manage all user data entry fields (aligned thanks to field width
variable_field_width = element_width-25

frames = []
labels = []
entries = []

for variable in task.process_user_inputs:
    frame = tk.Frame(window)
    frame.pack_forget()
    frames.append(frame)

    label = tk.Label(frame, text=variable[0], anchor='w', width=variable_field_width, bg=process.process_color)
    label.pack(side=tk.LEFT)
    labels.append(label)

    entry = tk.Entry(frame, justify='right', width=20)
    entry.pack(side=tk.LEFT)
    entry.insert(tk.END, variable[1])
    entries.append(entry)

# adjust the window size based on the number of initial buttons (window.winfo_reqheight() not found suitable) - 15 (text) & 26 (variable input cases) found by testing
window_height = len(task.elements) * 22 + 60 + 2 * sum([pady for pady in padys]) + 5 * (25)
window_width = 500 # =window.winfo_reqwidth()
window.geometry("{}x{}".format(window_width, window_height))
window_extra_height = window_height + len(lines) * 15 + len(task.process_user_inputs) * 26  + 14# adjust using number of lines of wrapped text + number of variables


######################## MAIN PROGRAM #####################################################################

# Initialise initial state (extra information status)
# get rbac_token from kerberos ticket
global rbac_token
k_refresh = 1

try:
    rbac_token = pyfgc_rbac.get_token_kerberos()
except Exception as e:
    # manage case FGC target doesn't exist
    sys.exit(0)

#initialize variables
process_end_date = ["Unknown" for _ in range(len(task.elements))]
is_maximized = False

# Run main prog (refresh, in loop mode, refreshing & V,I,status of converter, & Kerberos status)
refresh()
window.mainloop()