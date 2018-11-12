import cv2
import numpy as np
import time

cam= cv2.VideoCapture(0)
resolution = [340,220]
colorRange = [255,255,255,0,0,0]
rectangle = [(int(resolution[0]/2-resolution[0]/15),int(resolution[1]/2-resolution[1]/15)),(int(resolution[0]/2+resolution[0]/15),int(resolution[1]/2+resolution[1]/15))]
startTime = time.time()


def getValues():
    while True:
        ret, img=cam.read()
        img = cv2.resize(img,(resolution[0],resolution[1]))
        img = cv2.flip(img, 1)
        cv2.rectangle(img, rectangle[0],rectangle[1],(0,0,255),2)
        roi = img[rectangle[0][1]:rectangle[1][1],rectangle[0][0]:rectangle[1][0]]
        hsvRoi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        #print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min(), hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()))
        cv2.imshow("cam",img)
        cv2.waitKey(10)
        #print(time.time()-startTime)
        if time.time()-startTime>3 and time.time()-startTime<5:          # Between 3 and 5 secs
            for i in range(3):                   # Save the  values of HSV
                print(hsvRoi[:,:,i].min())
                if hsvRoi[:,:,i].min() < colorRange[i]:
                    print("black")
                    colorRange[i] = hsvRoi[:,:,i].min()
            for i in range(3):                 # Save the max values of HSV
                if hsvRoi[:,:,i].max() > colorRange[i+3]:
                    print("check")
                    colorRange[i+3] = hsvRoi[:,:,i].max()
            print(colorRange)
    return colorRange

list = getValues()
print(list)
