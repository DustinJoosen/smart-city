import RPi.GPIO as GPIO
import time

HCSR04_OUT = 17
HCSR04_IN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(HCSR04_OUT, GPIO.OUT)
GPIO.setup(HCSR04_IN, GPIO.IN)

def get_distance():    
    GPIO.output(HCSR04_OUT, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(HCSR04_OUT, GPIO.LOW)

    while GPIO.input(HCSR04_IN) == GPIO.LOW:
        start = time.time()
        print("s")
        
    while GPIO.input(HCSR04_IN) == GPIO.HIGH:
        end = time.time()
        print("e")
        exit()

    sig_time = end - start
    distance = sig_time / 0.000058
    
    return distance

try:
    print(get_distance())
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()