
from time import time

class Workout_manager:
    def __init__(self):
        # workout modes
        self.TRAINING = "training"
        self.ROUNDS = "rounds"
        self.selected_mode = self.TRAINING

        # training mode bag selection
        self.ALL = "all"
        self.HOOK = "hook"
        self.STRAIGHT = "straight"
        self.bags = [self.ALL, self.HOOK, self.STRAIGHT]
        self.bag_cursor = 0

        # round mode difficulty selection
        self.BEGINNER = "beginner"
        self.INTERMEDIATE = "intermediate"
        self.HARDCORE = "hardcore"
        self.selected_difficulty = self.BEGINNER

        # number of punches for each mode
        self.training_punches = list(range(10, 101, 10))
        self.rounds_punches = list(range(25, 201, 25))
        self.punches_cursor = 0

        # workout variables
        self.time_left = None
        self.init_time = None
        self.paused = True
        self.punches_landed = 0
        self.punches_taken = 0

    def set_mode(self, mode_name):
        self.selected_mode = mode_name

    def increment_bag(self):
        self.bag_cursor += 1 if self.bag_cursor + 1 < 3 else 0

    def decrement_bag(self):
        self.bag_cursor -= 1 if self.bag_cursor - 1 >= 0 else 0

    def get_bag(self):
        return self.bags[self.bag_cursor]

    def set_round_difficulty(self, level):
        self.selected_difficulty = level

    def reset_punches_cursor(self):
        self.punches_cursor = 0

    def increment_punches(self):
        if self.selected_mode is self.TRAINING:
            self.punches_cursor += 1 if self.punches_cursor + 1 < len(self.training_punches) else 0
        elif self.selected_mode is self.ROUNDS:
            self.punches_cursor += 1 if self.punches_cursor + 1 < len(self.rounds_punches) else 0

    def decrement_punches(self):
        if self.selected_mode is self.TRAINING:
            self.punches_cursor -= 1 if self.punches_cursor - 1 >= 0 else 0
        elif self.selected_mode is self.ROUNDS:
            self.punches_cursor -= 1 if self.punches_cursor - 1 >= 0 else 0

    def get_punches_value(self):
        return self.training_punches[self.punches_cursor] if self.selected_mode is self.TRAINING else self.rounds_punches[self.punches_cursor]

    def get_workout(self):
        if self.selected_mode is self.TRAINING:
            return self.TRAINING
        elif self.selected_mode is self.ROUNDS:
            return self.selected_difficulty
        
    def init_workout(self):
        self.time_left = self.get_punches_value() * 4

    def pause_workout(self):
        self.paused = True
        
    def resume_workout(self):
        self.paused = False
        self.init_time = int(time())

    def end_workout(self):
        self.paused = True

    def get_time_left(self):
        if not self.paused and (time() - self.init_time) >= 1:
            self.time_left -= 1 if self.time_left - 1 >= 0 else 0
            self.init_time = time()
        return self.time_left

    def get_landed(self):
        return self.punches_landed
    
    def get_taken(self):
        return self.punches_taken
        
    
            



