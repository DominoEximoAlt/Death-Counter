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

REPO = "DominoEximoAlt/Death-Counter"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"



def get_version():
        path = resource_path("deathcounter/version.txt")
        if getattr(sys, "frozen", False):
            print("MEIPASS contents:")
            for root, dirs, files in os.walk(sys._MEIPASS):
                print(root, files)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return "unknown"
        
def start_selector():
    pop_up = Tk()

    thread = threading.Thread(target=check_for_update, daemon=True)
    thread.start()
    thread2 = threading.Thread(target=maybe_prompt_update, daemon=True)
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
        from .overlay import start_overlay
        start_overlay(game_exe, selected_monitor)

    def start_new_run():
        selected_game = game_var.get()
        selected_monitor = monitor_var.get()[-1:]
        global game_exe
        game_exe = GAMES[selected_game][:-4]
        pop_up.destroy()
        from .state import initialize_state
        initialize_state(game_name=game_exe)
        from .overlay import start_overlay
        start_overlay(game_exe, selected_monitor)

    pop_up.protocol('WM_DELETE_WINDOW', pop_up.destroy)
    confirm_button = ttk.Button(pop_up, text="Start", command=confirm_selection)
    confirm_button.pack(pady=10)
    startNew_button = ttk.Button(pop_up, text="Start New", command=start_new_run)
    startNew_button.pack(pady=10)
    Label(pop_up, text=f"Version:" + get_version() + " | Developed by DominoEximoAlt", font=("Arial", 8)).pack(pady=10)
    pop_up.mainloop()
    
    

def maybe_prompt_update():
        result = check_for_update()
        
        if not result:
            return

        latest, url = result
        if messagebox.askyesno(
            "Update available",
            f"A new version ({latest}) is available.\n\nUpdate now?"
        ):
            download_and_update(url)    

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_for_update():
    try:
        r = requests.get(API_URL, timeout=3)
        r.raise_for_status()
        data = r.json()
        latest = data["tag_name"].lstrip("v")
        if Version(latest) > Version(get_version()):
            asset = data["assets"][0]["browser_download_url"]
            return latest, asset

    except Exception:
        return None

    return None



def download_and_update(zip_url):
    import stat
    
    # Get parent directory of current exe (where we'll extract to)
    current_exe = sys.executable
    current_dir = os.path.dirname(current_exe)
    parent_dir = os.path.dirname(current_dir)
    
    # Extract to parent directory, not temp
    extract_dir = os.path.join(parent_dir, "DeathCounter_update")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)
    
    death_counter_extract = os.path.join(extract_dir, "DeathCounter")
    os.makedirs(death_counter_extract, exist_ok=True)
    
    # Download zip
    zip_path = os.path.join(extract_dir, "update.zip")
    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    
    # Extract only the DeathCounter folder from the zip, flattening the structure
    with zipfile.ZipFile(zip_path) as zf:
        for file in zf.namelist():
            if file.startswith("DeathCounter/DeathCounter/"):
                # Remove the "DeathCounter/DeathCounter/" prefix to flatten
                relative_path = file.replace("DeathCounter/DeathCounter/", "", 1)
                if relative_path and not file.endswith('/'):  # Skip if empty or directory
                    target_path = os.path.join(death_counter_extract, relative_path)
                    target_dir = os.path.dirname(target_path)
                    try:
                        os.makedirs(target_dir, exist_ok=True)
                        with zf.open(file) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)
                    except Exception as e:
                        print(f"Warning: Could not extract {file}: {e}")
    
    launch_updater(death_counter_extract)

def launch_updater(new_exe_path):
    current_exe = sys.executable
    updater_path = get_updater_path(current_exe)

    if not os.path.exists(updater_path):
        raise RuntimeError(f"Updater not found: {updater_path}")

    subprocess.Popen([
        updater_path,
        current_exe,
        new_exe_path
    ])

    time.sleep(2)
    os._exit(0)
    
def get_updater_path(current_exe):
    exe_dir = os.path.dirname(current_exe)      # DeathCounter/
    parent_dir = os.path.dirname(exe_dir)
    parent_dir = os.path.dirname(parent_dir)                  # ParentFolder/
    return os.path.join(parent_dir,"updater", "updater", "updater.exe")

    
def start_update_check(root):
    threading.Thread(
        target=maybe_prompt_update,
        args=(root,),
        daemon=True
    ).start()