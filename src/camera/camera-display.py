import time
import busio
import digitalio
from board import SCK, MOSI, MISO, D12, D21, D25
import adafruit_rgb_display.ili9341 as ili9341
from PIL import Image
import subprocess

# Pin configuration
CS_PIN = D21
DC_PIN = D12
RESET_PIN = D25

# SPI bus configuration
spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

# Initialize the display
display = ili9341.ILI9341(
    spi,
    cs=digitalio.DigitalInOut(CS_PIN),
    dc=digitalio.DigitalInOut(DC_PIN),
    rst=digitalio.DigitalInOut(RESET_PIN),
    baudrate=24000000,
)

# Set up the resolution for the ILI9341 display
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

try:
    # Continuous loop to capture frames and display
    while True:
        # Capture an image using libcamera-still
        subprocess.run(
            [
                'libcamera-still',
                '--width', str(DISPLAY_WIDTH),
                '--height', str(DISPLAY_HEIGHT),
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
        image = image.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Display the image on the ILI9341 display
        display.image(image)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clear the display before exiting
    display.fill(0)
    print("Display has been cleared.")
