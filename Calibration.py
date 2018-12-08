import os
import pygame
from cursor import Cursor, CursorRecognition
import ObjectRecogImplementation as OR
import time

class CalibrationModel():
    """This is the model for the calibration test after the color calibration"""
    def __init__(self,screen,camera, organizer, controllernr, lastState):
        self.camera = camera
        self.screen = screen
        self.lastState = lastState
        self.backToLastState = False
        self.backToCalibration = False
        self.organizer = organizer
        self.firstCheck = False
        self.cursor = Cursor(0,0,20,self.organizer)
        self.upperLeftButton = CursorRecognition("1",20, [50,50,200,200],self.organizer)
        self.upperRightButton = CursorRecognition("2",20, [1850-250, 50, 200, 200], self.organizer)
        self.lowerRightButton = CursorRecognition("3", 20,[1850-250, 1080-250,200,200], self.organizer)
        self.lowerLeftButton = CursorRecognition("4", 20,[50, 1080-250, 200, 200] , self.organizer) # I hate hardcoding, resolution is 1850,1080
        self.controllernr = controllernr
        self.objectCoordinates, self.cameraImage = OR.getCoords(self.camera,0)  # Get the coordinates for controller '0'
        self.allowedTime = 15   # Time to complete the calibration
        self.startTime = time.time()   # Starttime when the program gets initialized
        self.elapsedTime = time.time() # gets updated every loop
        self.timer = self.elapsedTime - self.startTime # Time left


    def update(self):
        self.elapsedTime = time.time()
        self.timer = self.elapsedTime - self.startTime
        if self.timer > self.allowedTime:
            self.backToCalibration = True
        elif self.organizer.state == "first":
            self.upperLeftButton.areaSurveillance(self.cursor,"second",self.organizer,"state","second")
        elif self.organizer.state == "second":
            self.upperRightButton.areaSurveillance(self.cursor,"third", self.organizer, "state", "third")
        elif self.organizer.state == "third":
            self.lowerRightButton.areaSurveillance(self.cursor, "fourth", self.organizer, "state", "fourth")
        elif self.organizer.state == "fourth":
            self.lowerLeftButton.areaSurveillance(self.cursor, "fourth", self, "backToLastState", True)


class CalibrationView():
    """This is the view class for the CalibrationTest"""
    def __init__(self,model):
        self.model = model
        self.myfont = pygame.font.SysFont("monospace", 42) #Font that is used in states "game" and "select_speed" to prompt the user
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.colorGreen = (0,250,0)
        self.colorBlack = (0,0,0)


    def draw(self):
        """Draws the view of the calibration state, depending on the phase"""
        self.draw_background(self.model.screen)
        if self.model.organizer.state == "first":
            self.model.upperLeftButton.draw(self.model.screen)
            self.model.upperRightButton.draw(self.model.screen)
            self.model.lowerLeftButton.draw(self.model.screen)
            self.model.lowerRightButton.draw(self.model.screen)
        elif self.model.organizer.state == "second":
            self.model.upperLeftButton.draw(self.model.screen, self.colorGreen)
            self.model.upperRightButton.draw(self.model.screen)
            self.model.lowerLeftButton.draw(self.model.screen)
            self.model.lowerRightButton.draw(self.model.screen)
        elif self.model.organizer.state == "third":
            self.model.upperLeftButton.draw(self.model.screen, self.colorGreen)
            self.model.upperRightButton.draw(self.model.screen, self.colorGreen)
            self.model.lowerLeftButton.draw(self.model.screen)
            self.model.lowerRightButton.draw(self.model.screen)
        elif self.model.organizer.state == "fourth":
            self.model.upperLeftButton.draw(self.model.screen,self.colorGreen)
            self.model.upperRightButton.draw(self.model.screen,self.colorGreen)
            self.model.lowerLeftButton.draw(self.model.screen)
            self.model.lowerRightButton.draw(self.model.screen, self.colorGreen)


        timer = self.numberfont.render(str(int(self.model.allowedTime-self.model.timer)), 6, self.colorGreen)
        self.model.screen.blit(timer, (900,400))
        instructions = self.myfont.render("Hover over all the squares before the time runs out", 1, self.colorGreen)
        self.model.screen.blit(instructions, (400,20))
        self.model.cursor.draw(self.model.screen)
        pygame.display.update()

    def draw_background(self,screen): # draw the camera image to the background
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)

class CalibrationController():
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,self.model.controllernr)
        self.model.cursor.update(self.model.objectCoordinates[0], self.model.objectCoordinates[1])
