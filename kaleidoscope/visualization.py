import pygame
import time
import scipy
import numpy as np
import multiprocessing as mp 
import datetime

from .world import WHITE, BLACK
try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 

import logging

class surface2():
    def __init__(self, x, y, name, scale=10.0):
        self.scale = scale
        X, Y = int(self.scale * x), int(self.scale * y)
        #self.screen = pygame.display.set_mode((X, Y))
        #self.screen = pygame.display.set_mode((X, Y), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)
        #pygame.display.set_caption(name)   

        #logger = mp.log_to_stderr()
        #logger.setLevel(logging.INFO)
        self.pipe, self.child_conn = mp.Pipe()
        self.p = mp.Process(target=self._draw_buffer, args=(self.child_conn, X, Y, name, self.scale))
        self.p.start()
    
    def update(self, world):
        self.pipe.send(world)
    
    def get_events(self):
        if self.pipe.poll():
            events = []
            while(self.pipe.poll()):
                events.append(self.pipe.recv())
            return events
        else:
            return []


    @staticmethod
    def _draw_buffer(pipe, X, Y, name, image_scale, fps=5.0):
        pygame.init()
        surface = pygame.display.set_mode((X, Y))
        pygame.display.set_caption(name)

        interval = 1.0/fps
        # Make sure the first frame is drawn ...
        last_flip = datetime.datetime(1980, 1, 1)

        terminate = False
        while(not terminate):
            if pipe.poll(0.5):
                buffer = pipe.recv()
                if buffer is None:
                    terminate = True
                else:
                    t1 = datetime.datetime.now() - last_flip
                    since_last_flip = t1.seconds + t1.microseconds/1000000.0
                    if since_last_flip > interval:
                        img = surface2.__buffer_to_image(buffer, image_scale)
                        big_buffer = scipy.misc.fromimage(img)
                        pygame.surfarray.blit_array(surface, big_buffer)
                        pygame.display.flip()
                        last_flip = datetime.datetime.now() 

            # If there are some pygame events, send them to the main process
            if pygame.event.peek():
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        pipe.send((event.type, event.key))
                    else:
                        pipe.send((event.type, None))
        
        pygame.quit()


    @staticmethod    
    def __buffer_to_image(buffer, scale):
        im = scipy.misc.toimage(buffer, cmin=0, cmax=127, mode='P')
        size = tuple((np.array(im.size)*scale).astype(int))
        scaled_img = im.resize(size, resample=0)
        return scaled_img 
    
    def store_image(self, world, image_path):
        img = self.__buffer_to_image(world, self.scale)
        img.save(image_path)

    def destroy(self):
        self.pipe.send(None)
        self.p.join()
