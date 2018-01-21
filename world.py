import numpy as np
import pygame

BLACK = 0.0
WHITE = 1.0

import visualization as viz
import templates as T

from pudb import set_trace

class World():
    def __init__(self, x, y, dx, dy, name, genesis=T.dummy_genesis, environment=T.dummy_environment, agent=T.dummy_agent, surface=viz.surface2):
        self.surface = surface(x, y, name)
        self.W0 = np.ones(shape=(x, y)) 
        self.genesis = genesis
        self.environment = environment
        self.agent = agent
        self.x, self.y, self.dx, self.dy = x, y, dx, dy

        # Default internal states of the world
        self.terminate = False
        self.pause = False
        self.cycle_sleep = 0.5
        self.cycle_cnt = 0
    
    def __enter__(self):
        self.genesis(self.W0)
        self.surface.update(self.W0)
        return self

    def __exit__(self, *args):
        self.surface.destroy()
    
    def _input_handling(self):
        # Handle user input
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.terminate = True # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif event.key == pygame.K_q:
                    self.terminate = True
                elif event.key == pygame.K_w:
                    self.cycle_sleep = self.cycle_sleep * 0.8
                elif event.key == pygame.K_s:
                    self.cycle_sleep = self.cycle_sleep * 1.2
                elif event.key == pygame.K_t:
                    img_path = "./screen_shots/world_%03d.png" % self.cycle_cnt
                    print('Writing image to %s ...' % img_path)
                    self.surface.store_image(self.W0, img_path)
                    pass


    def cycle(self):
        return_value = True

        # Handle user input
        self._input_handling()
        
        if not self.pause:
            self.cycle_cnt = self.cycle_cnt + 1
            self.environment(self.W0)

            W1 = self.W0.copy()

            # Run the agent function over the complete world
            dx = self.dx
            dy = self.dy
            for x in range(dx,self.x):
                for y in range(dy, self.y):
                    #W1[x-dx:x+dx+1, y-dy:y+dy+1] = self.agent(self.W0[x-dx:x+dx+1, y-dy:y+dy+1], dx, dy)
                    W1[x, y] = self.agent(self.W0[x-dx:x+dx+1, y-dy:y+dy+1], dx, dy)
            self.surface.update(W1)
            
            # Copy the world buffer for the next cycle
            self.W0 = W1

        if self.terminate:
            return_value = False

        return return_value

