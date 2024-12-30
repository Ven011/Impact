import tkinter as tk
import os

from button import Button
from PIL import Image, ImageTk
from workout_manager import Workout_manager
from functools import partial
from time import time

cwd = os.getcwd()
wm = Workout_manager()

def get_image(location):
    image = Image.open(location)
    # resize to fit screen
    image = image.resize((800, 480))

    return ImageTk.PhotoImage(image)

def set_image(image_holder: tk.Label, image: tk.PhotoImage):
    image_holder.config(image=image)

class main_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "main"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        self.curr_image = None
        
        self.images = {
            "training": get_image(f"{cwd}/screens/2.png"),
            "rounds": get_image(f"{cwd}/screens/3.png"),
        }

        self.buttons = [
            Button(self.name, "training", 0, 42, 374, 310, self.training_action),
            Button(self.name, "rounds", 375, 42, 800, 310, self.rounds_action),
            Button(self.name, "start", 209, 355, 606, 434, self.start_action)
        ]

    def prepare(self):
        wm.set_mode(wm.TRAINING)

    def run(self, press_event: tk.Event):
        if self.curr_image is None: set_image(self.holder, self.images["training"])

        # check whether buttons have been pressed
        if press_event is not None: 
            for button in self.buttons: button.check_if_pressed(press_x=press_event.x, press_y=press_event.y)

    def training_action(self):
        set_image(self.holder, self.images["training"]) if self.curr_image != "training" else 0
        self.curr_image = "training"
        wm.set_mode(wm.TRAINING)

    def rounds_action(self):
        set_image(self.holder, self.images["rounds"]) if self.curr_image != "rounds" else 0
        self.curr_image = "rounds"
        wm.set_mode(wm.ROUNDS)

    def start_action(self):
        new_screen = "round_setup" if wm.selected_mode is wm.ROUNDS else "training_setup"
        self.set_screen(new_screen)
        self.curr_image = None

class round_setup_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "round_setup"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        self.curr_image = None
        
        self.images = {
            "beginner": get_image(f"{cwd}/screens/4.png"),
            "intermediate": get_image(f"{cwd}/screens/5.png"),
            "hardcore": get_image(f"{cwd}/screens/6.png")
        }

        self.buttons = [
            Button(self.name, "beginner", 0, 49, 506, 121, self.beginner_action),
            Button(self.name, "intermediate", 0, 179, 506, 253, self.intermediate_action),
            Button(self.name, "hardcore", 0, 309, 506, 385, self.hardcore_action),
            Button(self.name, "home", 372, 404, 423, 460, self.home_action),
            Button(self.name, "beginner_go", 507, 49, 800, 121, self.go_action),
            Button(self.name, "intermediate_go", 507, 179, 800, 253, self.go_action),
            Button(self.name, "hardcore_go", 507, 309, 800, 385, self.go_action)
        ]

    def prepare(self):
        set_image(self.holder, self.images["beginner"])
        wm.set_round_difficulty(wm.BEGINNER)
	
    def run(self, press_event: tk.Event):
        # check whether buttons have been pressed
        if press_event is not None: 
            for button in self.buttons: button.check_if_pressed(press_x=press_event.x, press_y=press_event.y)

    def beginner_action(self):
        set_image(self.holder, self.images["beginner"]) if self.curr_image != "beginner" else 0
        self.curr_image = "training"
        wm.set_round_difficulty(wm.BEGINNER)

    def intermediate_action(self):
        set_image(self.holder, self.images["intermediate"]) if self.curr_image != "intermediate" else 0
        self.curr_image = "intermediate"
        wm.set_round_difficulty(wm.INTERMEDIATE)

    def hardcore_action(self):
        set_image(self.holder, self.images["hardcore"]) if self.curr_image != "hardcore" else 0
        self.curr_image = "hardcore"
        wm.set_round_difficulty(wm.HARDCORE)

    def home_action(self):
        self.set_screen("main")
        self.curr_image = None

    def go_action(self):
        self.set_screen("punches_setup")
        self.curr_image = None

class punches_setup_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "punches_setup"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function
        self.punches = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="#4c494b")

        self.curr_image = None
        self.entered_screen = False
        
        self.images = {
            "punches": get_image(f"{cwd}/screens/7.png")
        }

        self.buttons = [
            Button(self.name, "punches_go", 601, 71, 794, 183, self.go_action),
            Button(self.name, "add_time", 584, 289, 690, 424, self.add_time_action),
            Button(self.name, "remove_time", 113, 290, 214, 420, self.remove_time_action),
            Button(self.name, "home", 18, 403, 69, 457, self.home_action),
        ]

    def prepare(self):
        wm.reset_punches_cursor()

        # prepare punches value text
        self.punches.config(text=wm.get_punches_value())
        self.punches.place(relx=0.5, rely=0.75, anchor="center")
        set_image(self.holder, self.images["punches"])

    def run(self, press_event: tk.Event):
        # check whether buttons have been pressed
        if press_event is not None: 
            for button in self.buttons: button.check_if_pressed(press_x=press_event.x, press_y=press_event.y)

    def go_action(self):
        self.set_screen("workout_start")
        self.curr_image = None
        self.punches.place_forget()

    def add_time_action(self):
        wm.increment_punches()
        self.punches.config(text=wm.get_punches_value())
        self.punches.place(relx=0.5, rely=0.75, anchor="center")

    def remove_time_action(self):
        wm.decrement_punches()
        self.punches.config(text=wm.get_punches_value())
        self.punches.place(relx=0.5, rely=0.75, anchor="center")

    def home_action(self):
        self.curr_image = None
        self.punches.place_forget()
        self.set_screen("main")

class training_setup_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "training_setup"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        self.curr_image = None
        
        self.images = {
            "all": get_image(f"{cwd}/screens/12.png"),
            "hook": get_image(f"{cwd}/screens/13.png"),
            "straight": get_image(f"{cwd}/screens/14.png")
        }

        self.buttons = [
            Button(self.name, "training_go", 265, 357, 540, 480, self.go_action),
            Button(self.name, "right_option", 677, 198, 744, 284, self.right_option_action),
            Button(self.name, "left_option", 57, 198, 123, 284, self.left_option_action),
            Button(self.name, "home", 18, 403, 69, 457, self.home_action),
        ]

    def prepare(self):
        set_image(self.holder, self.images[wm.get_bag()])
        wm.bag_cursor = 0

    def run(self, press_event: tk.Event):
        # check whether buttons have been pressed
        if press_event is not None: 
            for button in self.buttons: button.check_if_pressed(press_x=press_event.x, press_y=press_event.y)

    def go_action(self):
        self.set_screen("punches_setup")
        self.curr_image = None

    def right_option_action(self):
        wm.increment_bag()
        set_image(self.holder, self.images[wm.get_bag()])

    def left_option_action(self):
        wm.decrement_bag()
        set_image(self.holder, self.images[wm.get_bag()])

    def home_action(self):
        self.set_screen("main")
        self.curr_image = None

class workout_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "workout"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        # screen variable values
        self.target = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="black")
        self.landed = tk.Label(self.holder, font=("Helvetica", 50, "bold"), anchor="center", fg="white", bg="#4c494b")
        self.taken = tk.Label(self.holder, font=("Helvetica", 50, "bold"), anchor="center", fg="white", bg="#4c494b")

        self.curr_image = None
        
        self.images = {
            "training": get_image(f"{cwd}/screens/8.png"),
            "beginner": get_image(f"{cwd}/screens/9.png"),
            "intermediate": get_image(f"{cwd}/screens/10.png"),
            "hardcore": get_image(f"{cwd}/screens/11.png")
        }

        self.buttons = [
            Button(self.name, "pause", 660, 45, 767, 157, self.pause_action),
            Button(self.name, "play", 660, 189, 767, 296, self.play_action),
            Button(self.name, "home", 660, 327, 767, 436, self.home_action),
        ]

    def prepare(self):
        set_image(self.holder, self.images[wm.get_workout()])

        # start workout
        wm.init_workout()

        self.target.config(text=wm.get_punches_value())
        self.target.place(relx=0.5, rely=0.68, anchor="center")

        self.landed.config(text=wm.get_landed())
        self.landed.place(relx=0.105, rely=0.315, anchor="center")

        self.taken.config(text=wm.get_taken())
        self.taken.place(relx=0.105, rely=0.79, anchor="center")

    def run(self, press_event: tk.Event):
        # check whether buttons have been pressed
        if press_event is not None: 
            for button in self.buttons: button.check_if_pressed(press_x=press_event.x, press_y=press_event.y)

        # display target punches
        self.target.config(text=wm.get_punches_value())
        self.target.place(relx=0.5, rely=0.68, anchor="center") if self.curr_image else 0
        
        # update landed and taken punches
        self.landed.config(text=wm.get_landed())
        self.taken.config(text=wm.get_taken())

        # end workout if total sent punches is equal to the target punches
        if (wm.get_landed() + wm.get_taken()) >= wm.get_punches_value():
            self.home_action()

    def pause_action(self):
        # pause workout
        wm.pause_workout()

    def play_action(self):
        # resume workout if paused
        wm.resume_workout()

    def home_action(self):
        self.target.place_forget()
        self.taken.place_forget()
        self.landed.place_forget()

        self.set_screen("workout_end")
        self.curr_image = None
        wm.end_workout()

class workout_start_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "workout_start"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        # screen variable values
        self.target = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="black")
        self.time = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="black")
        self.display_start_time = 0
        self.display_time = 60 # number of seconds to show the screen
        self.display_elapsed_time = 0
        self.prev_time = 0

        self.curr_image = None
        
        self.images = {
            "workout_start_screen": get_image(f"{cwd}/screens/16.png")
        }

        self.buttons = [] # no buttons in this screen

    def prepare(self):
        # initialize screen variables
        self.display_elapsed_time = 0
        self.display_start_time = time()
        self.prev_time = self.display_start_time

        set_image(self.holder, self.images["workout_start_screen"])

        self.target.config(text=wm.get_punches_value())
        self.target.place(relx=0.29, rely=0.56, anchor="center")

        self.time.config(text=self.display_time)
        self.time.place(relx=0.72, rely=0.56, anchor="center")

    def run(self, press_event: tk.Event):
        _ = press_event

        # exit the screen after the display time has passed
        if time() - self.display_start_time >= self.display_time:
            self.curr_image = None
            self.target.place_forget()
            self.time.place_forget()
            self.set_screen("workout")

        # update the countdown time
        if time() - self.prev_time >= 1:
            self.display_elapsed_time += 1
            self.prev_time = time()
            time_left = self.display_time - self.display_elapsed_time
            self.time.config(text=time_left)
            self.time.place(relx=0.72, rely=0.56, anchor="center")

class workout_end_screen:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label, set_screen_function):
        global cwd
        self.name = "workout_end"
        self.root = root
        self.holder = screen_holder
        self.set_screen = set_screen_function

        # screen variable values
        self.target = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="black")
        self.landed = tk.Label(self.holder, font=("Helvetica", 80, "bold"), anchor="center", fg="white", bg="black")
        self.display_start_time = 0
        self.display_time = 10 # number of seconds to show the screen

        self.curr_image = None
        
        self.images = {
            "workout_end_screen": get_image(f"{cwd}/screens/17.png")
        }

        self.buttons = [] # no buttons in this screen

    def prepare(self):
        # initialize screen variables
        self.display_start_time = time()

        set_image(self.holder, self.images["workout_end_screen"])

        self.target.config(text=wm.get_punches_value())
        self.target.place(relx=0.29, rely=0.56, anchor="center")

        self.landed.config(text=wm.get_landed())
        self.landed.place(relx=0.72, rely=0.56, anchor="center")

    def run(self, press_event: tk.Event):
        _ = press_event

        # exit the screen after the display time has passed
        if time() - self.display_start_time >= self.display_time:
            wm.reset_variables()
            self.curr_image = None
            self.target.place_forget()
            self.landed.place_forget()
            self.set_screen("main")

class screen_manager:
    def __init__(self, root: tk.Tk, screen_holder: tk.Label):
        self.root = root
        self.holder = screen_holder

        self.screens = {
            "main": main_screen(self.root, self.holder, self.set_screen),
            "round_setup": round_setup_screen(self.root, self.holder, self.set_screen),
            "punches_setup": punches_setup_screen(self.root, self.holder, self.set_screen),
            "training_setup": training_setup_screen(self.root, self.holder, self.set_screen),
            "workout": workout_screen(self.root, self.holder, self.set_screen),
            "workout_start": workout_start_screen(self.root, self.holder, self.set_screen),
            "workout_end": workout_end_screen(self.root, self.holder, self.set_screen)
        }
        self.curr_screen = "main"
        self.press_event = None

    def handle_screens(self):
        self.screens[self.curr_screen].run(self.press_event)

        self.root.after(100, self.handle_screens)

    def handle_press(self, event: tk.Event):
        self.press_event = event
        self.root.after(101, self.forget_press)
        print(event.x, event.y, sep=",")

    def forget_press(self):
        self.press_event = None

    def set_screen(self, new_screen):
        self.curr_screen = new_screen
        self.screens[new_screen].prepare()
        self.press_event = None
    
