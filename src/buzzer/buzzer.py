import RPi.GPIO as GPIO
import time


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
        self.buzz(0.3)
        time.sleep(0.2)
        self.buzz(0.6)
        