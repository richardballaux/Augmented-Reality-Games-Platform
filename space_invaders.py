"""Space invaders file

This game need to have:
This is all based on this video:
https://www.youtube.com/watch?v=D1jZaIPeD5w
PIXELART generator :
https://www.piskelapp.com/p/agxzfnBpc2tlbC1hcHByEwsSBlBpc2tlbBiAgKDwzZSzCww/edit
"""
dir_path = os.path.dirname(os.path.realpath(__file__))

class SpaceInvadersModel():
    def __init__(self):
        self.enemystartxcoord = 100
        self.distanceBetweenEnemiesx = 50
        self.enemystartycoord = 100
        self.distanceBetweenEnemiesy = 50
        self.enemies = [][]
        for i in range(10):
            self.enemies[i][0]= EnemyLevel3(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord,dir_path+"/data/level3monster.png")
        for i in range(10):
            self.enemies[i][1] = EnemyLevel2(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord+distanceBetweenEnemiesy,dir_path+"/data/level2monster.png")
        for i in range(10):
            for j in range(2,3):
                self.enemies[i][j] = EnemyLevel1(enemystartxcoord+distanceBetweenEnemiesx*i,enemystartycoord+distanceBetweenEnemiesy*j,dir_path+"/data/level1monster.png")

        self.obstructions = []
        for i in range(3):
            self.obstructions[i] = Obstruction(450*i,800)
        self.player = Player(900,900,dir_path+"/data/spaceship.png")

        self.components = [self.enemies,self.obstructions,self.player]

        

    def update(self):
        for component in self.components:
            component.update()



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
        pass
    def move(self):
        pass


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
