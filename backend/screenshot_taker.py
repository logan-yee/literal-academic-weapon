import os
from PIL import ImageGrab
from datetime import datetime

def capture_screenshot():
    # Ensure 'screenshots' folder exists
    if not os.path.exists('backend/screenshots'):
        os.makedirs('backend/screenshots')

    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backend/screenshots/screenshot_{timestamp}.png"

    # Capture the screenshot and save it
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")


    return filename