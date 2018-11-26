import cv2
import numpy as np
import time

def calibrateColor(resolution):
    """
    Starts a camera screen and records the HSV values inside the drawn rectangle (ROI)

    Takes a resolution to draw the screen
    Returns a list of the min and max values of the recorded HSV values
    """
    cam= cv2.VideoCapture(0)
    colorRange = [255,255,255,0,0,0]
    rectangle = [(int(resolution[0]/2-resolution[0]/25),int(resolution[1]/2-resolution[1]/25)),(int(resolution[0]/2+resolution[0]/25),int(resolution[1]/2+resolution[1]/25))]
    startTime = time.time() # Saves the time the program started
    running = True
    font = cv2.FONT_HERSHEY_SIMPLEX  # font for the timer
    while running == True:
        ret, img=cam.read()
        img = cv2.resize(img,(resolution[0],resolution[1]))  # Resize the camera view to the desired resolution
        img = cv2.flip(img, 1)                               # Flip it
        roi = img[rectangle[0][1]:rectangle[1][1],rectangle[0][0]:rectangle[1][0]] # Defines the region of interest ROI
        hsvRoi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        cv2.putText(img,str(int(time.time()-startTime)),(10,20), font, 1,(255,255,255),2)  # Displays the time
        if time.time()-startTime>3 and time.time()-startTime<6:          # Between 3 and 5 secs
            cv2.rectangle(img, rectangle[0],rectangle[1],(0,255,0),4)  # Draw a rectangle for the scanning area
            for i in range(3):                   # Save the  values of HSV
                if hsvRoi[:,:,i].min() < colorRange[i]:
                    colorRange[i] = hsvRoi[:,:,i].min()
            for i in range(3):                 # Save the max values of HSV
                if hsvRoi[:,:,i].max() > colorRange[i+3]:
                    colorRange[i+3] = hsvRoi[:,:,i].max()
        else:
            cv2.rectangle(img, rectangle[0],rectangle[1],(0,0,255),2)  # Draw a rectangle for the scanning area
        if  time.time() - startTime > 5.5: # Breaks the while loop and the program
            running = False
            cv2.destroyAllWindows()


        cv2.imshow("cam",img)
        cv2.waitKey(10)
        colorRange[0] = colorRange[3] - 20
    return colorRange

if __name__ == '__main__':
    res = [900,400]
    range = calibrateColor(res)
    print(range)
