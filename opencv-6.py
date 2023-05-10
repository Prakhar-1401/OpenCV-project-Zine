import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(True):
    ret , frame =cap.read()

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)   

    contours , hierarchy = cv2.findContours(thresh_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for i, contours in enumerate(contours):
        if i ==0:
            continue

    perimeter=0.01*cv2.arcLength(contours,True)
    approx_Perimeter =cv2.approxPolyDP(contours,perimeter,True)

    cv2.drawContours(frame, contours , 0,(0,0,255),4)

    x,y,w,h =cv2.boundingRect(approx_Perimeter)
    x_midpoint=int(x+w/4)
    y_midpoint=int(y+h/3)

    coords=(x_midpoint,y_midpoint)
    colour=(0,0,0)
    font=cv2.FONT_HERSHEY_DUPLEX

    if len(approx_Perimeter)==3:
        cv2.putText(frame , "Triangle",coords,font,1,colour,1)
    elif len(approx_Perimeter)==4:
        cv2.putText(frame , "square",coords,font,1,colour,1)
    elif len(approx_Perimeter)==5:
        cv2.putText(frame , "pentagon",coords,font,1,colour,1)
    elif len(approx_Perimeter)==6:
        cv2.putText(frame , "hexagon",coords,font,1,colour,1)
    elif len(approx_Perimeter)==8:
        cv2.putText(frame , "octagon",coords,font,1,colour,1)
    elif len(approx_Perimeter)>8:
        cv2.putText(frame , "Circle",coords,font,1,colour,1)

    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([70, 255, 255])

    mask_red = cv2.inRange(hsv_roi, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv_roi, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv_roi, lower_green, upper_green)

    if np.sum(mask_red) > 0:
        cv2.putText(frame, "Red", (x, y), font, 1, colour, 1)
    elif np.sum(mask_blue) > 0:
            cv2.putText(frame, "Blue", (x, y), font, 1, colour, 1)
    elif np.sum(mask_green) > 0:
        cv2.putText(frame, "Green", (x, y), font, 1, colour, 1)


    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

