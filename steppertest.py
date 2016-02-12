import time
import RPi.GPIO as GPIO

doDrive = False
enablePinNum = 17
dirPinNum = 2
stepPinNum = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(dirPinNum, GPIO.OUT)
GPIO.setup(stepPinNum, GPIO.OUT)
GPIO.setup(enablePinNum, GPIO.OUT)

GPIO.output(dirPinNum, 1)
GPIO.output(stepPinNum, 0)
GPIO.output(enablePinNum, 0)

stepPin = GPIO.PWM(stepPinNum, 100)
stepPin.start(0)

while 1:
	GPIO.output(enablePinNum, 1)
	for i in range(0, 2):
		GPIO.output(dirPinNum, 1)
		stepPin.ChangeDutyCycle(10)
		time.sleep(1)
		GPIO.output(dirPinNum, 0)
		time.sleep(1)	
	GPIO.output(enablePinNum, 0)
	time.sleep(5)