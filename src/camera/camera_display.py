import time
import busio
import digitalio
from board import SCK, MOSI, MISO, D12, D21, D25
import adafruit_rgb_display.ili9341 as ili9341
from PIL import Image
import subprocess
import numpy as np
import cv2
import requests
import urllib3

# Don't want a warning every single fucking time you sent a frame up.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CameraDisplay:
    # Set up the resolution for the ILI9341 display
    DISPLAY_WIDTH = 240
    DISPLAY_HEIGHT = 320
        
    # Pin configuration
    CS_PIN = D21
    DC_PIN = D12
    RESET_PIN = D25
    
    API_BASE_URI = "https://quickserve-syter6.azurewebsites.net"
    
    def __init__(self):
        # SPI bus configuration
        spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

        # Initialize the display
        self.display = ili9341.ILI9341(
            spi,
            cs=digitalio.DigitalInOut(self.CS_PIN),
            dc=digitalio.DigitalInOut(self.DC_PIN),
            rst=digitalio.DigitalInOut(self.RESET_PIN),
            baudrate=24000000,
        )
        
        # Load the facial recognition model.
        self.face_recognition_model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def apply_facial_recognition(self):
        # Load the image.
        frame = cv2.imread('/tmp/image.jpg')

        # Convert the image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces.
        faces = self.face_recognition_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around faces.
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (204, 255, 204), 2)

        # Save result.
        cv2.imwrite('/tmp/image.jpg', frame)


    def send_buffer_to_api(self):
        with open('/tmp/image.jpg', "rb") as image_file:
            frame_bytes = image_file.read()

        print(f"Sending frame of size {len(frame_bytes)} bytes")

        # Send the frame to the API.
        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(f"{self.API_BASE_URI}/feed/stream", 
            data=frame_bytes, 
            headers=headers, 
            timeout=30, 
            verify=False)

        if response.status_code != 200:
            print(f"Failed to send frame: {response.status_code}")


    def capture_and_display(self):
        # Capture an image using libcamera-still
        subprocess.run(
            [
                'libcamera-still',
                '--width', str(self.DISPLAY_WIDTH),
                '--height', str(self.DISPLAY_HEIGHT),
                '--output', '/tmp/image.jpg',
                '--timeout', '1'  # Capture a frame as quickly as possible
            ],
            check=True
        )

        # Open the captured image
        image = Image.open('/tmp/image.jpg')

        # Convert the image to RGB format
        image = image.convert('RGB')

        # Resize the image to match the ILI9341 display
        image = image.resize((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        # Display the image on the ILI9341 display
        self.display.image(image)


    def cleanup(self):
        self.display.fill(0)
