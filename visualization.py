import pygame
from multiprocessing import Process, Lock, Value
import time

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()


    for num in range(10):

# Will have to use multiple processes
#https://pymotw.com/2/multiprocessing/basics.html
class UI(object):
    def __init__(self):
        pygame.init()

    def _draw_process(self, lock, display, draw_cycle):
        cycle = draw_cycle.value
        while(1){
            time.sleep(cycle)
            lock.acquire()
            display.flip()
            cycle = draw_cycle.value
            lock.release()
        }

    def create_world(self, x, y, name, draw_cycle=0.1):
        """
        Create an visualization of given size (x, y) and create a new process
        that draws the content of W0 to screen.
        """
        self.screen = pygame.display.set_mode([x, y])
        pygame.display.set_caption(name)
        self.W0 = pygame.surfarray.pixels3d(self.screen)
        self.clock = pygame.time.Clock()
        
        self.lock = Lock()
        self.draw_cycle=Value('d', draw_cycle, lock=False)

        self.process = Process(target=self., args=(self.lock, pygame.display, self.draw_cycle))
    
    def update(self, W0):
        """
        Update the internal display array
        """
        self.lock.acquire()
        self.W0 = W0
        self.lock.release()
    
    def get_input_event(self):
for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
    def events():
        while True:
            yield eventmodule.wait()
            while True:
                event = eventmodule.poll()
                if event.type == NOEVENT:
                    break
                else:
                    yield event


