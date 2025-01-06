import RPi.GPIO as GPIO
import time
import threading
from timeout import Timeout

class Led:
    LED_PIN = 6

    def __init__(self):
        GPIO.setup(self.LED_PIN, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        
    def turn_on_for_n_secs(self, n):
        self.turn_on()
        Timeout(self.turn_off, n)

        
