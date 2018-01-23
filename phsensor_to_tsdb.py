#!/usr/bin/python

import serial
import sys
import time
import string 
from serial import SerialException
import json
import requests

def getLocalURL():
    url = "http://125.7.128.42:4242/api/put?details"
    return url

def read_line():
	"""
	taken from the ftdi library and modified to 
	use the ezo line separator "\r"
	"""
	lsl = len('\r')
	line_buffer = []
	while True:
		next_char = ser.read(1)
		if next_char == '':
			break
		line_buffer.append(next_char)
		if (len(line_buffer) >= lsl and
				line_buffer[-lsl:] == list('\r')):
			break
	return ''.join(line_buffer)
	
def read_lines():
	"""
	also taken from ftdi lib to work with modified readline function
	"""
	lines = []
	try:
		while True:
			line = read_line()
			if not line:
				break
				ser.flush_input()
			lines.append(line)
		return lines
	
	except SerialException as e:
		print "Error, ", e
		return None	

def send_cmd(cmd):
	"""
	Send command to the Atlas Sensor.
	Before sending, add Carriage Return at the end of the command.
	:param cmd:
	:return:
	"""
	buf = cmd + "\r"     	# add carriage return
	try:
		ser.write(buf)
		return True
	except SerialException as e:
		print "Error, ", e
		return None
			
if __name__ == "__main__":
	
	usbport = '/dev/ttyAMA0' # change to match your pi's setup 

	print "Opening serial port now..."

	try:
		ser = serial.Serial(usbport, 9600, timeout=0)
	except serial.SerialException as e:
		print "Error, ", e
		sys.exit(0)

	while True:
                try:
                    while True:
                        send_cmd("R")
                        lines = read_lines()
        
#			for i in range(len(lines)):
			# print lines[i]
#			if lines[i][0] != '*':
#			print "Response: " , lines[i]
                        
                        data = {
                            "metric": "rc01.pH.H",
                            "timestamp": time.time(),
                            "value": lines[0],
                            "tags":{
                                "id" : 500,
                                "sensor" : "pH",
                            "floor_room": "astabio",
                            "building": "jbnu",
                            "owner": "thingspire",
                            "country": "Korea"
                            }
                        }
                        #print data
                        #print "first line ph value: " , lines[0]
                        url = getLocalURL()
                        ret = requests.post(url, data=json.dumps(data))
                        print data 
			time.sleep(5)

		except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
			print("Continuous polling stopped")
	
		# if not a special keyword, pass commands straight to board
#		else:
#			if len(input_val) == 0:
#				lines = read_lines()
#				for i in range(len(lines)):
#					print lines[i]
#			else:
#				send_cmd(input_val)
#				time.sleep(1.3)
#				lines = read_lines()
#				for i in range(len(lines)):
#					print lines[i]
