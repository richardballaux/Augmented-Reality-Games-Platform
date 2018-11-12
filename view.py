"""this file will contain all the views from all the different models
    We did this so we can easily switch between them"""
class View():
    """this might have the views of all the different screens so we can make an overall UI"""
    def __init__(self,screenSize,organizer,model):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.organizer = organizer
        self.model = model
        pygame.display.set_caption = ("AR-Arcade")

    def draw():
        if self.organizer.state == "pong":
            #draw everything the pong needs
            pass
        if self.organizer.state == "spaceinvaders":
            pass
