import cv2 # type: ignore
from util import get_limits
from PIL import Image # type: ignore

greenColor = [0, 255, 0] # Blue color in BGR

# For capturing video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(greenColor)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # mask_ = Image.fromarray(mask)

    # bbox = mask_.getbbox()

    # if bbox is not None:
    #     x1, y1, x2, y2 = bbox
    #     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    coords = cv2.findNonZero(mask)

    if coords is not None:
        x1, y1, w, h = cv2.boundingRect(coords)
        x2, y2 = x1+w, y1+h 
        frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 5)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()