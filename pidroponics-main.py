import RPi.GPIO as GPIO 
import time 
import picamera 
import os 
from datetime import datetime
import Adafruit_DHT as dht

print("Starting pidroponics-main")
susanEnablePinNum = 17
susanDirPinNum = 2
susanStepPinNum = 4
susanPwmHz = 10
susanDutyCycle = 50
susanStepTime = 0.15
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

sensorValueStorage = 240

tempSensePinNum = 5
tempReadings = []
humidityReadings = []

lightTogglePin = 6
GPIO.setup(lightTogglePin, 0)
GPIO.output(lightTogglePin, 0)
lightToggled = False

waterTogglePin = 13
GPIO.setup(waterTogglePin, 0)
GPIO.output(waterTogglePin, 0)
waterToggled = False

heatTogglePin = 13
GPIO.setup(heatTogglePin, 0)
GPIO.output(heatTogglePin, 0)
heatToggled = False


def main():
	setupCam()
	while(not capturePlants()):
		pass
	while(not collectData()):
		pass
	toggleLight()
	time.sleep(5)
	toggleLight()
	time.sleep(5)
	toggleWater()
	time.sleep(5)
	toggleWater()
	time.sleep(5)
	toggleHeat()
	time.sleep(5)
	toggleHear()
	time.sleep(5)
	print("Begining Life Sequence")
	while(True):
	        currentHour = datetime.now().hour
		currentMinute = datetime.now().minute
		if(currentHour % 12 == 0):
			while(not capturePlant()):
				pass
		if(currentMinute == 0):
			while(not collectData()):
			pass
		if(currentHour == 7 || currentHour == 23):
			toggleLight()
		if(currentMinute % 5 == 0)
			toggleWater()
			time.sleep(120)
			toggleWater()
		if(tempReadings[-1] <= 16 || tempReadings[-1] >= 27):	
			toggleHeat()

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
	return True	
		
def collectData():
	print("Taking measurement readings at " + str(datetime.now()))
	print("Taking Temp/Humidity Readings")
	currentHumidity, currentTemp = dht.read_retry(dht.DHT22, tempSensePinNum)
	
	tempReadings.append(currentTemp)
	humidityReadings.append(currentHumidity)

	if(len(tempReadings) >= sensorValueStorage):
		tempReadings.pop(0)
	if(len(humidityReadings) >= sensorValueStorage):
		humidityReadings.pop(0)
	
	return True

def toggleLight():
	if(lightToggled):
		print("Turning light off")
		GPIO.output(lightTogglePin, 0)
		lightToggled = False
	else:
		print("Turning light on")
		GPIO.output(lightTogglePin, 1)
		lightToggled = True

def toggleHeat():
        if(heatToggled):
                print("Turning heat off")
                GPIO.output(heatTogglePin, 0)
                heatToggled = False
        else:
                print("Turning heat on")
                GPIO.output(heatTogglePin, 1)
                heatToggled = True

def toggleWater():
	if(waterToggled):
		print("Turning water off")
		GPIO.output(waterTogglePin, 0)
		waterToggled = False
	else:
		print("Turning water on")
		GPIO.output(waterTogglePin, 1)
		waterToggled = True

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
