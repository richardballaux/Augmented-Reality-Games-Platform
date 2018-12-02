"""
This is the file that has all the needed things to play pong: view,model,mouse- and colorrecognition-controller
@authors: Richard Ballaux, Viktor Deturck, Leon Santen"""

# Necessary libraries
import pygame
from pygame.locals import *
import time
import ObjectRecogImplementation as OR
from PIL import Image
import numpy as np
import os
from cursor import Cursor, CursorRecognition

class PongView():
    """this board includes the outlines, the ball, the paddles and the goals"""
    def __init__(self,model):
        self.model=model
        self.screen=self.model.screen
        self.myfont = pygame.font.SysFont("monospace", 42) #Font that is used in states "game" and "select_speed" to prompt the user
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.ColorGreen = (0,250,0)
        self.ColorBlack = (0,0,0)


    def _draw_background(self, color = (0,0,0)):
        """draw background with plain Color
        color -- RGB format (R,G,B), values from 0 to 255, default color is black"""
        self.screen.fill(color)

        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)
        pygame.display.update()

    def draw(self):
        """draws corresponding to the state of organizer.state the different organizer settings or game"""

        if self.model.organizer.state == "menu": # Draw start screen
            self._draw_background()
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.ColorGreen)
            self.screen.blit(menutext, (50,50))
            self.model.startButton.draw(self.model.screen)
            self.model.cursor.draw(self.screen)
            pygame.display.update()

        if self.model.organizer.state == "select_speed":
            self._draw_background((255, 224, 254))
            menutext = self.myfont.render("Select a speed by hovering over the desired speed", 1, self.ColorBlack) # Message for menu to select speed
            self.screen.blit(menutext, (50,50))
            # DRAW BUTTON TO CHANGE SPEED OF BAll
            self.model.speedOneButton.draw(self.screen)
            self.model.speedTwoButton.draw(self.screen)
            self.model.speedThreeButton.draw(self.screen)
            self.model.speedFourButton.draw(self.screen)
            self.model.speedFiveButton.draw(self.screen)

            self.model.cursor.draw(self.screen)
            pygame.display.update()

        if self.model.organizer.state == "pong_game":
            self._draw_background()
            for component in self.model.components:
                 component.draw(self.screen)
            pygame.display.update()

        if self.model.organizer.state == "endgame":
            self._draw_background()
            pygame.draw.rect(self.screen, (150,150,0), pygame.Rect(int((self.model.width/6)), int(self.model.height/2)-50, int(self.model.width*4/6),150))
            if self.model.organizer.winner ==1:
                playertext = self.myfont.render("LEFT PLAYER WON", 1, self.ColorBlack)
            if self.model.organizer.winner ==2:
                playertext = self.myfont.render("RIGHT PLAYER WON", 1, self.ColorBlack)
            self.screen.blit(playertext, (int((self.model.width/6)*2),self.model.height/2))

            self.model.restartButton.draw(self.screen)
            self.screen.blit(replayText, (int((self.model.width/6)*5),int((self.model.width/6)*2)))
            self.model.homeScreenButton.draw(self.screen)
            self.model.cursor.draw(self.screen)
            pygame.display.update()

# class Organizer():
#     """State machine that regulates whether or not we see the menu or the game
#     The different states are:
#     - "menu"
#     - "select_speed"
#     - "pong_game"
#     - "endgame"
#
#     Instruction for adding a state:
#     - You don't need to add a state in the organizer() class. Just update the docstring to keep the documentation updated
#     - Add an if-statement with the state name to the draw() function in the class PlayboardWindowView()
#     - Add an if-statement with the state name t0 the handle_event() function in the class ArPongMouseController()
#     """
#     def __init__(self):
#         self.state = "menu"
#         self.settings_ballSpeed = 5
#         self.settings_cursorColor = (255, 20, 147)

class PongModel():
    """encodes a model of the game state
    windowSize -- This is a list wih the width and the height of the screen size demanded
    boundaryOffset -- This is the distance between the edges of the screen and the boundary
    boundaryThickness --  This is the thickness of the boundary in pixels
    camera --   This is a VideoCapture-object that the getCoords-function needs as input
    """
    def __init__(self,screen,camera,organizer):
        boundaryOffset = [50,50]
        boundaryThickness = 10
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.backToHomeScreen = False
        boundaryLength = self.width-2*boundaryOffset[0]
        self.upperboundary = Boundary(boundaryOffset[0],boundaryOffset[1],boundaryThickness,boundaryLength)
        self.lowerboundary = Boundary(boundaryOffset[0],self.height-boundaryOffset[1],boundaryThickness,boundaryLength)
        self.organizer = organizer
        self.ball = Ball(int(self.width/5),int(self.height/5),20)

        paddleWidth = 10
        paddleHeight = 100
        cursorRadius = 20
        self.leftPaddle = Paddle(10,self.height/2,paddleHeight,paddleWidth)
        self.rightPaddle = Paddle(self.width-10-paddleWidth,self.height/2,paddleHeight,paddleWidth)
        self.score = Score(self)

        self.components = (self.upperboundary,self.lowerboundary,self.ball,self.leftPaddle,self.rightPaddle,self.score)

        self.cursor = Cursor(int(self.width/2),int(self.height/2), cursorRadius,self.organizer)
        #Buttons
        self.selectSpeedButton = CursorRecognition("Select speed",30, [50, self.height/2-50, 200,500],self.organizer) #Triggerare in state "menu" - yellow square
        self.speedOneButton = CursorRecognition("1",30, [int((self.width/6)*1)-50, int(self.height/2)-150, 150,150],self.organizer) # Number 1 to 5: square to select speed in state "select_speed"
        self.speedTwoButton = CursorRecognition("2",30, [int((self.width/6)*2)-50, int(self.height/2)+150, 150,150],self.organizer)
        self.speedThreeButton = CursorRecognition("3",30, [int((self.width/6)*3)-50, int(self.height/2)-150, 150,150],self.organizer)
        self.speedFourButton = CursorRecognition("4",30, [int((self.width/6)*4)-50, int(self.height/2)+150, 150,150],self.organizer)
        self.speedFiveButton = CursorRecognition("5",30, [int((self.width/6)*5)-50, int(self.height/2)-150, 150,150],self.organizer) # Triggers square to repeat the game in state "endgame"
        self.restartButton = CursorRecognition("Restart", 30,[int((self.width/6)*5),int((self.width/6)*2),200,150],self.organizer)
        self.homeScreenButton = CursorRecognition("Home screen", 30,[int((self.width/6)*1),int((self.width/6)*2),250,150],self.organizer)
        self.startButton = CursorRecognition("Start", 30,[int((self.width/6)*1),int((self.width/6)*2),100,100],self.organizer)

        #camera and objectrecognition
        self.camera = camera
        OR.calibrate([self.width, self.height], self.camera, 1) # Initialize the color for controller '1'
        self.objectCoordinatesRight, self.cameraImage = OR.getCoords(self.camera,0) #gets coordinates of the two objects from the python file ObjectRecogImplementation.py

        #initialize the sprite groups for collision detection
        self.boundaryGroup = pygame.sprite.Group()
        self.boundaryGroup.add(self.upperboundary)
        self.boundaryGroup.add(self.lowerboundary)

        self.paddleGroup = pygame.sprite.Group()
        self.paddleGroup.add(self.leftPaddle)
        self.paddleGroup.add(self.rightPaddle)

        #Initialize the sounds
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.boundarySound = pygame.mixer.Sound(dir_path+"/data/boundaryBounce.wav")
        self.paddleSound = pygame.mixer.Sound(dir_path+"/data/paddleBounce.wav")
        self.deathSound = pygame.mixer.Sound(dir_path+"/data/death.wav")

    def update(self):
        """updates all the components the model has dependent on what state Organizer.state is in"""
        if self.organizer.state == "menu":
            self.selectSpeedButton.areaSurveillance(self.cursor, "select_speed", self.organizer, "state", "select_speed")

        if self.organizer.state == "select_speed": # Set 5 areas to click on, each mapped to a different ball speed
            self.speedOneButton.areaSurveillance(self.cursor, "pong_game", self.organizer, "settings_ballSpeed", 5)
            self.speedTwoButton.areaSurveillance(self.cursor, "pong_game", self.organizer, "settings_ballSpeed", 10)
            self.speedThreeButton.areaSurveillance(self.cursor, "pong_game", self.organizer, "settings_ballSpeed", 15)
            self.speedFourButton.areaSurveillance(self.cursor, "pong_game", self.organizer, "settings_ballSpeed", 22)
            self.speedFiveButton.areaSurveillance(self.cursor, "pong_game", self.organizer, "settings_ballSpeed", 28)

        if self.organizer.state == "pong_game":
            self.ball.update(self.organizer)
            #first update the position of the ball and then check if there has been a collision
            boundaryBounce = pygame.sprite.spritecollide(self.ball,self.boundaryGroup,False)
            if len(boundaryBounce)>0: # In case of bounce on boundary
                self.ball.movingDirection[1] = -self.ball.movingDirection[1] # Change the x-direction of the its opposite after the bounce
                pygame.mixer.Sound.play(self.boundarySound)

            paddleBounce = pygame.sprite.spritecollide(self.ball,self.paddleGroup,False)
            if len(paddleBounce)>0:
                self.ball.movingDirection[0] = -self.ball.movingDirection[0]
                pygame.mixer.Sound.play(self.paddleSound)

            if self.ball.x < 5: #When ball goes in the left goal
                self.score.update(1)        #Update the scores( give player2 a point)
                pygame.mixer.Sound.play(self.deathSound)
                self.ball.x = int(self.width/5) #move the ball to its new start position
                self.ball.rect.x = self.ball.x  #as well as its attribute rect to it can collide
                self.ball.y = int(self.height/5)
                self.ball.rect.y = self.ball.y
                self.ball.movingDirection=[1,1] #Makes the ball go to right down again

            if self.ball.x > self.width-5: #when ball goes in the right goal
                self.score.update(0)       #update scores(give player 1 a point)
                pygame.mixer.Sound.play(self.deathSound)
                self.ball.x = int(4*self.width/5)
                self.ball.rect.x = self.ball.x
                self.ball.y = int(self.height/5)
                self.ball.rect.y = self.ball.y
                self.ball.movingDirection=[-1,1]

        if self.organizer.state == "endgame": #this state is entered when one of the players reaches 5 points
            self.restartButton.areaSurveillance(self.cursor, "menu", self.organizer, "state", "menu")
            self.homeScreenButton.areaSurveillance(self.cursor, "True",self, "backToHomeScreen","True")
            self.score.reset()

class PongMouseController():
    """handles input from the mouse"""
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            if organizer.state == "menu" or "select_speed" or "endgame":
                self.model.objectCoordinatesRight, self.model.cameraImage = OR.getCoords(self.model.camera,0)
                self.model.cursor.update(event.pos[0], event.pos[1])

            if organizer.state == "pong_game":
                self.model.objectCoordinatesRight, self.model.cameraImage = OR.getCoords(self.model.camera,0)
                self.model.rightPaddle.update(event.pos[1]-self.model.rightPaddle.height/2.0)
                self.model.leftPaddle.update(event.pos[0]-self.model.leftPaddle.height/2.0)


class PongObjectRecogController():
    """handles the input from the camera"""
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinatesRight, self.model.cameraImage = OR.getCoords(self.model.camera,0)
        self.model.cursor.update(self.model.objectCoordinatesRight[0],self.model.objectCoordinatesRight[1])

        self.model.objectCoordinatesLeft = OR.getCoords(self.model.camera,1)
        self.model.cursor.update(self.model.objectCoordinatesLeft[0],self.model.objectCoordinatesLeft[1])
        # If coordinates are -1, no object has been detected
        self.model.leftPaddle.update(self.model.objectCoordinatesLeft[1]-self.model.leftPaddle.height/2.0)
        self.model.rightPaddle.update(self.model.objectCoordinatesRight[1]-self.model.rightPaddle.height/2.0)


class Ball(pygame.sprite.Sprite):
    """this is the ball that bounces on the walls, the paddles and that you try to get in the goal of the other player
    x -- initial x coordinate of the ball
    y -- initial y coordinate of the ball
    radius -- radius of the ball
    """
    def __init__(self,x,y,radius):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.radius=radius
        #the movingDirection needs to be between 0-1
        self.movingDirection = [1,-1]

        self.image = pygame.Surface([2*self.radius,2*self.radius])
        self.image.fill([69,0,66])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def update(self,organizer):
        """after one loop has gone by, move the ball in the movingDirection of the movement
        This function uses Organizer.settings_ballSpeed to as the speed parameter. This ensures that it can be changed by the areaSurveillance method"""
        self.x=self.x + self.movingDirection[0]*organizer.settings_ballSpeed # To move, add movingDirection times the ball speed by the previous coordinate, movingDirection gets updated after a bounce
        self.rect.x = self.rect.x + self.movingDirection[0]*organizer.settings_ballSpeed
        self.y = self.y + self.movingDirection[1]*organizer.settings_ballSpeed
        self.rect.y = self.rect.y + self.movingDirection[1]*organizer.settings_ballSpeed

    def draw(self,screen):
        """draw the ball on its new position"""
        pygame.draw.circle(screen, (66, 134, 244), (self.x,self.y), self.radius)


class Boundary(pygame.sprite.Sprite):
    """This is the boundary
    x -- x coordinate of upper left corner
    y -- y coordinate of upper left corner
    height -- y lenght of rectangle
    width -- x lenght of rectangle
    """
    def __init__(self,x,y,height,width):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.height=height
        self.width = width

        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x+width/2,self.y+height/2]

    def draw(self,screen):
        """draws the boundaries of the game"""
        pygame.draw.rect(screen,pygame.Color(69, 244, 66),pygame.Rect(self.x,self.y,self.width,self.height))


class Paddle(Boundary):
    """This is the movable boundary -> a paddle
    x -- x coordinate of upper left corner
    y -- y coordinate of upper left corner
    height -- y lenght of rectangle
    width -- x lenght of rectangle
    It inherits from Boundary
    """
    def __init__(self, x, y,height, width):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        super(Paddle,self).__init__(x,y,height,width)

    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color(244, 65, 65),pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self,y):
         """maybe used to change position although the position is accessed by the handle_event"""
         self.y=y
         self.rect.y=y


class Score():
    """this is the score"""
    def __init__(self,model):
        self.player1 = 0
        self.player2 = 0
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True)
        self.model = model

    def draw(self,screen):
        """print score for now, needs to print the score on the screen"""
        score1 = self.numberfont.render(str(self.player1), 1, (255,255,255))
        screen.blit(score1, (100,100))
        score2 = self.numberfont.render(str(self.player2), 1, (255,255,255))
        screen.blit(score2, (self.model.width-100,100))

    def update(self,player):
        """counts the score"""
        if player == 0:
            self.player1 +=1
        if player == 1:
            self.player2 +=1
        if self.player1>4:
            self.model.organizer.state = "endgame"
            self.model.organizer.winner = 1
        if self.player2>4:
            self.model.organizer.state = "endgame"
            self.model.organizer.winner = 2

    def reset(self):
        self.player1 = 0
        self.player2 = 0


def Main(model,view,controller):
    """Update graphics and check for pygame events.
    model -- an object of the type ArPongModel()
    view -- an object of the type PlayboardWindowView()
    controller -- an object ArPongMouseController()
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            #controller.handle_event(event)
        controller.update()
        model.update()
        view.draw()
        clock.tick(fps)

if __name__ == '__main__':
    pygame.init()
    #the mixer is for the playing the music
    pygame.mixer.init()
    clock = pygame.time.Clock()
    fps = 60
    screenSize = [1850,1080]
    camera = OR.setup(screenSize)
    organizer = Organizer()
    #We start the game in the Organizer state
    organizer.state = "menu"
    #arguments are screenSize, the BoundaryOffset, BoundaryThickness, ballRadius, ballSpeed
    model = PongModel(screenSize,camera,organizer)
    view = PongView(model,screenSize, organizer)
    view._draw_background()
    #controller = PongMouseController(model)
    controller = PongObjectRecogController(model)
    Main(model,view,controller)
