from logging import root
from tkinter import *
import time
import psutil
from utils.handle_death import *
from utils.capture import capture_screen
import threading
from utils.timer import Timer


is_running = False

def start_overlay(game_name, selected_monitor):
    global t, root, l, timer_label, is_running, time_exceeded
    thread0 = threading.Thread(target=look_for_game_window, args=(game_name+".exe",), daemon=True)
    thread0.start()

    while not is_running and not time_exceeded:
        pass

    if time_exceeded:
        return
    
    t = Timer.get_instance(game_name)
    root = Tk()
    counter = t.get_deaths()
    time = t.get_elapsed()
    root.title("Death Counter Overlay")
    x="10"     
    y="10" 

    root.geometry(f'250x150+{x}+{y}') 

    # to remove the titlebar     
    root.overrideredirect(True) 
    root.focus_set()
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "black")
    root.config(bg="black") 
    l=Label(root,text=f"Deaths: {counter}",fg="white",font=("Arial",20),bg="black")     
    l.pack()

    timer_label = Label(root,text=f"Time: {time}",fg="white",font=("Arial",20),bg="black")
    timer_label.pack()

    root.wm_attributes("-topmost", 1)

    thread = threading.Thread(target=capture_screen, args=(game_name,selected_monitor,), daemon=True)
    thread.start()

    root.bind("<Escape>", stop_overlay)
    
    update_counter()
    root.mainloop()

def update_counter():
    lock = threading.Lock()
    with lock:
        counter = t.get_deaths()
        l.config(text=f"Deaths: {counter}")

        #time = read_time()
        timer_label.config(text=t.get_formatted())
        if is_running == False:
            stop_overlay(None)
    
    root.after(1000, update_counter)


def stop_overlay(e):
        t._persist()
        root.destroy()

def look_for_game_window(game_process):
    global is_running, time_exceeded
    time_exceeded = False
    time_limit = time.time() + 10
    while True:
        # Implement logic to look for the game window
        time.sleep(2)  # Simulate waiting for the game to start
        for proc in psutil.process_iter(['name']):
            #print(proc.info['name'])
            if proc.info['name'] == game_process:
                is_running = True
                print(proc)
                break
            else:
                is_running = False
        print("is_running:", is_running)
        wait_time = time.time()
        if wait_time > time_limit and not is_running:
            time_exceeded = True
            print("Exiting overlay.")
            break

