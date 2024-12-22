from camera.camera_display import CameraDisplay
import time

def camera_display_n_seconds(n):
    start_time = time.time()
    camera_display = CameraDisplay()


    while True:
        camera_display.capture_and_display()
        camera_display.apply_facial_recognition()
        camera_display.send_buffer_to_api()
        
        if time.time() - start_time >= n and n != -1:
            print(f"Done with displaying {n} times :)")
            break

    camera_display.cleanup()


while True:
    secs = int(input("how many seconds should it turn on?\n>>>"))
    camera_display_n_seconds(-1)
