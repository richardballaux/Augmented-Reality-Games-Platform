"""Space invaders file

This is all based on this video:
https://www.youtube.com/watch?v=D1jZaIPeD5w
PIXELART generator :
https://www.piskelapp.com/p/agxzfnBpc2tlbC1hcHByEwsSBlBpc2tlbBiAgKDwzZSzCww/edit
"""
import os
import pygame
from cursor import Cursor, CursorRecognition
import ObjectRecogImplementation as OR
dir_path = os.path.dirname(os.path.realpath(__file__))

class SpaceInvadersModel():
    """This is the model for the space invaders game"""
    def __init__(self,screen,camera,organizer):
        self.camera = camera
        self.screen = screen
        self.organizer = organizer
        self.backToHomeScreen = False  #If this goes to True, the while loop in which this game runs breaks.
        self.enemystartxcoord = 100
        self.distanceBetweenEnemiesx = 200
        self.enemystartycoord = 100
        self.distanceBetweenEnemiesy = 150
        #initialization of the sprite groups. These will contain all the sprite so they can generate collisions
        self.enemySpriteGroup = pygame.sprite.Group()
        self.enemyBulletSpriteGroup = pygame.sprite.Group()
        self.playerBulletSpriteGroup = pygame.sprite.Group()
        self.obstructionSpriteGroup = pygame.sprite.Group()
        self.enemiesXposition = 0 #this keeps track of the current left or right movement of the enemies
        self.enemiesXMovement = 5 #this is the max number of horizontal movement
        self.enemiesYPosition = 0 #this keeps track of the current vertical movement of the enemies
        #initialization of all the enemies and adding them to their respective spriteGroups
        for i in range(10):
            enemy = EnemyLevel3(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord,dir_path+"/data/level3monster.png")
            self.enemySpriteGroup.add(enemy)
        for i in range(10):
            enemy = EnemyLevel2(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord+self.distanceBetweenEnemiesy,dir_path+"/data/level2monster.png")
            self.enemySpriteGroup.add(enemy)
        for i in range(10):
            for j in range(2,4):
                enemy = EnemyLevel1(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord+self.distanceBetweenEnemiesy*j,dir_path+"/data/level1monster.png")
                self.enemySpriteGroup.add(enemy)
        for i in range(3):
            obstruction = Obstruction(300+500*i,700)
            self.obstructionSpriteGroup.add(obstruction)

        self.player = Player(900,900,dir_path+"/data/spaceship.png")
        self.score = Score()

        self.cursor = Cursor(0,0,20,self.organizer)
        #creating the buttons that this game will have
        self.startGameButton = CursorRecognition("Start",30, [500, 500, 200,200],self.organizer)
        self.homeScreenButton = CursorRecognition("Home Screen",30, [500,500, 500,150],self.organizer)
        self.restartButton = CursorRecognition("Restart",30, [500,700, 150,150],self.organizer) # Triggers square to repeat the game in state "endgame"

    def update(self):
        """update all the components of the model:
        - player
        - all the enemies
        - all the obstructions
        - the score
        """
        if self.organizer.state == "game":
            self.player.update()
            for bullet in self.playerBulletSpriteGroup:
                bullet.update()
            for obstr in self.obstructionSpriteGroup:
                obstr.update()
            for enemy in self.enemySpriteGroup:
                enemy.move(self.enemiesXMovement,self.enemiesXposition)

            bulletbulletCollideDict = pygame.sprite.groupcollide(self.enemyBulletSpriteGroup,self.playerBulletSpriteGroup,True,True)
            bulletAndEnemyCollideDict = pygame.sprite.groupcollide(self.playerBulletSpriteGroup,self.enemySpriteGroup,True,True)
            for element in bulletAndEnemyCollideDict:
                self.score.add(bulletAndEnemyCollideDict[element][0].received_points_when_killed)
            # TODO: change the picture of the enemy to dead for some amount of loops
            bulletAndObstructionCollideDict = pygame.sprite.groupcollide(self.enemyBulletSpriteGroup,self.obstructionSpriteGroup,True,False)
            for element in bulletAndObstructionCollideDict:
                bulletAndObstructionCollideDict[element][0].shot()
            playerBulletAndObstructionCollideDict = pygame.sprite.groupcollide(self.playerBulletSpriteGroup,self.obstructionSpriteGroup,True,False)
            for element in playerBulletAndObstructionCollideDict:
                playerBulletAndObstructionCollideDict[element][0].shot()
            bulletAndPlayerCollideDict = pygame.sprite.spritecollide(self.player,self.enemyBulletSpriteGroup,True)
            # TODO: substact lives from the player

        if self.organizer.state == "menu": #this state is the first state when we enter this game
            #areaSurveillance over the start button of the game
            self.startGameButton.areaSurveillance(self.cursor, "game", self.organizer, "state", "game")

        if self.organizer.state == "endgame":
            self.homeScreenButton.areaSurveillance(self.cursor, "True", self, "backToHomeScreen", "True")
            self.restartButton.areaSurveillance(self.cursor, "menu",self.organizer, "state", "menu")
            #areaSurveillance over the "restart button" of the game
            #areaSurveillance over the "go back to homeScreen button"

    def playerShoot(self):
        playerbullet = Bullet(10,1,self.player.x,self.player.y)
        playerbullet.add(self.playerBulletSpriteGroup)


class SpaceInvadersView():
    """This is the view class for the space invaders game"""
    def __init__(self,model):
        self.model = model
        self.myfont = pygame.font.SysFont("monospace", 42) #Font that is used in states "game" and "select_speed" to prompt the user
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.ColorGreen = (0,250,0)
        self.ColorBlack = (0,0,0)

    def draw(self):
        """draws the corresponding state of the spaceInvadersPhaseKeeper of the game to the screen"""
        self.draw_background(self.model.screen) #always draw the background first

        if self.model.organizer.state == "game":
            self.model.player.draw(self.model.screen)
            for enemy in self.model.enemySpriteGroup:
                enemy.draw(self.model.screen)
            for bullet in self.model.playerBulletSpriteGroup:
                bullet.draw(self.model.screen)
            for obstruction in self.model.obstructionSpriteGroup:
                obstruction.draw(self.model.screen)
            self.model.score.draw(self.model.screen)


        if self.model.organizer.state == "menu":
            #draw instructions to play the Game
            #draw button to start the game
            #maybe also draw the highscore would be cool
            self.model.startGameButton.draw(self.model.screen)
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.ColorGreen)
            self.model.screen.blit(menutext, (50,50))
            instructions = self.myfont.render("Instructions: ", 1, self.ColorGreen)
            self.model.screen.blit(instructions, (100,100))
            self.model.cursor.draw(self.model.screen)


        if self.model.organizer.state == "endgame":
            #draw the final score

            #draw the two buttons
            self.model.homeScreenButton.draw(self.model.screen)
            restartButtonText = self.myfont.render("Restart", 1, self.ColorBlack)
            self.model.screen.blit(restartButtonText, (500,700))

            self.model.restartButton.draw(self.model.screen)
            backButtonText = self.myfont.render("Back to Home Screen", 1, self.ColorBlack) # Message for menu to select speed
            self.model.screen.blit(backButtonText,(500,500))
            #draw the highscore of other people

        pygame.display.update()

    def draw_background(self,screen): # draw the camera image to the background
        self.model.screen.fill(self.ColorBlack)
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)
        pygame.display.update()

class SpaceInvadersController():
    """This is the controller for the spaceInvaders game"""
    def __init__(self,model):
        #from the camera we need the x coordinate for the player and another way to know when the player shoots bullet
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0) # Get the coords of controller '0'
        if self.model.organizer.state == "game":
            if self.model.objectCoordinates[1][0]== -1:
                if self.model.objectCoordinates[0][0]<self.model.player.x:
                    self.model.player.direction = -1
                elif self.model.objectCoordinates[0][0]>self.model.player.x:
                    self.model.player.direction = 1
            else:
                if self.model.objectCoordinates[1][0]<self.model.player.x:
                    self.model.player.direction = -1
                elif self.model.objectCoordinates[0][0]>self.model.player.x:
                    self.model.player.direction = 1
            for event in pygame.event.get():
                if event.type is pygame.MOUSEBUTTONDOWN:
                    self.model.playerShoot()

        if self.model.organizer.state == "menu":
            if self.model.objectCoordinates[1][0]== -1:
                self.model.cursor.update(self.model.objectCoordinates[0][0],self.model.objectCoordinates[0][1])
            else: #if the first controller has -1 as values, the controller is changed two the controller on the right side of the screen
                self.model.cursor.update(self.model.objectCoordinates[1][0],self.model.objectCoordinates[1][1])
            # If coordinates are -1, no object has been detected
        if self.model.organizer.state == "endgame":
            self.homeScreenButton.draw(self.model.screen)
            self.restartButton.draw(self.model.screen)


class Player(pygame.sprite.Sprite):
    """this is the class of the spaceship"""
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.direction = -1 #negative or positive
        self.image = pygame.transform.scale(pygame.image.load(image),(100,120)) #"spaceship.png"
        self.x = x
        self.y =y
        self.rect = self.image.get_rect()
        self.rect.center = [self.x+50,self.y+60]
    def move(self):
        """moves the spaceship with one times the speed"""
        self.x = self.x+self.speed*self.direction

    def update(self):
        self.move()

    def draw(self,screen):
        """draw image on the screen"""
        screen.blit(self.image,(self.x,self.y))

class Enemy(Player):
    """this is the class of all the enemies (3 different levels)"""
    def __init__(self,x,y,aliveImage):
        self.deathImage = pygame.transform.scale(pygame.image.load(dir_path+"/data/New Pixel.png"),(80,100))
        self.killSound = pygame.mixer.Sound(dir_path+"/data/death.wav")
        super(Player,self).__init__(x,y,aliveImage)
        #is aliveImage the same as image


    def update(self):
        self.move()

    def move(self,enemiesXMovement,enemiesXposition):
        # TODO: give the following attributes of the model to the enemy
        if enemiesXposition >= enemiesXMovement:
            self.x = self.x-25
            self.rect.x = self.x-25
        else:
            self.x = self.x+25
            self.rect.x = self.rect.x+25
        if enemiesXposition == enemiesXMovement:
            self.y = self.y + 25
            self.rect.y = self.rect.y + 25

    def die(self):
        #play deathSound
        #remove the enemy from the spriteGroup
        pass

class EnemyLevel1(Enemy):
    def __init__(self,x,y, aliveImage):
        super(Enemy,self).__init__(x,y,aliveImage)
        self.received_points_when_killed = 5

class EnemyLevel2(Enemy):
    def __init__(self,x,y, aliveImage):
        super(Enemy,self).__init__(x,y,aliveImage)
        self.received_points_when_killed = 10

class EnemyLevel3(Enemy): # (this is the fast moving satelite at the top) not for now
    def __init__(self,x,y, aliveImage):
        super(Enemy,self).__init__(x,y,aliveImage)
        self.received_points_when_killed = 15

class Bullet(pygame.sprite.Sprite):
    def __init__(self,speed,direction,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load(dir_path+"/data/bullet.jpg"),(60,80))
        self.x = x
        self.y = y
        self.rect =self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def move(self):
        self.y = self.y -self.direction*self.speed
        self.rect.y = self.rect.y-self.direction*self.speed
        if self.y ==0:
            self.kill()
    #-collision(with enemy or player    or  with other bullet)

    def update(self):
        self.move()

    def draw(self,screen):
        if self.direction == -1:
            screen.blit(pygame.transform.rotate(self.image,180),(self.x,self.y))
        else:
            screen.blit(self.image,(self.x,self.y))

class Obstruction(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.healthLevel = 4 #this goes down everytime the obstruction gets shot
        self.fullHealth = pygame.transform.scale(pygame.image.load(dir_path+"/data/fullHealthObstruction.png"),(150,250))
        self.fourHealth = pygame.transform.scale(pygame.image.load(dir_path+"/data/4HealthObstruction.png"),(150,250))
        self.threeHealth = pygame.transform.scale(pygame.image.load(dir_path+"/data/3HealthObstruction.png"),(150,250))
        self.twoHealth = pygame.transform.scale(pygame.image.load(dir_path+"/data/2HealthObstruction.png"),(150,250))
        self.oneHealth = pygame.transform.scale(pygame.image.load(dir_path+"/data/1HealthObstruction.png"),(150,250))
        self.healthImages = [self.oneHealth,self.twoHealth,self.threeHealth,self.fourHealth,self.fullHealth]
        self.image = self.healthImages[self.healthLevel]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def update(self):
        self.image = self.healthImages[self.healthLevel]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def shot(self):
        self.healthLevel = self.healthLevel - 1
        if self.healthLevel == 0:
            self.kill()

    def draw(self,screen):
        screen.blit(self.healthImages[self.healthLevel],(self.x,self.y))


class Score():
    """this is the class that keeps track of the score"""

    def __init__(self):
        self.totalPoints = 0
        self.myfont = pygame.font.SysFont("monospace", 42,bold = True) #Font that is used in states "game" and "select_speed" to prompt the user
        self.ColorBlack = (0,0,0)

    def add(self,pointsToAdd):
        self.totalPoints += pointsToAdd

    def draw(self,screen):
        textMaker = self.myfont.render(str(self.totalPoints),1,self.ColorBlack)
        screen.blit(textMaker,(1500,50))
