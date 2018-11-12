"""This is the file that is ran when you want to start the full AR arcade"""

from view import View
from overallModel import OverallModel
from pong import PongView, PongModel, PongMouseController, PongObjectRecogController
import pygame
from pygame.locals import *
import time
import ObjectRecogImplementation as OR
from PIL import Image
import numpy as np
import os
from cursor import Cursor, CursorRecognition

class OverallModel():
    def __init__(self,organizer):
        pass


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
    organizer.state = "menu"
    #arguments are screenSize, the BoundaryOffset, BoundaryThickness, ballRadius, ballSpeed

    #initalize all the main classes
    mainModel = OverallModel(organizer)
    mainView = View(screenSize, organizer,mainModel)
    mainController = OverallController(mainModel)
    running = True
    while running:
        if 0xFF == ord('q'):
            running = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            #controller.handle_event(event)
        mainController.update()
        mainModel.update()
        mainView.draw()
        clock.tick(fps)

class Organizer():
    """State machine that regulates whether or not we see the menu or the game
    The different states are:
    - "menu"
    - "select_speed"
    - "pong_game"
    - "endgame"

    Instruction for adding a state:
    - You don't need to add a state in the Organizer() class. Just update the docstring to keep the documentation updated
    - Add an if-statement with the state name to the draw() function in the class PlayboardWindowView()
    - Add an if-statement with the state name t0 the handle_event() function in the class ArPongMouseController()
    """
    def __init__(self):
        self.state = "menu"
        self.settings_ballSpeed = 5
        self.settings_cursorColor = (255, 20, 147)

if __name__ == '__main__':
    Main()
    # model = PongModel(screenSize,(50,50),10,camera,organizer)
    # view = PongView(model,screenSize, organizer)
    # view._draw_background()
    # #controller = PongMouseController(model)
    # controller = PongObjectRecogController(model)
    # Main(model,view,controller)
