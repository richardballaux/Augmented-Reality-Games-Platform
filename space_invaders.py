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
import random
import time
dir_path = os.path.dirname(os.path.realpath(__file__))

class SpaceInvadersModel():
    """This is the model for the space invaders game
    - pygame screen object,
    - cv2.VideoCapture(0) object
    - In-game phaseKeeper of the Organizer class"""
    def __init__(self,screen,camera,organizer):
        self.camera = camera
        self.screen = screen
        self.organizer = organizer
        self.backToHomeScreen = False  #If this goes to True, the while loop in which this game runs breaks.
        self.enemystartxcoord = 50
        self.distanceBetweenEnemiesx = 150
        self.enemystartycoord = 100
        self.distanceBetweenEnemiesy = 150
        #initialization of the sprite groups. These will contain all the sprite so they can generate collisions
        self.enemySpriteGroup = pygame.sprite.Group()
        self.enemyBulletSpriteGroup = pygame.sprite.Group()
        self.playerBulletSpriteGroup = pygame.sprite.Group()
        self.obstructionSpriteGroup = pygame.sprite.Group()
        #initialize all the variables we need for moving the enemies of the screen look at the moveEnemies-function for more info
        self.enemiesXposition = 0 #this keeps track of the current left or right movement of the enemies
        self.enemiesXMovement = 5 #this is the max number of horizontal movement
        self.moveRight = True
        self.enemyMoveLooper = 0 #this variable keep track of the current number of loops between every enemy movement

        self.enemyShootLooper = 0 #this variable keep track of the current number of loops until an enemy shoots again
        self.enemyShootMinimumLooper = 20 #this variable is the minimum amount of loops between enemy shots. this is dependent of the number of enemies left.

        self.generateEnemiesAndObstructions() #in this function all the enemies and obstructions are generated. We do it this way to be able to reuse is when a user wants to restart the game

        self.haveToResetGame = False

        self.player = Player(900,900,dir_path+"/data/spaceship.png") #initialize the player with x and y coordinate and the path of the picture
        self.enemyShootSound = pygame.mixer.Sound(dir_path +"/data/shoot.wav")
        self.playerShootSound = pygame.mixer.Sound(dir_path +"/data/playerShoot.wav")
        self.lastTimeShot = 0 #this variable remembers at what time the player shot last
        self.timeBetweenShots = 1 # this variable is the minimum time in ..... between shots
        self.score = Score()
        self.health = Health()

        self.cursor = Cursor(0,0,20,self.organizer)
        self.drawCursor = False
        #creating the buttons that this game will have
        self.startGameButton = CursorRecognition("Start",30, [500, 500, 200,200],self.organizer)
        self.homeScreenButton = CursorRecognition("Home Screen",30, [900,500, 350,150],self.organizer)
        self.restartButton = CursorRecognition("Restart",30, [500,500, 250,150],self.organizer)
        self.stopGameButton = CursorRecognition("STOP",30,[925,50,150,75],self.organizer)

    def update(self):
        """This update function is divide for the different states of the organizer
        inside the different states different components have to be updated
        """
        if self.organizer.state == "game":
            #Inside the "game"-state we update all the components the game has:
            # - the player
            # - the bullets that are in the enemyBulletSpriteGroup and in the playerBulletSpriteGroup
            # - the Obstructions that are in their obstructionSpriteGroup
            # - the enemies in their enemySpriteGroup
            self.stopGameButton.areaSurveillance(self.cursor,"menu",self.organizer,"state","menu")
            self.player.update()
            for bullet in self.playerBulletSpriteGroup:
                bullet.update()
            for obstr in self.obstructionSpriteGroup:
                obstr.update()
            self.moveEnemies()
            self.enemyShoot()
            for bullet in self.enemyBulletSpriteGroup:
                bullet.update()


            #In this sectin we look for collisions between the spriteGroups
            #These collision-functions return a dictionary.
            #The values of the dictionary are lists containing all the colliding sprites from the seconds spritegroup you enter in the function
            bulletbulletCollideDict = pygame.sprite.groupcollide(self.enemyBulletSpriteGroup,self.playerBulletSpriteGroup,True,True)
            bulletAndEnemyCollideDict = pygame.sprite.groupcollide(self.playerBulletSpriteGroup,self.enemySpriteGroup,True,False)
            for element in bulletAndEnemyCollideDict:
                self.score.add(bulletAndEnemyCollideDict[element][0].received_points_when_killed)
                bulletAndEnemyCollideDict[element][0].die()
            # TODO: change the picture of the enemy to dead for some amount of loops
            bulletAndObstructionCollideDict = pygame.sprite.groupcollide(self.enemyBulletSpriteGroup,self.obstructionSpriteGroup,True,False)
            for element in bulletAndObstructionCollideDict:
                bulletAndObstructionCollideDict[element][0].shot()
            playerBulletAndObstructionCollideDict = pygame.sprite.groupcollide(self.playerBulletSpriteGroup,self.obstructionSpriteGroup,True,False)
            for element in playerBulletAndObstructionCollideDict:
                playerBulletAndObstructionCollideDict[element][0].shot()
            bulletAndPlayerCollideList = pygame.sprite.spritecollide(self.player,self.enemyBulletSpriteGroup,True)
            if len(bulletAndPlayerCollideList)>0:
                self.health.gotShot()

            #Transitions to the next state:--------------------------------------------------
            if len(self.enemySpriteGroup.sprites()) == 0: #all the enemy are dead
                self.player.win()
                self.organizer.win = True
                self.organizer.state = "endgame"

            elif self.health.healthLevel == 0:
                self.player.die()
                self.organizer.win = False
                self.organizer.state = "endgame"

        elif self.organizer.state == "menu": #this state is the first state when we enter this game
            #areaSurveillance over the start button of the game
            self.startGameButton.areaSurveillance(self.cursor, "game", self, "haveToResetGame", True)
            if self.haveToResetGame:
                self.resetGame()
                self.haveToResetGame = False
            self.homeScreenButton.areaSurveillance(self.cursor,"menu",self,"backToHomeScreen",True)

        elif self.organizer.state == "endgame": #this state occurs when the game is done
            self.homeScreenButton.areaSurveillance(self.cursor, "menu", self, "backToHomeScreen", True)
            self.restartButton.areaSurveillance(self.cursor, "menu",self.organizer, "state", "menu")
            #areaSurveillance over the "restart button" of the game
            #areaSurveillance over the "go back to homeScreen button"

    def playerShoot(self):
        """This makes the player shoot from its current position
        """
        if (time.time() - self.lastTimeShot)>= self.timeBetweenShots:
            playerbullet = Bullet(10,1,self.player.x,self.player.y)
            playerbullet.add(self.playerBulletSpriteGroup)
            pygame.mixer.Sound.play(self.playerShootSound)
            self.lastTimeShot = time.time()

    def moveEnemies(self):
        """this function makes the enemies move across the screen starting from left to right and then down
        The enemies are only moved once every 10 loops. So the first thing the function does is checking if the looper is 10.
        If so then it moves the enemies. If not then it increments the looper by one.
        So the enemies move left and right for 5 steps (self.enemiesXMovement) of 10 pixels each.
        """
        if self.enemyMoveLooper == 10:
            if self.moveRight:
                self.enemiesXposition +=1
                for enemy in self.enemySpriteGroup:
                    enemy.move(10,0)
            else:
                self.enemiesXposition -=1
                for enemy in self.enemySpriteGroup:
                    enemy.move(-10,0)

            if self.enemiesXposition>self.enemiesXMovement:
                self.moveRight = False
            if self.enemiesXposition ==0:
                self.moveRight = True

            if self.enemiesXposition == self.enemiesXMovement:
                for enemy in self.enemySpriteGroup:
                    enemy.move(0,1)

            self.enemyMoveLooper=0
        else:
            self.enemyMoveLooper +=1

    def enemyShoot(self):
        """Makes the enemies shoot after once every so many loops"""
        if self.enemyShootLooper == self.enemyShootMinimumLooper:
            enemyList = self.enemySpriteGroup.sprites()
            randomEnemy = random.choice(enemyList)
            enemyBullet = Bullet(10,-1,randomEnemy.x,randomEnemy.y)
            enemyBullet.add(self.enemyBulletSpriteGroup)
            #make the frequency of enemy shooting dependent of number of enemies
            self.enemyShootMinimumLooper = 60-len(enemyList)
            self.enemyShootLooper = 0 #if one of the enemies shot, set the enemyShootLooper back to zero
            pygame.mixer.Sound.play(self.enemyShootSound)

        else:
            self.enemyShootLooper +=1 # if none of the enemies didn't shoot this loop, increment the enemyShootLooper

    def generateEnemiesAndObstructions(self):
        """This function generates all the enemies and obstructions and puts them into their respective spriteGroups"""
        #initialization of all the enemies and adding them to their respective spriteGroups
        for i in range(10):
            enemy = Enemy(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord,dir_path+"/data/level3monster.png",15)
            self.enemySpriteGroup.add(enemy)
        for i in range(10):
            enemy = Enemy(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord+self.distanceBetweenEnemiesy,dir_path+"/data/level2monster.png",10)
            self.enemySpriteGroup.add(enemy)
        for i in range(10):
            for j in range(2,4):
                enemy = Enemy(self.enemystartxcoord+self.distanceBetweenEnemiesx*i,self.enemystartycoord+self.distanceBetweenEnemiesy*j,dir_path+"/data/level1monster.png",5)
                self.enemySpriteGroup.add(enemy)
        #initialization of the obstructinos at there fixed spot and adding them to the obstructionSpriteGroup
        for i in range(3):
            obstruction = Obstruction(300+500*i,700)
            self.obstructionSpriteGroup.add(obstruction)

    def resetGame(self):
        """This function resets the whole game back to zero"""
        #first make all the spriteGroups empty before refilling them again.
        self.enemySpriteGroup.empty()
        self.enemyBulletSpriteGroup.empty()
        self.obstructionSpriteGroup.empty()
        self.playerBulletSpriteGroup.empty()
        self.generateEnemiesAndObstructions()
        self.score.reset()
        self.health.reset()

class SpaceInvadersView():
    """This is the view class for the space invaders game
    model --    object of the SpaceInvadersModel class"""
    def __init__(self,model):
        self.model = model
        self.myfont = pygame.font.SysFont("monospace", 42) #Font that is used in states "game" and "select_speed" to prompt the user
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.ColorGreen = (0,250,0)
        self.ColorBlack = (0,0,0)
        self.ColorRed = (165, 0, 0)

    def draw(self):
        """draws the corresponding state of the spaceInvadersPhaseKeeper of the game to the screen"""
        self.draw_background(self.model.screen) #always draw the background first

        if self.model.organizer.state == "game":
            self.model.stopGameButton.draw(self.model.screen)
            pygame.draw.rect(self.model.screen,pygame.Color(135, 0, 0),pygame.Rect(30,700,1800,2)) #the user has to go above this line to shoot
            self.model.player.draw(self.model.screen)
            for enemy in self.model.enemySpriteGroup:
                enemy.draw(self.model.screen)
            for bullet in self.model.playerBulletSpriteGroup:
                bullet.draw(self.model.screen)
            for bullet in self.model.enemyBulletSpriteGroup:
                bullet.draw(self.model.screen)
            for obstruction in self.model.obstructionSpriteGroup:
                obstruction.draw(self.model.screen)
            self.model.score.draw(self.model.screen)
            self.model.health.draw(self.model.screen)
            if self.model.drawCursor: #only draw the cursor when he is above a certain line to get to the stop button
                self.model.cursor.draw(self.model.screen)


        elif self.model.organizer.state == "menu":
            #draw instructions to play the Game
            #draw button to start the game
            #maybe also draw the highscore would be cool
            self.model.startGameButton.draw(self.model.screen)
            self.model.homeScreenButton.draw(self.model.screen)
            pygame.draw.rect(self.model.screen,pygame.Color(0, 0, 0),pygame.Rect(30,30,1800,300)) #the user has to go above this line to shoot
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.ColorGreen)
            self.model.screen.blit(menutext, (50,50))
            instructions = self.myfont.render("Instructions: ", 1, self.ColorGreen)
            self.model.screen.blit(instructions, (50,100))
            moreInstructions = self.myfont.render("Move your controller left and right to move your spaceship.", 1, self.ColorRed)
            self.model.screen.blit(moreInstructions, (50,150))
            evenMoreInstructions = self.myfont.render("To shoot hold your controller above the dark red line.", 1, self.ColorRed)
            self.model.screen.blit(evenMoreInstructions, (50,200))
            goodLuck = self.myfont.render("Try not to shoot your own obstructions   GOOD LUCK", 1, self.ColorRed)
            self.model.screen.blit(goodLuck, (50,250))
            self.model.cursor.draw(self.model.screen)


        elif self.model.organizer.state == "endgame":
            #draw the final score
            if self.model.organizer.win:
                menutext = self.myfont.render("Congratulations, YOU WON", 1, self.ColorGreen)
                self.model.screen.blit(menutext, (200,50))
                self.model.score.draw(self.model.screen)
            else:
                menutext = self.myfont.render("Sad, YOU LOST", 1, self.ColorRed)
                self.model.screen.blit(menutext, (900,350))
            #draw the two buttons
            self.model.homeScreenButton.draw(self.model.screen)
            self.model.restartButton.draw(self.model.screen)
            self.model.cursor.draw(self.model.screen)
            #draw the highscore of other people
        pygame.display.update()

    def draw_background(self,screen): # draw the camera image to the background
        self.model.screen.fill(self.ColorBlack)
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)

class SpaceInvadersController():
    """This is the controller for the spaceInvaders game
    model --    object of the SpaceInvadersModel class"""
    def __init__(self,model):
        self.model = model

    def update(self):
        """This update function gets the coordinates from the objectrecognition object and processes it"""
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0) # Get the coords of controller '0'
        if self.model.organizer.state == "game":
            if self.model.objectCoordinates[0]<self.model.player.x:
                self.model.player.direction = -1
            elif self.model.objectCoordinates[0]>self.model.player.x:
                self.model.player.direction = 1

            if self.model.objectCoordinates[1]<80:
                self.model.cursor.update(self.model.objectCoordinates[0],self.model.objectCoordinates[1])
                self.model.drawCursor = True
            else:
                self.model.drawCursor = False

            if self.model.objectCoordinates[1]<650:
                self.model.playerShoot()


        elif self.model.organizer.state == "menu":
            self.model.cursor.update(self.model.objectCoordinates[0],self.model.objectCoordinates[1])

        elif self.model.organizer.state =="endgame":
            self.model.cursor.update(self.model.objectCoordinates[0],self.model.objectCoordinates[1])

class Player(pygame.sprite.Sprite):
    """this is the class of the spaceship
    x --    (integer) starting x position of the spaceship
    y --    (integer) starting y position of the spaceship
    image --    (string) path of the spaceship image"""
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.direction = -1 #negative or positive
        self.image = pygame.transform.scale(pygame.image.load(image),(100,120)) #"spaceship.png"
        self.playerDieSound = pygame.mixer.Sound(dir_path+"/data/playerDie.wav")
        self.playerWinSound = pygame.mixer.Sound(dir_path+"/data/playerWin.wav")
        self.x = x
        self.y =y
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]
        #self.killSound = pygame.mixer.Sound(dir_path+"/data/death.wav")

    def move(self):
        """moves the spaceship with one times the speed"""
        self.x = self.x + self.speed * self.direction
        self.rect.x = self.rect.x + self.speed*self.direction

    def update(self):
        """update the player"""
        self.move()

    def draw(self,screen):
        """draw image on the screen
        screen --   pygame screen object"""
        screen.blit(self.image,(self.x,self.y))

    def die(self):
        """This function plays the die sound of the player"""
        pygame.mixer.Sound.play(self.playerDieSound)

    def win(self):
        """This function plays the win sound of the player"""
        pygame.mixer.Sound.play(self.playerWinSound)

class Enemy(Player):
    """this is the class of all the enemies (3 different levels)
    x --    (integer) starting x position of the enemy
    y --    (integer) starting y position of the enemy
    aliveImage --   (string) path of the alive image of the enemy
    pointsWhenKilled -- (integer) points the player gets when he kills this enemy"""
    def __init__(self,x,y,aliveImage,pointsWhenKilled):
        super(Enemy,self).__init__(x,y,aliveImage)
        #self.deathImage = pygame.transform.scale(pygame.image.load(dir_path+"/data/New Pixel.png"),(80,100))
        self.killSound = pygame.mixer.Sound(dir_path+"/data/death.wav")
        self.received_points_when_killed = pointsWhenKilled
        #is aliveImage the same as image

    def move(self,xMovement,yMovement):
        """moves the enemy with a given x and y distance
        - xMovement --  integer to move enemy in x direction
        - yMovement --  integer to move enemy in y direction
        """
        self.x = self.x +xMovement
        self.rect.x = self.rect.x + xMovement
        self.y = self.y +yMovement
        self.rect.y = self.rect.y + yMovement

    def die(self):
        """This function is called when the enemy dies"""
        pygame.mixer.Sound.play(self.killSound)
        self.kill()

class Bullet(pygame.sprite.Sprite):
    """This is the Bullet class
    - speed --  integer, this defines the speed in pixels per loop
    - direction -- -1 for downward movement 1 for upward movement
    - x --  starting x position in pixels
    - y --  starting y position in pixels
    """
    def __init__(self,speed,direction,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load(dir_path+"/data/bullet.jpg"),(50,70))
        self.x = x
        self.y = y
        self.rect =self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def move(self):
        """move the bullet and if the bullet moves out of the screen it kills itself"""
        self.y = self.y -self.direction*self.speed
        self.rect.y = self.rect.y-self.direction*self.speed
        if self.y ==0 or self.y==1080:
            self.kill()

    def update(self):
        self.move()

    def draw(self,screen):
        """draws the Bullet image to the screen dependent on the direction draws it facing upward or downward"""
        if self.direction == -1:
            screen.blit(pygame.transform.rotate(self.image,180),(self.x,self.y))
        else:
            screen.blit(self.image,(self.x,self.y))

class Obstruction(pygame.sprite.Sprite):
    """this is the obstuction class
    - x --   x position of the obstruction
    - y --   y position of the obstuction
    """
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
        """This function updates the Obstruction object
        it changes the "image" to the current healthLevel and resets the rect to keep the collision accurate
        """
        self.image = self.healthImages[self.healthLevel]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]

    def shot(self):
        """This function is called when the obstruction gets hit by any bullet"""
        self.healthLevel = self.healthLevel - 1
        if self.healthLevel == 0:
            self.kill()

    def draw(self,screen):
        """draw the current image (corresponding with the healthLevel) to the screen"""
        screen.blit(self.healthImages[self.healthLevel],(self.x,self.y))


class Score():
    """this is the class that keeps track of the score"""
    def __init__(self):
        self.totalPoints = 0
        self.myfont = pygame.font.SysFont("monospace", 42,bold = True) #Font that is used in states "game" and "select_speed" to prompt the user
        self.ColorBlack = (0,0,0)

    def add(self,pointsToAdd):
        """add points from a killed enemy to the score"""
        self.totalPoints += pointsToAdd

    def reset(self):
        """This function resets the score back to zero"""
        self.totalPoints = 0

    def draw(self,screen):
        """draw the score to the screen"""
        textMaker = self.myfont.render(str(self.totalPoints),1,self.ColorBlack)
        screen.blit(textMaker,(1500,50))

class Health():
    """This is the health class, this keeps track of the shields the player still has and draws the according amount to the screen"""
    def __init__(self):
        self.healthLevel = 3
        self.shieldImage = pygame.transform.scale(pygame.image.load(dir_path+"/data/shield.jpg"),(50,50))
        self.x = 20
        self.y=20
        self.myfont = pygame.font.SysFont("monospace", 42)
        self.playerLoosesShieldSound = pygame.mixer.Sound(dir_path+"/data/playerLoosesLife.wav")


    def gotShot(self):
        """This function is called when the player gets shot by an enemy and as a result loses a shield"""
        self.healthLevel -= 1
        pygame.mixer.Sound.play(self.playerLoosesShieldSound)

    def reset(self):
        """This function resets the healt back to three"""
        self.healthLevel = 3

    def draw(self,screen):
        """This function draws the shield of the player to the screen. This is dependent on the number shield he still has left"""
        textMaker = self.myfont.render("HEALTH: ", 1, (0,0,0))
        screen.blit(textMaker,(self.x,self.y))
        for i in range(self.healthLevel):
            screen.blit(self.shieldImage,(self.x + 200 + i*70 ,self.y))
