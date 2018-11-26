"""This is the file that is ran when you want to start the full AR arcade"""

from view import View
from pong import PongView, PongModel, PongMouseController, PongObjectRecogController
from space_invaders import SpaceInvadersView, SpaceInvadersModel, SpaceInvadersController
import pygame
from pygame.locals import *
import time
import ObjectRecogImplementation as OR
from PIL import Image
import numpy as np
import os
from cursor import Cursor, CursorRecognition



class OverallModel():
    def __init__(self, organizer,screenSize,camera,clock,fps):
        self.organizer = organizer
        self.screenSize = screenSize
        self.width = screenSize[0]
        self.height = screenSize[1]
        self.clock = clock
        self.fps = fps
        self.cursor = Cursor(0,0,20,self.organizer)
        self.pongButton = CursorRecognition(30, [100, 200, 200,200],self.organizer)
        self.spaceInvadersButton = CursorRecognition(30, [500,200, 200,200],self.organizer)
        self.camera = camera
        self.objectCoordinates, self.cameraImage = OR.getCoords(self.camera)

    def update(self):
        if self.organizer.state == "homeScreen":
            self.pongButton.areaSurveillance(self.cursor, "pong", self.organizer, "state", "pong")
            self.spaceInvadersButton.areaSurveillance(self.cursor, "spaceInvaders", self.organizer, "state", "spaceInvaders")

        if self.organizer.state == "pong":
            self.pongPhaseKeeper = Organizer()  #create state machine for inside the pong game
            self.pongPhaseKeeper.state = "menu"
            self.pongModel = PongModel(self.screen,self.camera,self.pongPhaseKeeper)
            #TODO give existing screen to newly initialized view, because i think pygame can't handle multiple screens
            self.pongView = PongView(self.pongModel,self.screenSize)
            self.pongController = PongObjectRecogController(self.pongModel)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type is pygame.QUIT:
                        running = False
                if self.pongModel.backToHomeScreen == False:
                    self.pongController.update()
                    self.pongModel.update()
                    self.pongView.draw()
                    self.clock.tick(self.fps/2)
                else:
                    running = False
                    self.organizer.state == "homeScreen"

        if self.organizer.state == "spaceInvaders":
            self.spaceInvadersPhaseKeeper = Organizer() #create state machine for inside the pong game
            self.spaceInvadersPhaseKeeper.state = "menu"
            self.spaceInvadersModel = SpaceInvadersModel(self.screen,self.camera,self.spaceInvadersPhaseKeeper)
            self.spaceInvadersView = SpaceInvadersView(self.spaceInvadersModel)
            self.spaceInvadersController = SpaceInvadersController(self.spaceInvadersModel)
            running = True
            while running:
                for event in pygame.event.get():
                    print(event)
                    if event.type is pygame.QUIT:
                        running = False
                        self.organizer.state == "homeScreen"
                        self.spaceInvadersModel.backToHomeScreen = True

                if self.spaceInvadersModel.backToHomeScreen == False:
                    self.spaceInvadersController.update()
                    self.spaceInvadersModel.update()
                    self.spaceInvadersView.draw()
                    self.clock.tick(self.fps/2)
                else:
                    running = False
                    self.organizer.state == "homeScreen"


class MouseController():
    """handles input from the mouse"""
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            if self.model.organizer.state == "homeScreen":
                self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera)
                self.model.cursor.update(event.pos[0], event.pos[1])

class ObjectRecogController():
    """handles the input from the camera"""
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera)
        if self.model.objectCoordinates[1][0]== -1:
            self.model.cursor.update(self.model.objectCoordinates[0][0],self.model.objectCoordinates[0][1])
        else: #if the first controller has -1 as values, the controller is changed two the controller on the right side of the screen
            self.model.cursor.update(self.model.objectCoordinates[1][0],self.model.objectCoordinates[1][1])
        # If coordinates are -1, no object has been detected

class Organizer():
    """State machine that regulates whether or not we see the menu or the game
    The different states are:


    Instruction for adding a state:
    - You don't need to add a state in the Organizer() class. Just update the docstring to keep the documentation updated
    - Add an if-statement with the state name to the draw() function in the class PlayboardWindowView()
    - Add an if-statement with the state name t0 the handle_event() function in the class ArPongMouseController()
    """
    def __init__(self):
        self.state = "menu"
        self.settings_ballSpeed = 5
        self.settings_cursorColor = (255, 20, 147)

def Main():
    """Update graphics and check for pygame events.
    model -- an object of the type ArPongModel()
    view -- an object of the type PlayboardWindowView()
    controller -- an object ArPongMouseController()
    """
    pygame.init()
    pygame.mixer.init() #the mixer is for the playing the music
    clock = pygame.time.Clock()
    fps = 60
    screenSize = [1850,1080]
    camera = OR.setup(screenSize)
    organizer = Organizer()
    #We start the game in the organizer state
    organizer.state = "homeScreen"
    #initalize all the main classes
    mainModel = OverallModel(organizer,screenSize,camera,clock,fps)
    mainView = View(screenSize, mainModel)
    #mainController = Controller(mainModel)
    #this is the mouse controller
    fakeObject = ObjectRecogController(mainModel)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            #fakeObject.handle_event(event)
        fakeObject.update()
        mainModel.update()
        mainView.draw()
        clock.tick(fps)

if __name__ == '__main__':
    Main()
