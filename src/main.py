import threading
import time
import RPi.GPIO as GPIO
from camera_display import CameraDisplay
from button import Button
from buzzer import Buzzer
from hcsr04 import Hcsr
from pir import Pir
from led import Led
from live_feed import app  # Import the Flask app from live_feed.py

# Set the GPIO mode to BCM.
GPIO.setmode(GPIO.BCM)


def on_motion_detected():
    hcsr = Hcsr()    
    distance = hcsr.get_distance_cm()
   
    if distance <= 30:
        print(f"Someone is here! And less than 30cm away ({distance}cm)")
   
        led = Led()
        led.turn_on_for_n_secs(60)

        camera_display = CameraDisplay()
        camera_display.capture_and_display_n_secs(60)


def run_flask_app():
    """Function to run Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=5863, threaded=True)


def main():
    # Initialize the sensors
    camera_display = CameraDisplay()
    button = Button()
    buzzer = Buzzer()
    led = Led()
    pir = Pir()

    # On button presses, do the following events:
    button.add_callback(lambda _: buzzer.buzz_in_ring_pattern())
    button.add_callback(lambda _: camera_display.capture_and_display_n_secs(60))
    button.add_callback(lambda _: led.turn_on_for_n_secs(60))
    
    # On movement detections, do the following events:
    pir.add_callback(lambda _: on_motion_detected())

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # Daemonize the thread to ensure it exits when the main program exits
    flask_thread.start()

    # Main loop. Keep the program running while the Flask app handles HTTP requests.
    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
