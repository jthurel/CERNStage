import tkinter as tk
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