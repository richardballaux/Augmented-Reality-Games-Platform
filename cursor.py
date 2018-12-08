import pygame

class Cursor():
    """Cursor representation for navigating through the settings
    x -- initial x coordinate of the cursor
    y -- initial y coordinate of the cursor
    radius -- radius of the cursor
    """
    def __init__(self, x, y, radius, organizer):
        self.x = x
        self.y = y
        self.radius = radius
        self.organizer = organizer

    def draw(self, screen): #Draws a representation of the cursor (purple circle)
        #print(self.x, self.y)
        pygame.draw.circle(screen, self.organizer.settings_cursorColor, (self.x,self.y), self.radius)

    def update(self, x, y):
        self.x = x
        self.y = y

class CursorRecognition():
    """Recognizes a cursor that hovers over an area and triggers a change of an attribute of an object_to_change.
    counts up every loop the XY object is still in the same area.

    counter_limit -- int, the limit for when "something" should be triggered
    area -- list of form: same as pygame draw rectangle - [upper left corner x, upper left corner y, length in x direction, length in y direction]
    """
    def __init__(self, text,counter_limit, area,organizer):
        self.text=text
        self.counter = 0 #Counter for areaSurveillance
        self.limit = counter_limit  # Time it should take to trigger (?)
        self.input = area
        self.triggerArea = [self.input[0], self.input[1]+self.input[3], self.input[0]+self.input[2], self.input[1]]
        self.organizer = organizer
        self.myfont = pygame.font.SysFont("monospace", 42)
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True) #font is used for numbers in "select_speed" state
        self.ColorGreen = (0,250,0)
        self.ColorBlack = (0,0,0)
        self.ColorYellow = (250,250,0)

    def areaSurveillance(self, cursor,change_state_to, object_to_change, attribute_of_object, change_attribute_to):
        """With a specific cursor as an input, change the attribute of an object to a specific value

        cursor -- cursor.x should be x coordinate, cursor.y should be y coordinate
        change_state_to -- changes state of game. To stay in same state just input the same state here
        object_to_change -- pass in the class object to change
        attribute_of_object -- as a string, pass in the attribute of the corresponding class object to change
        change_attribute_to -- pass in the value object.attribute needs to be changed to when triggered
        """
        #checks if coordinates of cursor are in the recatangle from the area input (self.triggerArea)
        if int(cursor.x) in range(int(self.triggerArea[0]), int(self.triggerArea[2]+1)):
            if int(cursor.y) in range(int(self.triggerArea[3]+1), int(self.triggerArea[1])):  # y-coordinates flipped since y coordinates are upside down
                self.counter += 1 #inrement counter by one if hovered over areaSurveillance area and set back two zero when not hoverd over it
            else:
                self.counter = 0 #set cpunter back to 0 when not hovered over self.triggerArea - this is for y coordiantes
        else:
            self.counter = 0 #set cpunter back to 0 when not hovered over self.triggerArea - this is for x coordiantes

        # when counter limit reached do change the state of the organizer and change the attribute of the object to its next value
        if self.counter == self.limit:
            self.organizer.state = change_state_to
            setattr(object_to_change, attribute_of_object, change_attribute_to) #changes an attribute (attribute_of_object) of an object (object_to_change) to a value (change_attribute_to)

    def draw(self,screen,color = (250,250,0)):
        """This function draws the button to the screen with the given text and button size"""
        pygame.draw.rect(screen,color,pygame.Rect(self.input[0],self.input[1],self.input[2],self.input[3]))
        textMaker = self.myfont.render(self.text, 1, self.ColorGreen)
        screen.blit(textMaker,(self.input[0]+50,self.input[1]))
