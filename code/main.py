import tkinter as tk
import os

from impact_screens import screen_manager, set_image, get_image
from time import sleep

# delay to allow graphical target to get up
sleep(5)

root = tk.Tk()
root.geometry("800x480")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# screen image holder
screen_holder = tk.Label(root)
screen_holder.pack()

cwd = os.getcwd()
LOGO_DURATION = 6500
main_logo = get_image(f"{cwd}/screens/1.png")
core_logo = get_image(f"{cwd}/screens/15.png")

def show_main_logo():
	# show the main logo
	global main_logo
	set_image(screen_holder, main_logo)
	root.update()
	
def show_core_logo():
	global core_logo
	# show the core machine logo
	core_logo = get_image(f"{cwd}/screens/15.png")
	set_image(screen_holder, core_logo)
	root.update()

# create screen manager
manager = screen_manager(root, screen_holder)

# show the main logo
show_main_logo()

# show the core machine logo
root.after(LOGO_DURATION, show_core_logo)

root.after((LOGO_DURATION*2), manager.handle_screens)

# set bindings
root.bind("<Button-1>", manager.handle_press)

# set bindings
root.mainloop()
