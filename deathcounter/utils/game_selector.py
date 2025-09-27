from tkinter import *
from tkinter import ttk
from time import *

def start_selector():
    pop_up = Tk()

    GAMES = {
        "Lords of the Fallen": "LOTF2.exe",
        "Dark Souls 3": "DarkSoulsIII.exe",
        "Elden Ring": "eldenring.exe",
    }

    pop_up.title("Select Game")

    l = Label(pop_up, text="Choose a game to track:", font=("Arial", 12)).pack(pady=10)

    game_var = StringVar(value=list(GAMES.keys())[0])  # default selection
    dropdown = ttk.Combobox(pop_up, textvariable=game_var, values=list(GAMES.keys()), state="readonly")
    dropdown.pack(pady=5)

    def confirm_selection():
        selected_game = game_var.get()
        global game_exe
        game_exe = GAMES[selected_game][:-4]
        pop_up.destroy()
        from utils.overlay import start_overlay
        start_overlay(game_exe)


    confirm_button = ttk.Button(pop_up, text="Start", command=confirm_selection)
    confirm_button.pack(pady=10)

    pop_up.mainloop()
