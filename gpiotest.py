import RPi.GPIO as GPIO
import time
print("Import Successful")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)

while(True):
	GPIO.output(4, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(4, GPIO.LOW)
	time.sleep(1)
