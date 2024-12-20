import cv2 #type: ignore
import numpy as np #type: ignore
from util import get_limits

green_bgr = [0, 255, 0]
green_hsv = cv2.cvtColor(np.uint8([[green_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
lower_limit, upper_limit = get_limits(green_hsv)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv_frame)

    blank = np.zeros_like(hue)
    
    hue = cv2.multiply(hue, 2)  
    
    # Create colored visualizations
    hue_color = cv2.merge([hue, np.ones_like(hue) * 255, np.ones_like(hue) * 255])
    hue_color = cv2.cvtColor(hue_color, cv2.COLOR_HSV2BGR)
    
    saturation_color = cv2.merge([np.ones_like(saturation) * 90, saturation, np.ones_like(saturation) * 255])
    saturation_color = cv2.cvtColor(saturation_color, cv2.COLOR_HSV2BGR)
    
    value_color = cv2.merge([np.zeros_like(value), np.zeros_like(value), value])
    
    mask = cv2.inRange(hsv_frame, lower_limit, upper_limit) # mask
    res = cv2.bitwise_and(frame, frame, mask=mask) # result
    
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1) #erosion
    dilation = cv2.dilate(erosion, kernel, iterations=1) #dilation
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    if len(contours) > 0:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        for cnt in contours[:3]:
            area = cv2.contourArea(cnt)
            if area > 500:
                x1, y1, w, h = cv2.boundingRect(cnt)
                x2, y2 = x1+w, y1+h
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("HsvFrame", hsv_frame)
    cv2.imshow("Hue", hue_color)
    cv2.imshow("Saturation", saturation_color)
    cv2.imshow("Value", value_color)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", res)
    cv2.imshow("Erosion", erosion)
    cv2.imshow("Dilation", dilation)
    cv2.imshow("Opening", opening)
    cv2.imshow("Closing", closing)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()