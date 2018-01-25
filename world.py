import numpy as np
import numpy
import pygame
import ctypes
import time
import datetime 

try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 

import multiprocessing as mp
from multiprocessing import Pool

BLACK = 0.0
WHITE = 1.0
NOSE = 0.77

import visualization as viz
import templates as T

class World():
    def __init__(self, x, y, dx, dy, name, \
    genesis=T.dummy_genesis, \
    environment=T.dummy_environment, \
    agent=T.dummy_agent, \
    surface=viz.surface2, \
    border_policy='deadzone', \
    seed=None):
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
        self.last_cycle = datetime.datetime.now()
        # Cycles per second
        self.cps = 0

        # Prepare worker process
        self.shared_W0 = mp.Array(ctypes.c_double, (x+2*dx)*(y+2*dy), lock=False)
        self.W0 = np.frombuffer(self.shared_W0)
        self.W0 = self.W0.reshape(x+2*dx, y+2*dy)

        self.shared_W1 = mp.Array(ctypes.c_double, self.W0.size, lock=False)
        self.W1 = np.frombuffer(self.shared_W1)
        self.W1 = self.W1.reshape(self.W0.shape)

        # Reserve one for the plotting function
        ncpu = mp.cpu_count()
        if seed is None:
            seed = np.random.randint(10000) 
        self.pool = Pool(processes=ncpu-1, initializer=self._init_worker, initargs=(seed, self.shared_W0, self.shared_W1,))

        # Precalculate the worker arguments
        self.worker_args = [(x, self.x, self.y, dx, dy, self.agent) for x in range(dx, self.x+dx)]
 
    
    def __enter__(self):
        self.W0[:, :] = WHITE
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
        self.pool.terminate()
    
    def _input_handling(self):
        # Handle user input
        for etype, ekey in self.surface.get_events(): # User did something
            #print('Getting event %d and key %s' % (etype, ekey))
            if etype == pygame.QUIT: # If user clicked close
                self.terminate = True # Flag that we are done so we exit this loop
            elif etype == pygame.KEYDOWN :
                if ekey == pygame.K_SPACE :
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif ekey == pygame.K_q:
                    self.terminate = True
                elif ekey == pygame.K_w:
                    self.cycle_sleep = max(0.0, self.cycle_sleep - 0.25)
                elif ekey == pygame.K_s:
                    self.cycle_sleep = min(2.0, self.cycle_sleep + .25)
                elif ekey == pygame.K_t:
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

    @staticmethod
    def _init_worker(seed, shared_W0_, shared_W1_):
        p = mp.current_process()
        my_seed = seed + int(p.name.split('-')[1])
        print('Initializing random generator in %s with %s' % (p.name, my_seed))
        numpy.random.seed(my_seed)

        global shared_W1
        shared_W1 = shared_W1_
        global shared_W0
        shared_W0 = shared_W0_

    @staticmethod
    def _agend_process(ix, x, y, dx, dy, agent):
        W0 = np.frombuffer(shared_W0)
        W0 = W0.reshape(x+2*dx, y+2*dy)

        W1 = np.frombuffer(shared_W1)
        W1 = W1.reshape(x+2*dx, y+2*dy)

        for iy in range(dy, y+dy):
            W1[ix, iy] = agent(W0[ix-dx:ix+dx+1, iy-dy:iy+dy+1], dx, dy)


    def cycle(self):
        # Handle user input
        self._input_handling()
        if not self.pause:
            # Calculate cycles per second
            now = datetime.datetime.now()
            diff = now - self.last_cycle
            insec = diff.seconds + diff.microseconds / 999999
            self.cpc = float(1.0 / insec)
            self.last_cycle = now

            self.cycle_cnt = self.cycle_cnt + 1

            # Apply environment function
            self.environment(self.W0)
            self.W1[:, :] = self.W0[:, :]

            # Use the worker pool in order to update self.W1 based on self.W0
            self.pool.starmap(self._agend_process, self.worker_args)

            # Apply the border policy selected
            self._border_policy_enforcement(self.W1)

            # Pass the x, y area
            self.surface.update(self.W1[self.dx:self.x+self.dx, self.dy:self.y+self.dy])

            # Copy the world buffer for the next cycle
            self.W0[:, :] = self.W1[:, :]
