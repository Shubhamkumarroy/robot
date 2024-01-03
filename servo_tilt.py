import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
tiltPin = 3
GPIO.setup(tiltPin, GPIO.OUT)
pwm = GPIO.PWM(tiltPin, 50)
pwm.start(0)

try:
	while True:
		angle = float(input("Enter angle: "))
		angle += 90
		dutyCycle = angle/18. + 2.
		pwm.ChangeDutyCycle(dutyCycle)
		sleep(.5)
		pwm.ChangeDutyCycle(0)
except:
	GPIO.cleanup()
	print("GPIO is good to go...")
