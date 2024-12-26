import RPi.GPIO as GPIO
import time


class Hcsr:
    # Pin configuration.
    HCSR04_OUT = 27
    HCSR04_IN = 17

    def __init__(self):
        GPIO.setup(self.HCSR04_OUT, GPIO.OUT)
        GPIO.setup(self.HCSR04_IN, GPIO.IN)

    def get_distance_cm(self):
        GPIO.output(self.HCSR04_OUT, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.HCSR04_OUT, GPIO.LOW)
    
        while GPIO.input(self.HCSR04_IN) == GPIO.LOW:
            start = time.time()
        
        while GPIO.input(self.HCSR04_IN) == GPIO.HIGH:
            end = time.time()
    
        sig_time = end - start
        distance = sig_time / 0.000058
        time.sleep(0.1)
        return distance


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    hcsr = Hcsr()
    
    while True:
        print(hcsr.get_distance_cm())        

