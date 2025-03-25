import threading
import traceback

from time import time, sleep
from comms import Comms_manager
from random import randint

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
		self.started = False
		self.time_left = None
		self.init_time = None
		self.paused = True
		self.punches_landed = 0
		self.punches_taken = 0
		self.punches_reached = False
		self.combo = [0, 0, 0, 0] 		# indicated bags/pads that need to be hit (0 = no, 1 = yes)
		self.time_till_next = 0 		# time to give user to perform a sit-up/ time between rounds 
		self.time_till_results = 0

		self.workout_thread = threading.Thread(target = self.run_workout)
		self.workout_thread.start()

		# trinket communications manager
		self.cm = Comms_manager()

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
		self.time_left = self.get_punches_value()

	def pause_workout(self):
		self.paused = True
		# turn off pads
		pad_info = [self.cm.BLACK]*4
		pad_info.append('a')
		self.cm.set_pads(*pad_info)
        
	def resume_workout(self):
		self.paused = False
		self.init_time = int(time())

	def end_workout(self):
		self.paused = True
		# reset punches landed and taken
		self.punches_reached = False
		# turn off pads
		pad_info = [self.cm.BLACK]*4
		pad_info.append('a')
		pad_info.append('a')
		self.cm.set_pads(*pad_info)

	def reset_variables(self):
		self.punches_landed = 0
		self.punches_taken = 0

	def get_time_left(self):
		if not self.paused and (time() - self.init_time) >= 1:
			self.time_left -= 1 if self.time_left - 1 >= 0 else 0
			self.init_time = time()
		return self.time_left if not self.punches_reached else 0
        
	def get_landed(self):
		return self.punches_landed
    
	def get_taken(self):
		return self.punches_taken
		
	def run_workout(self):
		try:
			while True:
				# send punches every 4 seconds if the workout has been started
				if not self.paused and not self.punches_reached:
					self.send_punch()
					
					# pause before polling results
					sleep(self.time_till_results + 0.5)
					self.check_punch_results()

					# pause before next round of punches
					sleep(self.time_till_next)
				
		except Exception as e:
			print(f"Error in workout thread: {e}")
			traceback.print_exc()
			self.cm.fire_manager = True
			self.cm.close()
			
	def check_punch_results(self):
		if not self.paused:
			self.punches_landed += sum(self.cm.hit_status[0:4])
			self.punches_taken += abs(sum(self.combo[0:4]) - sum(self.cm.hit_status[0:4]))
			self.punches_reached = True if (self.punches_landed + self.punches_taken) >= self.get_punches_value() else False
        
	def send_punch(self):
		self.combo = [0, 0, 0, 0]

		# determine what pads to send punches
		if self.selected_mode is self.TRAINING:
			target_bag = 0
			self.time_till_next = 3
			
			if self.get_bag() == self.ALL:
				target_bag = randint(0, 3)
			elif self.get_bag() == self.HOOK:
				target_bag = [0, 3][randint(0, 1)]
			elif self.get_bag() == self.STRAIGHT:
				target_bag = [1, 2][randint(0, 1)]

			self.combo[target_bag] = 1
			# calculate how much time the PI should wait until polling for results
			self.time_till_results = 4

		elif self.selected_mode is self.ROUNDS:
			target_bags = [randint(0, 3) * 1000 for _ in range(20)] # create list of 20 random numbers within range of bag numbers
			target_bags = set(target_bags) # remove duplicates
			target_bags = [bag//1000 for bag in target_bags] # remove 1000 that allowed the set to remain unordered

			# get number of punches user selected
			selected_punches = self.training_punches[self.punches_cursor] if self.selected_mode is self.TRAINING else self.rounds_punches[self.punches_cursor]

			# determine number of punches user has to hit
			if selected_punches >= 75:
				self.combo = [1] * 4
			elif selected_punches >= 50:
				# select first three random bags
				self.combo[target_bags[0]] = 1
				self.combo[target_bags[1]] = 1
				self.combo[target_bags[2]] = 1
			else:
				# select the first two random bags
				self.combo[target_bags[0]] = 1
				self.combo[target_bags[1]] = 1
			
			if self.selected_difficulty == self.BEGINNER:
				self.time_till_next = 3
				# calculate how much time the PI should wait until polling for results
				self.time_till_results = 3.5
			elif self.selected_difficulty == self.INTERMEDIATE:
				self.time_till_next = 2
				# calculate how much time the PI should wait until polling for results
				self.time_till_results = 2.5
			elif self.selected_difficulty == self.HARDCORE:
				self.time_till_next = 2
				# calculate how much time the PI should wait until polling for results
				self.time_till_results = 2
			
		# set and send the message
		lookup = {1: self.cm.GREEN, 0: self.cm.BLACK}

		whole_ascii = None
		deci_ascii = None

		# convert time to ASCII value that represents the lowercase alphabets
		if type(self.time_till_results) is float:
			whole_ascii = chr(int(self.time_till_results) + 97) if 26 >= int(self.time_till_results) >= 0 else chr(97)
			decimal_as_whole = int((self.time_till_results - int(self.time_till_results))*10)
			deci_ascii = chr(decimal_as_whole + 97) if 9 >= decimal_as_whole >= 0 else chr(97)
		else:
			whole_ascii = chr(self.time_till_results + 97) if 26 >= self.time_till_results >= 0 else chr(97)
			deci_ascii = chr(97)
		
		pad_info = [lookup[val] for val in self.combo]
		pad_info.append(whole_ascii)
		pad_info.append(deci_ascii)
		self.cm.set_pads(*pad_info)
		
        
    
            
