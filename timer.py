#!/usr/bin/python3

import os
import time
import socket

def print_log(message):
    print(message)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, WatchDog!"

sock = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(2)

watchdog_tick = time.time() + 60 # 45'
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
            watchdog_tick = time.time() + 300 # 15'
            print_log("Next kick is %d" % watchdog_tick)
        time.sleep(2)
    except Exception as err:
        print_log(err)
