import view
import model
import
import controller


def Main(model,view,controller):
    """Update graphics and check for pygame events.
    model -- an object of the type ArPongModel()
    view -- an object of the type PlayboardWindowView()
    controller -- an object ArPongMouseController()
    """
    running = True
    while running:
        if 0xFF == ord('q'):
            running = False
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            controller.handle_event(event)
        #controller.update()
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
Organizer = Organizer()
#We start the game in the Organizer state
Organizer.state = "menu"
#arguments are screenSize, the BoundaryOffset, BoundaryThickness, ballRadius, ballSpeed
model = ArPongModel(screenSize,(50,50),10,camera)
view = PlayboardWindowView(model,screenSize, Organizer)
view._draw_background()
controller = ArPongMouseController(model)
#controller = ArPongObjectRecogController(model)
Main(model,view,controller)
