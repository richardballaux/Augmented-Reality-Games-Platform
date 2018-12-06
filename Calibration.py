import os
import pygame
from cursor import Cursor, CursorRecognition
import ObjectRecogImplementation as OR

class CalibrationModel():
    """This is the model for the calibration test after the color calibration"""
    def __init__(self,screen,camera, organizer, controllernr):
        self.camera = camera
        self.screen = screen
        self.backToHomeScreen = False
        self.organizer = organizer
        self.firstCheck = False
        self.cursor = Cursor(0,0,20,self.organizer)
        self.upperLeftButton = CursorRecognition("1",30, [10,10,200,200],self.organizer)
        self.controllernr = controllernr

    def update(self):

        self.upperLeftButton.areaSurveillance(self.cursor,"calibration",self,"firstCheck","True")

        if firstCheck == True:
            self.backToHomeScreen = True

class CalibrationView():
    """This is the view class for the CalibrationTest"""
    def __init__(self,model):
        self.model = model
        self.myfont = pygame.font.SysFont("monospace", 42) #Font that is used in states "game" and "select_speed" to prompt the user
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.ColorGreen = (0,250,0)

    def draw(self):
        self.draw_background(self.model.screen)
        if self.firstCheck == True:
            self.model.upperLeftButton.draw(self.model.screen, self.ColorGreen)
        else:
            self.model.upperLeftButton.draw(self.model.screen)
        instructions = self.myfont.render("Hover over all the squares before the time runs out", 1, self.ColorGreen)
        self.model.screen.blit(instructions, (400,20))
        pygame.display.update()

    def draw_background(self,screen): # draw the camera image to the background
        self.model.screen.fill(self.ColorBlack)
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)
        pygame.display.update()

class CalibrationController():
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0)
        self.model.cursor.update(self.model.objsectCoordinates[0], self.model.objectCoordinates[1])
