import RPi.GPIO as GPIO
import time

pwmPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pwmPin, GPIO.OUT)

led = GPIO.PWM(pwmPin, 100)
led.start(15)
while 1:
	led.ChangeDutyCycle(15)
"""
while(True):
	 for dc in range(0, 101, 5):
		led.ChangeDutyCycle(dc)
		print(dc)
        	time.sleep(0.5)
         for dc in range(100, -1, -5):
                led.ChangeDutyCycle(dc)
		print(dc)
                time.sleep(0.5)
"""
