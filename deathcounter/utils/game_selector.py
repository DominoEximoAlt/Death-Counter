from tkinter import *
from tkinter import ttk
from time import *
from tkinter import messagebox
import tempfile, zipfile, shutil
import subprocess, sys, time
import sys
import os
import mss
import requests
import threading
from packaging.version import Version
from utils.version import __version__

REPO = "DominoEximoAlt/Death-Counter"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

def start_selector():
    pop_up = Tk()

    thread = threading.Thread(target=check_for_update, daemon=True)
    thread.start()
    thread2 = threading.Thread(target=maybe_prompt_update, args=(pop_up,), daemon=True)
    thread2.start()

    GAMES = {
        "Lords of the Fallen": "LOTF2-Win64-Shipping.exe",
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
    try:
        theme_path = resource_path("deathcounter/assets/azure.tcl")
    except Exception:
        theme_path = resource_path("assets/azure.tcl")
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
    Label(pop_up, text=f"Version: {__version__} | Developed by DominoEximoAlt", font=("Arial", 8)).pack(pady=10)

    pop_up.mainloop()
    
    

def maybe_prompt_update(pop_up):
        result = check_for_update()
        
        if not result:
            return

        latest, url = result
        print(url)
        if messagebox.askyesno(
            "Update available",
            f"A new version ({latest}) is available.\n\nUpdate now?"
        ):
            download_and_update(url,pop_up)    

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_for_update():
    try:
        r = requests.get(API_URL, timeout=3)
        print(r)
        r.raise_for_status()
        data = r.json()
        latest = data["tag_name"].lstrip("v")
        if Version(latest) > Version(__version__):
            asset = data["assets"][0]["browser_download_url"]
            return latest, asset

    except Exception:
        return None

    return None



def download_and_update(zip_url, pop_up):
    tmp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(tmp_dir, "update.zip")
    print(zip_path)
    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    extract_dir = os.path.join(tmp_dir, "new")
    zipfile.ZipFile(zip_path).extractall(extract_dir)

    launch_updater(extract_dir, pop_up)

def launch_updater(new_dir, pop_up):
    current_dir = os.path.dirname(sys.executable)
    print(sys.executable)
    print(current_dir)
    updater = f"""
    timeout /t 1 > nul
    rmdir /s /q "{current_dir}"
    move "{new_dir}\\DeathCounter\\" "{current_dir}"
    start "" "{current_dir}\\DeathCounter.exe"
    """

    bat_path = os.path.join(os.getenv("TEMP"), "deathcounter_update.bat")
    with open(bat_path, "w") as f:
        f.write(updater)

    subprocess.Popen(bat_path, shell=True)
    
    sys.exit()
    

def start_update_check(root):
    threading.Thread(
        target=maybe_prompt_update,
        args=(root,),
        daemon=True
    ).start()