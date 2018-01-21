import pygame
import time
import numpy as np
from pudb import set_trace as st
import scipy.misc
import world
from world import BLACK, WHITE

import templates
import visualization

#with World(x, y, dx, dy, name, agent=random_agent) as world:
opts = {'x':100, 'y':100, 'dx':1, 'dy':1, 'name': 'First_try', \
    'genesis': lambda x: templates.random_genesis(x, threshold=0.95),
    'agent': templates.gol_agent,
    'surface': visualization.surface2
    }

clock = pygame.time.Clock()
with world.World(**opts) as world:
    while(world.cycle()):
        #time.sleep(1.0)
        clock.tick(10)
        if world.pause:
            print('<<Paused>>')
        else:
            print('Cycle %d' % world.cycle_cnt)
