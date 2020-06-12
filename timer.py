#!/usr/bin/python3

import os
import time
import socket
import logging

# next_time = time.time() + 3600
# print('Will start at')
# print(next_time)
# while time.time()<next_time:
# 	time.sleep(10)
# 	print('curent: ')
# 	print(time.time())
# os.system("sudo reboot")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def print_log(message):
	logger.info(message)
	print(message)

# define file handler and set formatter
file_handler = logging.FileHandler('/home/pi/Desktop/Lab_Monitor/watchdog.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, WatchDog!"

sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(2)

# first_time_startup = True

# if first_time_startup:
# 	watchdog_tick = time.time() + 900 # 45'
# else:
# 	watchdog_tick = time.time() + 300 # 15'
watchdog_tick = time.time() + 900 # 45'
print_log("Next kick is %d" % watchdog_tick)

while True:
	try:
		print_log("WatchDog check: %d" % time.time())
		if time.time() > watchdog_tick:
			print_log("WatchDog kick")
			os.system("sudo reboot")

		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print_log("received message: %s"% data.decode("utf-8"))
		if data.decode("utf-8") == MESSAGE:
			print_log("WatchDog update")

			# first_time_startup = False
			# if first_time_startup:
			# 	watchdog_tick = time.time() + 900 # 45'
			# else:
			# 	watchdog_tick = time.time() + 300 # 15'

			watchdog_tick = time.time() + 300 # 15'
			print_log("Next kick is %d" % watchdog_tick)
		time.sleep(2)
	except Exception as err:
		print_log(err)