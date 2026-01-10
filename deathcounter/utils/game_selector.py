from tkinter import *
from tkinter import ttk
from time import *
import sys
import os
import mss

def start_selector():
    pop_up = Tk()

    GAMES = {
        "Lords of the Fallen": "LOTF2-Win64-Shipping.exe",
        "Dark Souls 3": "DarkSoulsIII.exe",
        "Dark Souls REMASTERED": "DarkSoulsRemastered.exe",
        "Sekiro": "sekiro.exe",
        "Elden Ring": "eldenring.exe",
    }

    pop_up.title("Select Game")
    pop_up.eval('tk::PlaceWindow . center')
    Label(pop_up, text="Choose a game to track:", font=("Arial", 12)).pack(pady=10)

    monitors = mss.mss().monitors.__len__() - 1
    monitor_names = [f"Monitor {i}" for i in range(1, monitors + 1)]
    #monitor_names = [f"Monitor {i}" for i in monitors if i != 0]
    game_var = StringVar(value=list(GAMES.keys())[0])  # default selection
    monitor_var = StringVar(value=monitor_names[0])  # default selection
    dropdown = ttk.Combobox(pop_up, textvariable=game_var, values=list(GAMES.keys()), state="readonly")
    dropdown2 = ttk.Combobox(pop_up, textvariable=monitor_var, values=list(monitor_names), state="readonly")

    dropdown.pack(pady=5)
    dropdown2.pack(pady=5)
    ## Set theme
    theme_path = resource_path("deathcounter/assets/azure.tcl")
    pop_up.tk.call("source", theme_path)
    pop_up.tk.call("set_theme", "dark")
    def confirm_selection():
        selected_game = game_var.get()
        selected_monitor = monitor_var.get()[-1:]
        global game_exe
        game_exe = GAMES[selected_game][:-4]
        pop_up.destroy()
        from utils.overlay import start_overlay
        start_overlay(game_exe, selected_monitor)
    def start_new_run():
        selected_game = game_var.get()
        selected_monitor = monitor_var.get()[-1:]
        global game_exe
        game_exe = GAMES[selected_game][:-4]
        pop_up.destroy()
        from utils.state import initialize_state
        initialize_state(game_name=game_exe)
        from utils.overlay import start_overlay
        start_overlay(game_exe, selected_monitor)

    pop_up.protocol('WM_DELETE_WINDOW', pop_up.destroy)
    confirm_button = ttk.Button(pop_up, text="Start", command=confirm_selection)
    confirm_button.pack(pady=10)
    startNew_button = ttk.Button(pop_up, text="Start New", command=start_new_run)
    startNew_button.pack(pady=10)

    pop_up.mainloop()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
