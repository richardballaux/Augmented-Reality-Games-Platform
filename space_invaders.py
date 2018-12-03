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
dir_path = os.path.dirname(os.path.realpath(__file__))

class SpaceInvadersModel():
    """This is the model for the space invaders game"""
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
        self.enemyMoveLooper = 0

        self.enemyShootLooper = 0
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

        self.player = Player(900,900,dir_path+"/data/spaceship.png") #initialize the player with x and y coordinate and the path of the picture
        self.score = Score()
        self.health = Health()

        self.cursor = Cursor(0,0,20,self.organizer)
        #creating the buttons that this game will have
        self.startGameButton = CursorRecognition("Start",30, [500, 500, 200,200],self.organizer)
        self.homeScreenButton = CursorRecognition("Home Screen",30, [500,500, 300,150],self.organizer)
        self.restartButton = CursorRecognition("Restart",30, [500,700, 200,150],self.organizer)

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
            print(self.enemySpriteGroup.sprites())
            if len(self.enemySpriteGroup.sprites()) == 0: #all the enemy are deathSound
                self.organizer.win = True
                self.organizer.state = "endgame"

            elif self.health.healthLevel == 0:
                self.organizer.win = False
                self.organizer.state = "endgame"

        elif self.organizer.state == "menu": #this state is the first state when we enter this game
            #areaSurveillance over the start button of the game
            self.startGameButton.areaSurveillance(self.cursor, "game", self.organizer, "state", "game")

        elif self.organizer.state == "endgame": #this state occurs when the game ends
            self.homeScreenButton.areaSurveillance(self.cursor, "True", self, "backToHomeScreen", "True")
            self.restartButton.areaSurveillance(self.cursor, "menu",self.organizer, "state", "menu")
            #areaSurveillance over the "restart button" of the game
            #areaSurveillance over the "go back to homeScreen button"

    def playerShoot(self):
        """This makes the player shoot from its current position
        """
        #TODO : make a looper so the player can't shoot constantly
        playerbullet = Bullet(10,1,self.player.x,self.player.y)
        playerbullet.add(self.playerBulletSpriteGroup)

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
        if self.enemyShootLooper == 20:
            enemyList = self.enemySpriteGroup.sprites()
            randomEnemy = random.choice(enemyList)
            enemyBullet = Bullet(10,-1,randomEnemy.x,randomEnemy.y)
            enemyBullet.add(self.enemyBulletSpriteGroup)
            self.enemyShootLooper = 0
            pass
        else:
            self.enemyShootLooper +=1


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
            for bullet in self.model.enemyBulletSpriteGroup:
                bullet.draw(self.model.screen)
            for obstruction in self.model.obstructionSpriteGroup:
                obstruction.draw(self.model.screen)
            self.model.score.draw(self.model.screen)
            self.model.health.draw(self.model.screen)


        elif self.model.organizer.state == "menu":
            #draw instructions to play the Game
            #draw button to start the game
            #maybe also draw the highscore would be cool
            self.model.startGameButton.draw(self.model.screen)
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.ColorGreen)
            self.model.screen.blit(menutext, (50,50))
            instructions = self.myfont.render("Instructions: ", 1, self.ColorGreen)
            self.model.screen.blit(instructions, (100,100))
            self.model.cursor.draw(self.model.screen)


        elif self.model.organizer.state == "endgame":
            #draw the final score
            if self.model.organizer.win:
                menutext = self.myfont.render("Congratulations, YOU WON", 1, self.ColorGreen)
                self.model.screen.blit(menutext, (200,50))
                self.model.score(self.model.screen)
            else:
                menutext = self.myfont.render("Sad, YOU LOST", 1, self.ColorGreen)
                self.model.screen.blit(menutext, (200,50))
            #draw the two buttons
            self.model.homeScreenButton.draw(self.model.screen)
            self.model.restartButton.draw(self.model.screen)
            #draw the highscore of other people
        pygame.display.update()

    def draw_background(self,screen): # draw the camera image to the background
        self.model.screen.fill(self.ColorBlack)
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.model.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)

class SpaceInvadersController():
    """This is the controller for the spaceInvaders game"""
    def __init__(self,model):
        """The controller only needs access to the model
        """
        self.model = model

    def update(self):
        """This update function gets the coordinates from the objectrecognition object and processes it"""
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera,0) # Get the coords of controller '0'
        if self.model.organizer.state == "game":
                if self.model.objectCoordinates[0]<self.model.player.x:
                    self.model.player.direction = -1
                elif self.model.objectCoordinates[0]>self.model.player.x:
                    self.model.player.direction = 1

        elif self.model.organizer.state == "menu":
                self.model.cursor.update(self.model.objectCoordinates[0],self.model.objectCoordinates[1])

        for event in pygame.event.get():
            if event.type is pygame.MOUSEBUTTONDOWN:
                self.model.playerShoot()

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
        self.rect.center = [self.x,self.y]
        #self.killSound = pygame.mixer.Sound(dir_path+"/data/death.wav")

    def move(self):
        """moves the spaceship with one times the speed"""
        self.x = self.x+self.speed*self.direction

    def update(self):
        """update the player, for now this is only moving it"""
        self.move()

    def draw(self,screen):
        """draw image on the screen"""
        screen.blit(self.image,(self.x,self.y))

class Enemy(Player):
    """this is the class of all the enemies (3 different levels)"""
    def __init__(self,x,y,aliveImage,pointsWhenKilled):
        super(Enemy,self).__init__(x,y,aliveImage)
        #self.deathImage = pygame.transform.scale(pygame.image.load(dir_path+"/data/New Pixel.png"),(80,100))
        self.killSound = pygame.mixer.Sound(dir_path+"/data/death.wav")
        self.received_points_when_killed = pointsWhenKilled
        #is aliveImage the same as image

    def move(self,xMovement,yMovement):
        self.x = self.x +xMovement
        self.rect.x = self.rect.x + xMovement
        self.y = self.y +yMovement
        self.rect.y = self.rect.y + yMovement

    def die(self):
        pygame.mixer.Sound.play(self.killSound)
        self.kill()

class Bullet(pygame.sprite.Sprite):
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
        """draws the Bullet image to the screen"""
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

    def draw(self,screen):
        """draw the score to the screen"""
        textMaker = self.myfont.render(str(self.totalPoints),1,self.ColorBlack)
        screen.blit(textMaker,(1500,50))

class Health():
    def __init__(self):
        self.healthLevel = 3
        self.shieldImage = pygame.transform.scale(pygame.image.load(dir_path+"/data/shield.jpg"),(50,50))
        self.x = 20
        self.y=20
        self.myfont = pygame.font.SysFont("monospace", 42)

    def gotShot(self):
        self.healthLevel -= 1

    def draw(self,screen):
        textMaker = self.myfont.render("HEALTH: ", 1, (0,0,0))
        screen.blit(textMaker,(self.x,self.y))
        for i in range(self.healthLevel):
            screen.blit(self.shieldImage,(self.x + 200 + i*70 ,self.y))
