"""This is the file that is ran when you want to start the full AR arcade"""


from pong import PongView, PongModel, PongMouseController, PongObjectRecogController  # use everything, but import it like this so we can use the function just normally instead of the need to put the file in front
from space_invaders import SpaceInvadersView, SpaceInvadersModel, SpaceInvadersController
from Calibration import CalibrationModel, CalibrationView, CalibrationController
import pygame
from pygame.locals import *
import time
import ObjectRecogImplementation as OR
from PIL import Image
import numpy as np
import os
from cursor import Cursor, CursorRecognition



class OverallModel():
    """This is the class for the model that runs the homeScreen and the other games inside of it
    - organizer --  object of the organizer class. This keeps track of the state
    - screenSize -- list containing width and height of the desired screen size of the screen
    - camera -- cv.2 VideoCapture(0) object
    - clock --  a pygame clock
    - fps --    frames per second to run the pygame
    """
    def __init__(self, organizer,screenSize,camera,clock,fps):
        self.organizer = organizer
        self.screenSize = screenSize
        self.width = screenSize[0]
        self.height = screenSize[1]
        self.closePlatform = False   #The main while loop looks if this is true or false to break out of the while loop
        self.clock = clock
        self.fps = fps
        self.cursor = Cursor(0,0,20,self.organizer) # Initialize a cursor in coord (0,0) with radius 20
        self.pongButton = CursorRecognition("Pong",30, [100, 200, 200,200],self.organizer) # Make a button for the areaSurveillance with left corner coords (100,200) & length/width = 200
        self.spaceInvadersButton = CursorRecognition("Space Invaders",30, [500,200, 400,200],self.organizer)
        self.calibrationButton = CursorRecognition(" Calibrate", 30, [1000,200,300,200],self.organizer)
        self.closeButton = CursorRecognition("CLOSE",30,[1500,50,200,150],self.organizer)
        self.camera = camera
        OR.calibrate(self.screenSize, self.camera, 0) # Initialize the color for controller '0'
        organizer.state = "calibrationTest"
        self.objectCoordinates, self.cameraImage = OR.getCoords(self.camera,0)  # Get the coordinates for controller '0'
        self.controllernr = 0


    def update(self):
        """updates all the components of the model corresponding to their state"""
        if self.organizer.state == "homeScreen":
            self.pongButton.areaSurveillance(self.cursor, "pong", self.organizer, "state", "pong")
            self.spaceInvadersButton.areaSurveillance(self.cursor, "spaceInvaders", self.organizer, "state", "spaceInvaders")
            self.closeButton.areaSurveillance(self.cursor,"homeScreen",self,"closePlatform",True)
            self.calibrationButton.areaSurveillance(self.cursor,"calibrationTest",self.organizer,"state","calibrationTest")

        elif self.organizer.state == "pong":
            self.pongPhaseKeeper = Organizer()  #create state machine for inside the pong game
            self.pongPhaseKeeper.state = "menu" # First phase of the game in the state machine is the menu
            self.pongModel = PongModel(self.screen,self.camera,self.pongPhaseKeeper)
            self.pongView = PongView(self.pongModel)
            self.pongController = PongObjectRecogController(self.pongModel)
            pongRunning = True
            while pongRunning: # The program will stay in this while loop while running pong, until it gets closed
                for event in pygame.event.get():
                    if event.type is pygame.QUIT:
                        pongRunning = False
                        self.pongModel.backToHomeScreen = True
                        self.closePlatform = True
                if self.pongModel.backToHomeScreen == False: # If backToHomeScreen is false (game is still running), update everything
                    self.pongController.update()
                    self.pongModel.update()
                    self.pongView.draw()
                    self.clock.tick(self.fps/2)
                else:                                   # if backToHomeScreen is true (game ended, program got closed), stop the while loop and go back to the homeScreen state
                    pongRunning = False
                    self.organizer.state = "homeScreen"

        elif self.organizer.state == "spaceInvaders":
            self.spaceInvadersPhaseKeeper = Organizer() #create state machine for inside the pong game
            self.spaceInvadersPhaseKeeper.state = "menu"
            self.spaceInvadersModel = SpaceInvadersModel(self.screen,self.camera,self.spaceInvadersPhaseKeeper)
            self.spaceInvadersView = SpaceInvadersView(self.spaceInvadersModel)
            self.spaceInvadersController = SpaceInvadersController(self.spaceInvadersModel)
            spaceRunning = True
            while spaceRunning:
                for event in pygame.event.get():
                    if event.type is pygame.QUIT:
                        spaceRunning = False
                        self.spaceInvadersModel.backToHomeScreen = True
                        self.closePlatform = True
                if self.spaceInvadersModel.backToHomeScreen == False:
                    self.spaceInvadersController.update()
                    self.spaceInvadersModel.update()
                    self.spaceInvadersView.draw()
                    self.clock.tick(self.fps/2)  #TODO What is this??
                else:
                    spaceRunning = False
                    self.organizer.state = "homeScreen"

        elif self.organizer.state == "calibrationTest":
            self.calibrationPhaseKeeper = Organizer()
            self.calibrationPhaseKeeper.state = "first"
            self.calibrationModel = CalibrationModel(self.screen,self.camera, self.calibrationPhaseKeeper, self.controllernr, self.organizer.lastState)
            self.calibrationView = CalibrationView(self.calibrationModel)
            self.calibrationController = CalibrationController(self.calibrationModel)
            calibrationRunning = True
            while calibrationRunning:
                for event in pygame.event.get():
                    if event.type is pygame.QUIT:
                        calibrationRunning = False
                        self.calibrationModel.backToHomeScreen = True
                        self.closePlatform = True
                if self.calibrationModel.backToCalibration == False:
                    self.calibrationController.update()
                    self.calibrationModel.update()
                    self.calibrationView.draw()
                    self.clock.tick(self.fps/2)
                else:
                    calibrationRunning = False
                    OR.calibrate(self.screenSize, self.camera, self.controllernr)
                    self.organizer.state = "calibrationTest"
                if self.calibrationModel.backToLastState == True:
                    calibrationRunning = False
                    self.organizer.state = self.calibrationModel.lastState

            self.lastState = self.organizer.state

class MouseController():
    """handles input from the mouse"""
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            if self.model.organizer.state == "homeScreen":
                self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0)
                self.model.cursor.update(event.pos[0], event.pos[1])

class ObjectRecogController():
    """handles the input from the camera"""
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0)
        self.model.cursor.update(self.model.objectCoordinates[0],self.model.objectCoordinates[1])
        # If coordinates are -1, no object has been detected

class overallView():
    """This is the view class for the OverallModel, it writes all those components to the screen"""
    def __init__(self,screenSize,model):
        self.screen_size = screenSize
        self.model = model
        self.model.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption = ("AR-Arcade")

    def draw(self):
        self.draw_background()
        if self.model.organizer.state == "homeScreen":
            #draw squares for buttons for pong and spaceinvaders
            self.model.pongButton.draw(self.model.screen)
            self.model.spaceInvadersButton.draw(self.model.screen)
            self.model.calibrationButton.draw(self.model.screen)
            self.model.closeButton.draw(self.model.screen)
            self.model.cursor.draw(self.model.screen)
        pygame.display.update()

    def draw_background(self):
        """draws the last taken camera image to the screen as a background"""
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)

class Organizer():
    """State machine that regulates the states in the different models. We use one organizer for the OverallModel and his overallView.
    Next every seperate game/application has its own Organizer called phaseKeeper.
    """
    def __init__(self):
        self.state = "menu"
        self.settings_ballSpeed = 5
        self.settings_cursorColor = (255, 20, 147)
        self.win = False
        self.lastState = "homeScreen"


def Main():
    """
    Start this function to start the platform. This initializes the OverallModel and its view and its conroller.
    """
    pygame.init()
    pygame.mixer.init() #the mixer is for the playing the music
    clock = pygame.time.Clock()
    fps = 60
    screenSize = [1850,1080]
    camera = OR.setup(screenSize) # Initialize a camera via the object recognition in openCV
    organizer = Organizer() # initialize an Organizer object
    #We start the game in the organizer state


    organizer.state = "homeScreen"
    #initalize all the main classes
    mainModel = OverallModel(organizer,screenSize,camera,clock,fps)
    mainView = overallView(screenSize, mainModel)
    overallRecogController = ObjectRecogController(mainModel)
    overallRunning = True
    while overallRunning:
        overallRecogController.update()
        mainModel.update()
        mainView.draw()
        if mainModel.closePlatform == True:
            overallRunning = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                overallRunning = False
        clock.tick(fps)

if __name__ == '__main__':
    Main()
