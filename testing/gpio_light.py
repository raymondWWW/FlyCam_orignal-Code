# Testing GPIO with MOSFET and Ring LED

import RPi.GPIO as GPIO
from time import sleep

def main():
	print("Main")
	
	# Use BCM or Broadcom numbering system
	# Here, 3 represents row 2, column 3 of GPIO pins (start at 1, not 0).
	SIG_PIN = 3
	
	# Setup GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SIG_PIN, GPIO.OUT)
	
	print("Turning on LED")
	
	# Method 1: Turn on LED, no PWM
	# Turn on LED
	GPIO.output(SIG_PIN, True)
	sleep(4)
	
	# Turn off LED
	GPIO.output(SIG_PIN, False)
	
	# Method 2 of Turning LED on with PWM
	# Alternative way using PWM and frequency (will strobe LED)
	# FREQ = 100
	# print("Starting LED...")
	# p = GPIO.PWM(SIG_PIN, FREQ)
	# p.start(FREQ)
	# sleep(5)
	# p.stop()
	
	# Clean up GPIO
	GPIO.cleanup()
	
	print("Stopping LED...")
	
	pass

if __name__ == "__main__":
	main()
