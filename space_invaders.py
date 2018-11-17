"""Space invaders file

This game need to have:
This is all based on this video:
https://www.youtube.com/watch?v=D1jZaIPeD5w
PIXELART generator :
https://www.piskelapp.com/p/agxzfnBpc2tlbC1hcHByEwsSBlBpc2tlbBiAgKDwzZSzCww/edit
"""
import os
import pygame
dir_path = os.path.dirname(os.path.realpath(__file__))

class SpaceInvadersModel():
    def __init__(self,screen,organizer):
        self.screen = screen
        self.organizer = organizer
        self.enemystartxcoord = 100
        self.distanceBetweenEnemiesx = 50
        self.enemystartycoord = 100
        self.distanceBetweenEnemiesy = 50
        self.enemies = []
        self.enemiesXposition = 0 #this keeps track of the current left or right movement of the enemies
        self.enemiesXMovement = 5 #this is the max number of horizontal movement
        self.enemiesYPosition = 0 #this keeps track of the current vertical movement of the enemies
        for i in range(10):
            enemy = EnemyLevel3(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord,dir_path+"/data/level3monster.png")
            list = []
            self.enemies[0].append(enemy)
        for i in range(10):
            enemy = EnemyLevel2(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord+distanceBetweenEnemiesy,dir_path+"/data/level2monster.png")
            self.enemies[1].append(enemy)
        for i in range(10):
            for j in range(2,3):
                enemy = EnemyLevel1(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord+distanceBetweenEnemiesy*j,dir_path+"/data/level1monster.png")
                self.enemies[i].append(enemy)

        self.obstructions = []
        for i in range(3):
            self.obstructions[i] = Obstruction(450*i,800)

        self.player = Player(900,900,dir_path+"/data/spaceship.png")
        self.score = Score()
        self.components = [self.enemies,self.obstructions,self.player,self.score] #TODO enemies doesn't have a .update()-function because it is a list.

    def update(self):
        if self.organizer.state == "game":
            self.player.update()
            for enemyRow in self.enemies:
                for enemy in enemyRow:
                    enemy.update()
            #check for all the collisions
        if self.organizer.state == "menu":
            #areaSurveillance over the start button of the game
            pass
        if self.organizer.state == "endgame":
            #areaSurveillance over the "restart button" of the game
            #areaSurveillance over the "go back to homeScreen button"
            pass

class SpaceInvadersView():
    def __init__(self,model):
        self.model = model

    def draw():
        self.draw_background(self.model.screen) #always draw the background first

        if self.organizer.state == "game":
            self.model.player.draw(self.model.screen)
            for enemyRow in self.model.enemies:
                for enemy in enemyRow:
                    enemy.draw(self.model.screen)
            for obstruction in self.model.obstructions:
                obstruction.draw(self.model.screen)
            for bullet in self.model.bulletCollisionGroup:
                bullet.draw(self.model.screen)
        if self.organizer.state == "menu":
            #draw instructions to play the Game
            #maybe also draw the highscore would be cool
            pass
        if self.organizer.state == "endgame":
            #draw the final score
            #draw the two buttons
            #draw the highscore of other people
            pass

    def draw_background(screen):
        self.screen.fill((0,0,0))
        newSurface = pygame.surfarray.make_surface(self.model.cameraImage) # Reads the stored camera image and makes a surface out of it
        self.screen.blit(newSurface,(0,0)) # Make background of the sufrace (so it becomes live video)
        pygame.display.update()

class SpaceInvadersController():
    def __init__(self):
        pass

class Player():
    """this is the class of the spaceship"""
    def __init__(self,x,y,image):
            self.speed = 10
            self.direction = -1 #negative or positive
            self.image = pygame.image.load(image) #"spaceship.png"
            self.x = x
            self.y =y
            self.rect = self.image.get_rect()
            self.rect.center = [self.x,self.y]
    def move(self,direction):
        """moves the spaceship with one times the speed"""
        self.x = self.x+self.speed

    def shoot(self):
        """shoot bullet from the place where it is at the moment"""
        #create bullet object and make it go upwards
        ## TODO: bullet
        bullet = Playerbullet(self.x,self.y,5)
        #add bullet to screen or list of stuff in the screen

    def update(self):
        self.move()

    def draw(self,screen):
        #draw image on the screen
        pass

class Enemy(Player):
    """this is the class of all the enemies (3 different levels)"""
    def __init__(self,x,y,aliveImage):
        super(Player,self).__init__(x,y,aliveImage)
        self.aliveImage = pygame.load(aliveImage)
        self.deathImage = pygame.load(dir_path+"/New Pixel.png")
        self.killSound = pygame.mixer.Sound(dir_path+"/death.wav")

    def update(self):
        #update the enemy
        #kill enemy if shot, give player score
        #move enemy
        pass
    def move(self):
        if self.enemiesXposition >= self.enemiesXMovement:
            self.x = self.x-25
        else:
            self.x = self.x+25
        if self.enemiesXposition == self.enemiesXMovement:
            self.y = self.y + 25


class EnemyLevel1(Enemy):
    def __init__(self, aliveImage):
        super(Enemy,self).__init__(aliveImage)
        self.received_points_when_killed = 5

class EnemyLevel2(Enemy):
    def __init__(self, aliveImage):
        super(Enemy,self).__init__(aliveImage)
        self.received_points_when_killed = 10

class EnemyLevel3(Enemy): # (this is the fast moving satelite at the top)
    def __init__(self, aliveImage):
        super(Enemy,self).__init__(aliveImage)
        self.received_points_when_killed = 15

class Bullet():
    def __init__(self,speed,direction,x,y):
        self.speed=speed
        self.direction = direction
        self.image = pygame.load("/data/bullet.jpg")
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.y = self.y +self.direction*self.speed
        self.rect.y = self.rect.y+self.direction*self.speed
    #-collision(with enemy or player    or     with other bullet)

    def update(self):
        self.move()

    def draw(self,screen):
        pygame.draw.rect(screen, (250,250,250), pygame.Rect(self.x,self.y,20,100))


class Playerbullet(Bullet):
    def __init__(self,x,y,speed):
        super(Bullet,self).__init__(speed,1,x,y)
        #direction is by default upwards

class EnemyBullet(Bullet):
    def __init__(self,speed):
        super(Bullet,self).__init__(speed,-1)
        #direction is downwards by default

class Obstruction():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.healthLevel = 5 #this goes down everytime the obstruction gets shot
        self.fullHealth = pygame.image.load()
        self.threequarterHealth = pygame.image.load()
        self.halfHealth = pygame.image.load()
        self.quarterHealth = pygame.image.load()
        self.noHealth = pygame.image.load()
        self.healthImages = [self.noHealth,self.quarterHealth,self.halfHealth,self.threequarterHealth,self.fullHealth]

    def update():
        # do nothing for now
        pass

    def draw(self,screen):
        #draw image: self.healthImages[healthLevel-1]
        pass

class Score():
    """this is the class that keeps track of the score"""

    def __init__(self):
        self.totalPoints = 0

    def update(self):
        #add the points from the killed enemies to the score
        pass

    def draw(self,screen):
        #draw a number to the screen
        pass

# class Organizer():
#     """
#     possible states of the organizer in space_invaders:
#     - menu
#     - game
#     - endgame
#     """
#     def __init__(self):
#         self.state = "menu"
