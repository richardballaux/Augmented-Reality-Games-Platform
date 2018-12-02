import os
import pygame
from cursor import Cursor, CursorRecognition
import ObjectRecogImplementation as OR

class CalibrationModel():
    """This is the model for the calibration test after the color calibration"""
    def __init__(self,screen,camera,organizer):
        self.camera = camera
        self.screen = screen
        self.organizer = organizer
        self.backToHomeScreen = False
        self.firstCheck = False
        self.cursor = Cursor(0,0,20,self.organizer)
        self.upperLeftButton = CursorRecognition(30, [1800,1030,200,200],self.organizer)

    def update(self):
        if self.organizer.state == "calibration":
            self.upperLeftButton.areaSurveillance(self.cursor,"calibration",self,"firstCheck","True")

        if firstCheck == True:
            self.backToHomeScreen = True

    class CalibrationView():
        """This is the view class for the CalibrationTest""""
        def __init__(self,model):
            self.model =
