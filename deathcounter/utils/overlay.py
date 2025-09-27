from tkinter import *
from utils.handle_death import *
from utils.capture import capture_screen
import threading

root = Tk()
counter = read_death()
time = read_time()
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

b=Label(root,text=f"Time: {time}",fg="white",font=("Arial",20),bg="black")    
b.pack()

root.wm_attributes("-topmost", 1)

def start_overlay():

    thread = threading.Thread(target=capture_screen, daemon=True)
    thread.start()

    def stop_overlay(e):
        root.destroy()

    # make window to be always on top
    root.bind("<Escape>", stop_overlay)
    
    update_counter()
    root.mainloop()

def update_counter():
    lock = threading.Lock()
    with lock:
        counter = read_death()
        l.config(text=f"Deaths: {counter}")
        add_time(1)
        time = read_time()
        b.config(text=f"Time: {time}")
    
    root.after(1000, update_counter)




