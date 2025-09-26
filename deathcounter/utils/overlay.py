from tkinter import *


def start_overlay():
    counter = 0
    root = Tk()
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

    # make window to be always on top
    root.wm_attributes("-topmost", 1)
    root.mainloop()