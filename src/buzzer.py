import RPi.GPIO as GPIO
from notification import Notification
import time

notif = Notification()

# Adding notifications (the current time will be logged automatically)

class Buzzer:
    # Pin configuration.
    BUZZER_PIN = 22

    def __init__(self):            
        # Set GPIO22 as an output pin.
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)

    def buzz(self, time_in_ms):
        # Make the buzzer sound for n second.
        GPIO.output(self.BUZZER_PIN, GPIO.HIGH)

        time.sleep(time_in_ms)

        # Stop the buzzer
        GPIO.output(self.BUZZER_PIN, GPIO.LOW)

    def buzz_in_ring_pattern(self):
        notif.add_notification()
        print('buzzz')

        # Send a GET request to the add_notification 
        self.buzz(0.3)
        time.sleep(0.2)
        self.buzz(0.6)
        