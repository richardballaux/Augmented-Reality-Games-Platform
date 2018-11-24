import cv2
import numpy as np

def calibrateColor(resolution):
    """
    Starts a camera screen and records the HSV values inside the drawn rectangle (ROI)

    Takes a resolution to draw the screen
    Returns a list of the min and max values of the recorded HSV values
    """
    cam= cv2.VideoCapture(0)
    rectangle = [(int(resolution[0]/2-resolution[0]/25),int(resolution[1]/2-resolution[1]/25)),(int(resolution[0]/2+resolution[0]/25),int(resolution[1]/2+resolution[1]/25))]
    running = True
    while running == True:
        ret, img=cam.read()
        img = cv2.resize(img,(resolution[0],resolution[1]))  # Resize the camera view to the desired resolution
        img = cv2.flip(img, 1)                               # Flip it
        cv2.rectangle(img, rectangle[0],rectangle[1],(0,0,255),2)  # Draw a rectangle for the scanning area
        roi = img[rectangle[0][1]:rectangle[1][1],rectangle[0][0]:rectangle[1][0]] # Defines the region of interest ROI
        hsvRoi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        # colorRange = hsvRoi[:,:,]
        print(hsvRoi)
        # if time.time()-startTime>3 and time.time()-startTime<6:          # Between 3 and 5 secs
        #     for i in range(3):                   # Save the  values of HSV
        #         if hsvRoi[:,:,i].min() < colorRange[i]:
        #             colorRange[i] = hsvRoi[:,:,i].min()
        #     for i in range(3):                 # Save the max values of HSV
        #         if hsvRoi[:,:,i].max() > colorRange[i+3]:
        #             colorRange[i+3] = hsvRoi[:,:,i].max()
        # if  time.time() - startTime > 5.5: # Breaks the while loop and the program
        #     running = False
        #     cv2.destroyAllWindows()
        #print(colorRange)
        
        cv2.imshow("cam",img)
        cv2.waitKey(10)
    return colorRange

if __name__ == '__main__':
    res = [900,400]
    range = calibrateColor(res)
    print(range)
