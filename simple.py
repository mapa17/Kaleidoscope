import pygame
import time
import numpy as np
from pudb import set_trace as st
import scipy.misc

BLACK = 0.0
WHITE = 1.0 

#BLACK = (0, 0, 0)
#WHITE = (255, 255, 255)


class surface2():
    def __init__(self, x, y, name, scale=10.0):
        pygame.init()
        self.scale = scale
        X, Y = int(self.scale * x), int(self.scale * y)
        self.screen = pygame.display.set_mode([X, Y])
        pygame.display.set_caption(name)
        self.surface = pygame.display.get_surface()
        self.W0 = pygame.surfarray.pixels3d(self.screen)

        # Initialize the surface white
        self.W0[:, :, :] = WHITE
        pygame.display.flip()
    
    def update(self, world):
        #self.W0[:, :, :] = W1[:, :, :]
        im = scipy.misc.toimage(world, cmin=0.0, cmax=1.0, mode='P')
        size = tuple((np.array(im.size)*self.scale).astype(int))
        imnew = im.resize(size, resample=0)
        buff = scipy.misc.fromimage(imnew)
        #self.W0 = buff
        self.W0[:, :, :] = buff[:, :, :]
        pygame.display.flip()
    
    def get_world(self):
        return self.W0
    
    def destroy(self):
        pygame.quit()
    

def dummy_agent(ROI, dx, dy):
    return ROI

def random_agent(ROI, dx, dy):
    if np.random.random() >= 0.5:
        ROI[dx, dy, ] = WHITE
    else:
        ROI[dx, dy, ] = BLACK
    return ROI

def gol_agent(ROI, dx, dy):
    binary = np.any(ROI == BLACK, axis=2).astype(int)
    pop = binary.sum()
    if binary[dx, dy]:
        # Starvation
        if pop < 2:
            ROI[dx, dy, :] = WHITE
        # Overpopulation
        if pop > 3:
            ROI[dx, dy, :] = WHITE
        
        # Leave as it is
    else:
        # Reproduction
        if pop >= 3:
            ROI[dx, dy, :] = BLACK
        
    return ROI

def gol_agent2(ROI, dx, dy):
    binary = (ROI == BLACK).astype(int) 
    pop = binary.sum()
    if binary[dx, dy]:
        # Starvation
        if pop < 2:
            ROI[dx, dy] = WHITE
        # Overpopulation
        if pop > 3:
            ROI[dx, dy] = WHITE
        
        # Leave as it is
    else:
        # Reproduction
        if pop >= 3:
            ROI[dx, dy] = BLACK
        
    return ROI



def dummy_environment(world):
    pass

def dummy_genesis(world):
    pass

def random_genesis(world, threshold=0.5):
    decision = np.random.random(world.shape)
    world[decision >= threshold, ] =  BLACK

class World():
    def __init__(self, x, y, dx, dy, name, genesis=dummy_genesis, environment=dummy_environment, agent=dummy_agent):
        self.surface = surface2(x, y, name)
        self.W0 = np.ones(shape=(x, y)) 
        self.genesis = genesis
        self.environment = environment
        self.agent = agent
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
    
    def __enter__(self):
        self.genesis(self.W0)
        self.surface.update(self.W0)
        return self

    def __exit__(self, *args):
        self.surface.destroy()

    def cycle(self):
        return_value = True
        self.environment(self.W0)

        W1 = self.W0.copy()

        # Run the agent function over the complete world
        dx = self.dx
        dy = self.dy
        for x in range(dx,self.x):
            for y in range(dy, self.y):
                W1[x-dx:x+dx+1, y-dy:y+dy+1] = self.agent(self.W0[x-dx:x+dx+1, y-dy:y+dy+1], dx, dy)
        self.surface.update(W1)

        # Handle user input
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return_value=False # Flag that we are done so we exit this loop
        
        return return_value


x = 50
y = 50
name = 'First try'

#st()
clock = pygame.time.Clock()
#with World(x, y, dx, dy, name, agent=random_agent) as world:

loop_cnt = 0
with World(x, y, 1, 1, name, genesis=lambda x: random_genesis(x, threshold=0.95), agent=gol_agent2) as world:
#with World(x, y, 1, 1, name, genesis=dummy_genesis, agent=dummy_agent) as world:
    while(world.cycle()):
        loop_cnt = loop_cnt + 1
        #time.sleep(1.0)
        clock.tick(10)
        print('Cycle %d' % loop_cnt)
