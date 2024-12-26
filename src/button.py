import RPi.GPIO as GPIO
import time
import threading


class Button:
    # Pin configuration.
    BUTTON_PIN = 5

    def __init__(self):
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.BUTTON_PIN, GPIO.RISING, callback=self.on_button_press, bouncetime=200)

        self.callbacks = []
        
    def add_callback(self, callback):
        self.callbacks.append(callback)

    def on_button_press(self, event):
        print("Button press detected")
        for callback in self.callbacks:
            threading.Thread(target=callback, args=(event,)).start()
