import pygame

# Will have to use multiple processes
#https://pymotw.com/2/multiprocessing/basics.html
class UI(object):
    def __init__(self):
        pygame.init()
    
    def create_world(self, x, y, name):
        """
        Create a 
        """
        self.screen = pygame.display.set_mode([x, y])
        pygame.display.set_caption(name)
        self.W0 = pygame.surfarray.pixels3d(self.screen)
        self.clock = pygame.time.Clock()