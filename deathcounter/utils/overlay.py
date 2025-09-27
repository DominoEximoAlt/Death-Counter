from tkinter import *
from utils.handle_death import *
from utils.capture import capture_screen
import threading
from utils.timer import Timer
t = Timer.get_instance()
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

def start_overlay():

    thread = threading.Thread(target=capture_screen, daemon=True)
    thread.start()

    

    # make window to be always on top
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
    
    root.after(1000, update_counter)


def stop_overlay(e):
        t._persist()
        root.destroy()

