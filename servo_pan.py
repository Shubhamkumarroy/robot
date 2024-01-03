import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
panPin = 4
GPIO.setup(panPin, GPIO.OUT)
pwm = GPIO.PWM(panPin, 50)
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
