"""
	Manages serial communication between the Raspberry Pi and the "Master" Trinket
	Outgoing Message Format:
		- "M1C2C3C4CTVDW"
		- M = starting byte
		- C = color to set pad (1, 2, 3, and 4) LED (R, G, or B for black)
		- T = byte preceeding time representation
		- V = Time byte ranging from 97 - 122 ASCII, lowercase alphabet, 26 letters, represents times between 0 and 26 seconds
		- D = byte preceeding decimal portion of time representation
		- W = ranges from 97 to 107 ASCII, represents single digit decimal between 0 and 9
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
		
		# Start the message monitor supervisor
		threading.Thread(target=self.monitor_supervisor).start()
		
	def process_incoming_message(self, msg):
		translator = {"H":1, "N":0}
		self.hit_status = [translator[msg[1+msg.index(str(val))]] for val in range(1, 5)]

	def monitor_supervisor(self):
		while True:
			self.monitor = threading.Thread(target=self.message_monitoring)
			self.monitor.start()
			self.monitor.join()  # Wait for the thread to finish
			print("Message Monitoring Thread exited, restarting ...")
			sleep(0.1)  # restarting
			
	def message_monitoring(self):
		try:
			while not self.fire_manager:
				# wait for full main trinket message
				if self.ser.in_waiting == 9:
					if self.ser.read(1) == b'M':
						# raw = self.ser.read(8) # read the next 8 bytes
						# print(f"Raw bytes: {raw}")  # print bytes
				
						# msg = ""
						# for m in raw:
						# 	try:
						# 		msg += raw[].decode()
						# 	except UnicodeDecodeError:
						# 		print("Decode Error...")
						# 		msg += 'N'
						msg = ""
						for _ in range(8):
							try:
								raw = self.ser.read(1)
								if raw in [b"\0xff", b"\x00"]:
									msg += "N"
								else:
									msg += raw.decode()
							except Exception as e:
								print(f"Decode error: {e}, assigning default value")
								msg += "N"
			
						if len(msg) == 8 and '1' in msg and '2' in msg and '3' in msg and '4' in msg:
							self.process_incoming_message(msg)
							print(self.hit_status)
							print(f"Decoded message: {msg}")
						else:
							self.hit_status = [0, 0, 0, 0]
		except Exception as e:
			print(f"Error in thread: {e}")
		
	def set_pads(self, pad1, pad2, pad3, pad4, report_by_time_whole, report_by_time_deci):
		message = f"M1{pad1}2{pad2}3{pad3}4{pad4}T{report_by_time_whole}D{report_by_time_deci}"
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
		
	
		
