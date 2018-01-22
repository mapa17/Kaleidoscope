import numpy as np
import pygame

BLACK = 0.0
WHITE = 1.0
NOSE = 0.77

import visualization as viz
import templates as T

try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 



class World():
    def __init__(self, x, y, dx, dy, name, \
    genesis=T.dummy_genesis, \
    environment=T.dummy_environment, \
    agent=T.dummy_agent, \
    surface=viz.surface2, \
    border_policy='deadzone'):
        st()
        self.surface = surface(x, y, name)
        self.W0 = np.ones(shape=(x+2*dx, y+2*dy)) 
        self.genesis = genesis
        self.environment = environment
        self.agent = agent
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
        self.border_policy = border_policy

        # Default internal states of the world
        self.terminate = False
        self.pause = True # Start paused 
        self.cycle_sleep = 0.25
        self.cycle_cnt = 0
    
    def __enter__(self):
        self.genesis(self.W0)
        # Apply the border policy selected
        self._border_policy_enforcement(self.W0)

        x, y = self.x, self.y
        dx, dy = self.dx, self.dy
        # Pass the x, y area
        self.surface.update(self.W0[dx:x+dx, dy:y+dy])
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
                    self.cycle_sleep = max(0.0, self.cycle_sleep - 0.25)
                elif event.key == pygame.K_s:
                    self.cycle_sleep = min(2.0, self.cycle_sleep + .25)
                elif event.key == pygame.K_t:
                    img_path = "./screen_shots/world_%03d.png" % self.cycle_cnt
                    print('Writing image to %s ...' % img_path)
                    self.surface.store_image(self.W0, img_path)

    def _border_policy_enforcement(self, buffer):
        dx, dy = self.dx, self.dy
        x, y = self.x, self.y

        buffer_original = buffer.copy()
        if self.border_policy == 'deadzone':
            buffer[0:dx, :] = WHITE 
            buffer[:, 0:dy] = WHITE 
            buffer[x+dx:x+2*dx, :] = WHITE 
            buffer[:, y+dy:y+2*dy] = WHITE 
        elif self.border_policy == 'reflection':
            for ix in range(dx):
                buffer[ix, :] = buffer_original[(2*dx-1)-ix, :]
                buffer[ix+x+dx, :] = buffer_original[(x+dx)-(ix+1), :]

            for iy in range(dy):
                buffer[iy, :] = buffer_original[(2*dy-1)-iy, :]
                buffer[iy+y+dy, :] = buffer_original[(y+dy)-(iy+1), :]
        elif self.border_policy == 'wrap':
            buffer[0:dx, :] = buffer_original[x:x+dx, :]
            buffer[x+dx:x+2*dx, :] = buffer_original[dx:2*dx, :]
            buffer[:, 0:dy] = buffer_original[:, y:y+dy]
            buffer[:, y+dy:y+2*dy] = buffer_original[:, dy:2*dy]
        else:
            print("Error! Invalid border policy!")

    def cycle(self):
        # Handle user input
        self._input_handling()
        
        if not self.pause:
            self.cycle_cnt = self.cycle_cnt + 1

            # Apply environment function
            self.environment(self.W0)

            W1 = self.W0.copy()

            # Run the agent function over the complete world
            dx = self.dx
            dy = self.dy
            for x in range(dx,self.x+dx):
                for y in range(dy, self.y+dy):
                    #W1[x-dx:x+dx+1, y-dy:y+dy+1] = self.agent(self.W0[x-dx:x+dx+1, y-dy:y+dy+1], dx, dy)
                    W1[x, y] = self.agent(self.W0[x-dx:x+dx+1, y-dy:y+dy+1], dx, dy)

            # Apply the border policy selected
            self._border_policy_enforcement(W1)

            # Pass the x, y area
            self.surface.update(W1[dx:self.x+dx, dy:self.y+dy])

            # Copy the world buffer for the next cycle
            self.W0 = W1
