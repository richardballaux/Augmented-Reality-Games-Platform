import cv2
import numpy as np
import SetColor as sct

cam= cv2.VideoCapture(0)
bounds = np.asarray(sct.calibrateColor([800,400],cam))
lowerBound=bounds[0:3]
upperBound=bounds[3:6]


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))


while True:
    ret, img=cam.read()
    img=cv2.resize(img,(800,400))

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    im,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
    cv2.imshow("cam",img)
    cv2.waitKey(10)
