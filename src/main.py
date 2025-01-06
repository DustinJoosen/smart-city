from camera_display import CameraDisplay
from button import Button
from buzzer import Buzzer
from hcsr04 import Hcsr
from pir import Pir
from led import Led
import RPi.GPIO as GPIO


# Set the GPIO mode to BCM.
GPIO.setmode(GPIO.BCM)


def on_motion_detected():
    hcsr = Hcsr()    
    distance = hcsr.get_distance_cm()
   
    if distance <= 30:
        print(f"Someone is here! And less then 30cm away ({distance}cm)")
   
        led = Led()
        led.turn_on_for_n_secs(5)

        camera_display = CameraDisplay()
        camera_display.capture_and_display_n_secs(5)


def main():
    # Initialize the sensors
    camera_display = CameraDisplay()
    button = Button()
    buzzer = Buzzer()
    led = Led()
    pir = Pir()

    # On button presses, do the following events:
    button.add_callback(lambda _: buzzer.buzz_in_ring_pattern())
    button.add_callback(lambda _: camera_display.capture_and_display_n_secs(5))
    button.add_callback(lambda _: led.turn_on_for_n_secs(5))
    
    # On movement detections, do the following events:
    pir.add_callback(lambda _: on_motion_detected())

    # Main loop. Keep the program running.
    while True:
          pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
