import RPi.GPIO as GPIO
import time
import picamera
import os
from datetime import datetime

print("Starting pidroponics-main")
susanEnablePinNum = 17
susanDirPinNum = 2
susanStepPinNum = 4
susanPwmHz = 10
susanDutyCycle = 50
susanStepTime = 1.388888
susanCamDelay = .2
susanEnableDelay = .5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(susanEnablePinNum, GPIO.OUT)
GPIO.setup(susanDirPinNum, GPIO.OUT)
GPIO.setup(susanStepPinNum, GPIO.OUT)

GPIO.output(susanEnablePinNum, 1)
GPIO.output(susanDirPinNum, 0)
GPIO.output(susanStepPinNum, 0)

susanStepPin = GPIO.PWM(susanStepPinNum, susanPwmHz)

picam = 0

def main():
	setupCam()
	capturePlant()

def capturePlant():
	print("Taking Capture at " + str(datetime.now()))
	currentYear = datetime.now().year
	currentMonth = datetime.now().month
	currentDay = datetime.now().day
	currentHour = datetime.now().hour
	currentMinute = datetime.now().minute
	currentDir = str(currentYear) + "_" + str(currentMonth) + "_" + str(currentDay) + "_" + str(currentHour) + "_" + str(currentMinute)
	print("Saving To: " + currentDir)
	if not os.path.exists(currentDir):
		os.makedirs(currentDir)
	for picture in range(0, 36, 1):
		enableSusan(True)
		susanStepPin.start(susanDutyCycle)
		time.sleep(susanStepTime)
		enableSusan(False)
		print("Taking Picture " + str(picture))
		picam.capture(currentDir + "/" + str(picture) + ".jpg")
		time.sleep(susanCamDelay)
	enableSusan(False)
		
def collectData():
	return

def toggleLight():
	return

def toggleHeat():
	return

def toggleWater():
	return

def setupCam():
	print("Setting up PiCam")
	global picam
	picam = picamera.PiCamera()
	picam.resolution = (1920, 1080)

def enableSusan(enable):
	if(enable):
		print("Enabling Susan")
		GPIO.output(susanEnablePinNum, 0)
	else:
		print("Disabling Susan")
		GPIO.output(susanEnablePinNum, 1)
	time.sleep(susanEnableDelay)
	
main()
