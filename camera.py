import cv2
import numpy as np
from web_interface import camera_lock  # Import at top of file

def detect_color_once():
    with camera_lock:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            return None

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Failed to grab frame")
            return None

        # Convert to HSV and analyze
        frame = cv2.resize(frame, (640, 480))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define ranges
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Count pixels
        green_pixels = cv2.countNonZero(mask_green)
        yellow_pixels = cv2.countNonZero(mask_yellow)
        red_pixels = cv2.countNonZero(mask_red)

        # Determine dominant color
        if red_pixels > green_pixels and red_pixels > yellow_pixels:
            return "Red"
        elif yellow_pixels > green_pixels and yellow_pixels > red_pixels:
            return "Yellow"
        elif green_pixels > red_pixels and green_pixels > yellow_pixels:
            return "Green"
        else:
            return None
