import cv2
import numpy as np
import json
import os

def process_floor_plan(image_path):
    # Read and preprocess
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Failed to load image")

    # Threshold to binary (black lines on white)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Morphology to clean lines
    kernel = np.ones((5,5), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)

    # Detect lines with Hough
    lines = cv2.HoughLinesP(binary, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)

    # Scale (adjust based on your image's real size, e.g., 10m x 5m for small plan)
    height, width = img.shape
    scale_x = 10.0 / width
    scale_y = 5.0 / height

    walls = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Scale to meters
            x1_m = x1 * scale_x
            y1_m = y1 * scale_y
            x2_m = x2 * scale_x
            y2_m = y2 * scale_y
            # Add as wall segment
            walls.append({
                "start": [x1_m, 0, y1_m],
                "end": [x2_m, 0, y2_m],
                "height": 2.7,  # Extrude height
                "color": "#D4A59A"  # Default wall color
            })

    # Simple decors (add manually for now, based on assumed rooms)
    decors = [
        {"type": "bed", "position": [2.0, 0.5, 2.0], "size": [1.5, 0.5, 2.0], "color": "#8A9A5B"},
        {"type": "table", "position": [4.0, 0.5, 3.0], "size": [1.0, 0.5, 1.0], "color": "#A9CBA4"}
    ]

    layout_data = {"walls": walls, "decors": decors, "floors": ["ground"]}
    return json.dumps(layout_data)

# Test
if __name__ == "__main__":
    test_image = "D:\\construction_client\\static\\uploads\\test_plan.png"  # Update to static
    if os.path.exists(test_image):
        result = process_floor_plan(test_image)
        print(result)
    else:
        print(f"Image not found at {test_image}.")
