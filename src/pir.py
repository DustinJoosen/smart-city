import RPi.GPIO as GPIO
import time
import threading


class Pir:
    # Pin configuration.
    PIR_PIN = 4

    def __init__(self):
        GPIO.setup(self.PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.PIR_PIN, GPIO.RISING, callback=self.on_motion, bouncetime=10)

        self.callbacks = []
        
    def add_callback(self, callback):
        self.callbacks.append(callback)

    def on_motion(self, event):
        print("Motion detected")

        for callback in self.callbacks:
             threading.Thread(target=callback, args=(event,)).start()
