import tkinter as tk

from impact_screens import screen_manager

root = tk.Tk()
root.geometry("800x480")
root.configure(bg="black")

# screen image holder
screen_holder = tk.Label(root)
screen_holder.pack()

# create screen manager
manager = screen_manager(root, screen_holder)

root.after(500, manager.handle_screens)
# set bindings
root.bind("<Button-1>", manager.handle_press)

# set bindings
root.mainloop()
