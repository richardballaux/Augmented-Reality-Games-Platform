class View():
    def __init__(self,screenSize,organizer):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.organizer = organizer
        pygame.display.set_caption = ("AR-Arcade")

    def draw(model,organizer):
        self.model=model
        if self.organizer.state == "pong":
            #draw everything the pong needs
            pass
        if self.organizer.state == "spaceinvaders":
            pass
