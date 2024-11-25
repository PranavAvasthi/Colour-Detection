import cv2 # type: ignore
from util import get_limits

blueColor = [255, 0, 0] # Blue color in BGR

# For capturing video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(blueColor)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    cv2.imshow("Frame", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()