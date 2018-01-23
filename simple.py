import pygame
import time
import numpy as np
try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 
import scipy.misc
import world
from world import BLACK, WHITE

import templates
import visualization

#with World(x, y, dx, dy, name, agent=random_agent) as world:
opts = {'x':100, 'y':100, 'dx':1, 'dy':1, 'name': 'First_try', \
    'genesis': lambda x: templates.random_genesis(x, threshold=0.95),
    'agent': templates.gol_agent,
    'surface': visualization.surface2,
    'border_policy': 'wrap',
    'seed': 23
    }

clock = pygame.time.Clock()
with world.World(**opts) as world:
    while(not world.terminate):
        #time.sleep(1.0)
        world.cycle()
        time.sleep(world.cycle_sleep)
        if world.pause:
            print('<<Paused>>')
        else:
            print('Cycle %d' % world.cycle_cnt)
