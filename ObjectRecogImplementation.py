"""this file contains everything concerning the objectrecognition"""

#TODO find a way to track 2 colors at the same time.

import cv2
cv2.__version__
import numpy as np
import SetColor as sct
centerCoordsZero = (0,0)
centerCoordsOne = (0,0)

def calibrate(resolution, cam, controller):
    global lowerBoundZero
    global lowerBoundOne
    global upperBoundZero
    global upperBoundOne

    bounds = np.asarray(sct.calibrateColor(resolution,cam))
    if controller == 0:
        lowerBoundZero=bounds[0:3]
        upperBoundZero=bounds[3:6]
    else:
        lowerBoundOne=bounds[0:3]
        upperBoundOne=bounds[3:6]


def setup(resolution):
    """
    Setting up the camera with the resolution, sets a resolution and creates an
    range of colors to detect. Later this can be set to other colors and maybe
    color recognition. Camera gets initialized.

    resolution -- a list of the width and height of the screen
    """
    # Defining screen resolution
    global horRes
    horRes = resolution[0]
    global vertRes
    vertRes = resolution[1]

    #resolution we want it to analyze (so it doesnt have to analyze the whole picture)
    global analyze_res_width
    analyze_res_width = 500
    global analyze_res_height
    analyze_res_height = 281

    # Variables to adjust the coordinates to the displayed image
    global width_ratio
    width_ratio = horRes/analyze_res_width
    global height_ratio
    height_ratio = vertRes/analyze_res_height



    # Make a VideoCapture object (camera)
    cam= cv2.VideoCapture(0)
    return cam


def getCoords(cam,controller):
    """
    Gets the coordinates of the objects in the camera objec and returns the
    background image. (camera view)

    cam -- camera object
    controller -- get the coords from the controller
    """
    # Making kernel to delete noise (open = erosion followed by dilation, close is reversed)
    # MORPH_OPEN deletes noise outside of the object, MORPH_CLOSE inside of the object)
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))


    # Get the video data
    ret, orImg=cam.read()

    # Resize the frame, to have not too many pixels and flip the image.
    orImg=cv2.resize(orImg,(horRes,vertRes))
    global img
    global centerCoordsZero
    global centerCoordsOne
    img = cv2.flip(orImg, 1)
    backGroundImage = cv2.cvtColor(np.rot90(orImg),cv2.COLOR_BGR2RGB)

    #resize image to analyze
    resized_img = cv2.resize(img,(analyze_res_width,analyze_res_height))
    # convert BGR to HSV
    imgHSV= cv2.cvtColor(resized_img,cv2.COLOR_BGR2HSV)
    if controller == 0:
        lowerBound = lowerBoundZero
        upperBound = upperBoundZero
    else:
        lowerBound = lowerBoundOne
        upperBound = upperBoundOne
    # create the Mask, look for the object in this color range
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    # Delete all the noise in the image
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose # This is our final image with object in black-white (object is white)
    im2, conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # Finds contours of the object
    coords = []
    widthList = []
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])  #Draws rectangle around contours
        #(x,y),rad = cv2.minEnclosingCircle(conts[i])       # draws circle instead of rectangle (slower)
        center = (int(width_ratio*x+width_ratio*w/2),int(height_ratio*y+height_ratio*h/2))
        coords.append(center)
        widthList.append(w)
    if len(widthList) > 0:
        if controller ==0:
            centerCoordsZero = coords[widthList.index(max(widthList))]
        else:
            centerCoordsOne = coords[widthList.index(max(widthList))]
    #cv2.circle(img,center,int(rad),(0,22,0),2)
    if controller == 0:
        return centerCoordsZero,backGroundImage  # return coords and camera image for the main Controller
    else:
        return centerCoordsOne #return just the coords, camera is provided via the first controller


# test code to see if the functions work
def main():
    resolution = [1000 ,562]
    cam = setup(resolution)
    calibrate(resolution, cam, 0)
    while True:
        coords,img = getCoords(cam,0)
        print(coords)
        #cv2.imshow("cam",img)
        #cv2.waitKey(10)

if __name__ == '__main__':
    main()
