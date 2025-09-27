from tkinter import *
from utils.handle_death import read_death
from utils.capture import capture_screen
import threading

root = Tk()
counter = read_death()
lock = threading.Lock() 

root.title("Death Counter Overlay")
x="10"     
y="10" 

root.geometry(f'250x150+{x}+{y}') 

# to remove the titlebar     
root.overrideredirect(True) 

root.attributes("-topmost", True)
root.attributes("-transparentcolor", "black")
root.config(bg="black") 
l=Label(root,text=f"Deaths: {counter}",fg="white",font=("Arial",20),bg="black")     
l.pack()

b=Label(root,text=f"Time: ",fg="white",font=("Arial",20),bg="black")    
b.pack()

def start_overlay():


    thread = threading.Thread(target=capture_screen, daemon=True)
    thread.start()

    # make window to be always on top
    root.wm_attributes("-topmost", 1)
    root.after(1000, update_counter)
    root.mainloop()

def update_counter():
    with lock:
        counter = read_death()
        l.config(text=f"Deaths: {counter}")
    
    root.after(1000, update_counter)