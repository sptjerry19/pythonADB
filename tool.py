import os, time, sys
try: 
    import numpy as np
    import cv2
    import subprocess
except: 
    os.system("pip install cv2")
    os.system("pip install numpy")
    os.system("pip install opencv-python")
    os.system("pip install pure-python-adb")
    
import numpy as np
import cv2
import subprocess

class ADB:
    @staticmethod
    def adb_shell(command):
        """Run ADB shell command."""
        subprocess.run(['adb', 'shell', command], check=True)

    @staticmethod
    def adb_click(x, y):
        """Perform a click event at the specified coordinates."""
        ADB.adb_shell(f'input tap {x} {y}')

    @staticmethod
    def capture_screenshot():
        """Capture a emulator-5554 screenshot of the device's screen."""
        os.system(f"adb -s emulator-5554 exec-out screencap -p > screenshot.png ")

    @staticmethod
    def find_image(target_image_path, screenshot_path):
        """Find the target image within the screenshot."""
        target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
        screenshot = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
        
        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        return max_loc

def find_and_click(target_image_path):
    # Capture a screenshot
    ADB.capture_screenshot()
    
    # Find the target image within the screenshot
    screenshot_path = 'screenshot.png'
    match_location = ADB.find_image(target_image_path, screenshot_path)
    
    if match_location:
        # Calculate the coordinates of the center of the found image
        target_image = cv2.imread(target_image_path)
        h, w = target_image.shape[:2]
        center_x = match_location[0] + w // 2
        center_y = match_location[1] + h // 2
        
        # Simulate a click event at the center of the found image
        ADB.adb_click(center_x, center_y)
    else:
        print("Image not found")

def get_connected_devices():
    # Run the ADB command to get the list of connected devices
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    
    # Split the output into lines and skip the first line (header)
    lines = result.stdout.strip().split('\n')[1:]
    
    # Extract the device IDs from the output
    devices = [line.split('\t')[0] for line in lines if line.strip()]
    
    return devices

if __name__ == "__main__":
    connected_devices = get_connected_devices()
    print("Connected devices:")
    for device in connected_devices:
        print(device)
        # Path to the image you want to find and click on
        target_image_path = './images/1.png'
        find_and_click(target_image_path)