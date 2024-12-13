"""
	Manages serial communication between the Raspberry Pi and the "Master" Trinket
	Outgoing Message Format:
		- "M1C2C3C4C"
		- M = starting byte
		- C = color to set pad (1, 2, 3, and 4) LED (R, G, or B for black)
	Incoming Message Format:
		- "M1S2S3S4S"
		- M = starting byte
		- S = pad (1, 2, 3, and 4) hit status (H = hit, N = not hit)
"""

import threading

from serial import Serial
from time import sleep

class Comms_manager:
	def __init__(self, port = "/dev/ttyUSB0", baudrate = 9600):
		self.ser = Serial(port, baudrate)
		 
		self.GREEN = 'G'
		self.RED = 'R'
		self.BLACK = 'B'
		
		self.hit_status = [0, 0, 0, 0]
		
		self.fire_manager = False
		
		# open serial port if not already open
		if not self.ser.is_open:
			try:
				self.ser.open()
			except Exception as e:
				print(e)
		
		
		# message monitoring thread
		self.monitor = threading.Thread(target=self.message_monitoring)
		self.monitor.start()
		
	def process_incoming_message(self, msg):
		translator = {"H":1, "N":0}
		self.hit_status = [translator[msg[1+msg.index(str(val))]] for val in range(1, 5)]
			
	def message_monitoring(self):
		try:
			while not self.fire_manager:
				# find starting byte
				if self.ser.read().decode() == "M":
					sleep(0.1)
					msg = self.ser.read(8).decode()
					self.process_incoming_message(msg) if len(msg) == 8 else 0
					print(self.hit_status)
		except Exception as e:
			print(f"Error in thread: {e}")
		
	def set_pads(self, pad1, pad2, pad3, pad4):
		message = f"M1{pad1}2{pad2}3{pad3}4{pad4}"
		if self.ser.write(bytes(message, "utf-8")):
			print(f"{message} written successfully")
			return 1
		else: 
			print("Could not write message to Trinket")
			return 0
		
	def get_hits(self):
		return self.hit_results
		
	def close(self):
		self.fire_manager = True
		self.ser.close()
		
	
		
