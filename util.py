import numpy as np # type: ignore
import cv2 # type: ignore

def get_limits(hsv_color, tolerance=20):
    lower = np.array([max(hsv_color[0] - tolerance, 0), 50, 50])
    upper = np.array([min(hsv_color[0] + tolerance, 179), 255, 255])
    return lower, upper