from camera.camera_display import CameraDisplay
from button.button import Button
from buzzer.buzzer import Buzzer
from hcsr04.hcsr04 import Hcsr
import RPi.GPIO as GPIO

# Set the GPIO mode to BCM.
GPIO.setmode(GPIO.BCM)


def main():
    # Initialize the sensors
    camera_display = CameraDisplay()
    button = Button()
    buzzer = Buzzer()
    hcsr = Hcsr()

    # On button presses, do the following events:
    button.add_callback(lambda _: buzzer.buzz_in_ring_pattern()) 
    button.add_callback(lambda _: camera_display.capture_and_display_n_secs(30))

    # Main loop. Keep the program running.
    while True:
        distance = hcsr.get_distance_cm()
        print(f"Current distance measured from hcsr: {distance}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
