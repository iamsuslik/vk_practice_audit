import cv2
import numpy as np

def check_vks_quality() -> dict:
    return {
        "audio_quality": np.random.randint(80, 100),
        "video_quality": np.random.randint(75, 95),
        "latency": np.random.uniform(0.1, 0.5)
    }

def blur_background(image_path: str) -> str:
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    mask[100:-100, 100:-100] = 255
    blurred = cv2.GaussianBlur(img, (51, 51), 0)
    result = np.where(mask[..., None] == 255, img, blurred)
    cv2.imwrite("blurred_output.jpg", result)
    return "blurred_output.jpg"