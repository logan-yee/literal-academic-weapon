import base64
from io import BytesIO
from PIL import Image

from screenshot_taker import capture_screenshot


# Convert image to base64
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

# Function to convert screenshots to PIL and then base64
def convert_screenshot_to_base64(image_path):
    pil_image = Image.open(image_path)

    # Convert RGBA to RGB if necessary
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')  # Convert to RGB

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # Save the image as JPEG
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Convert to base64
    return img_str
