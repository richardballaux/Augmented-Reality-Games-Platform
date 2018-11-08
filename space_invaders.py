"""Space invaders file

This game need to have:
This is all based on this video:
https://www.youtube.com/watch?v=D1jZaIPeD5w
PIXELART generator :
https://www.piskelapp.com/p/agxzfnBpc2tlbC1hcHByEwsSBlBpc2tlbBiAgKDwzZSzCww/edit
"""

dir_path = os.path.dirname(os.path.realpath(__file__))

class Player:
"""this is the class of the spaceship"""
    # TODOcounter between shooting times (can only shoot once every 2 seconds for instance)

    def __init__(self,image):
            self.speed = 10
            self.direction = -1 #negative or positive
            self.image = pygame.image.load(image) #"spaceship.png"
            self.x = 10
            self.y =10
    def move(self,direction):
        """moves the spaceship with one times the speed"""
        self.x = self.x+self.speed

    def shoot(self):
        """shoot bullet from the place where it is at the moment"""
        #create bullet object and make it go upwards
        ## TODO: bullet
        bullet = Playerbullet(self.x,self.y,5)
        #add bullet to screen or list of stuff in the screen

class Enemy(Player):
    """this is the class of all the enemies (3 different levels)"""
    def __init__(self,aliveImage):
        super(Player,self).__init__(aliveImage)
        self.aliveImage = pygame.load(aliveImage)
        self.deathImage = pygame.load(deathImage)
        self.killSound = pygame.mixer.Sound(dir_path+"/death.wav")

    def update(self):
        #update the enemy
    def move(self):


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
    def move(self):
        self.y = self.y +self.direction*self.speed
    #-collision(with enemy or player    or     with other bullet)
    def update(self):
        self.move()

class Playerbullet(Bullet):
    def __init__(self,x,y,speed):
        super(Bullet,self).__init__(speed,1,x,y)
        #direction is by default upwards

class EnemyBullet(bullet):
    def __init__(self,speed):
        super(Bullet,self).__init__(speed,-1)
        #direction is downwards by default

class Obstruction:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.healthLevel = 5 #this goes down everytime the obstruction gets shot
        self.fullHealth = pygame.image.load()
        self.threequarterHealth = pygame.image.load()
        self.halfHealth = pygame.image.load()
        self.quarterHealth = pygame.image.load()
        self.noHealth = pygame.image.load()
