import pygame
import time
import numpy as np
try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 
import scipy.misc
import sys

from kaleidoscope import world, templates, visualization
from kaleidoscope.world import BLACK, WHITE

#with World(x, y, dx, dy, name, agent=random_agent) as world:
opts = {'x':100, 'y':100, 'dx':1, 'dy':1, 'name': 'First_try', \
    'genesis': lambda x: templates.random_genesis(x, threshold=0.99),
    #'agent': templates.gol_agent,
    'agent': templates.snowflake,
    'surface': visualization.surface2,
    'border_policy': 'wrap',
    'seed': 23
    }

clock = pygame.time.Clock()
pb = ' '*80
with world.World(**opts) as world:
    while(not world.terminate):
        #time.sleep(1.0)
        world.cycle()
        time.sleep(world.cycle_sleep)
        
        if world.pause:
            print('<<Paused>>    ', end='\r')
        else:
            print('Cycle %d: %02.2fcpc' % (world.cycle_cnt, world.cpc), end='\r')
        
        sys.stdout.flush()
