import pygame
import time
import scipy
import numpy as np

from world import WHITE, BLACK


class surface2():
    def __init__(self, x, y, name, scale=10.0):
        pygame.init()
        self.scale = scale
        X, Y = int(self.scale * x), int(self.scale * y)
        self.screen = pygame.display.set_mode([X, Y])
        pygame.display.set_caption(name)
        self.W0 = pygame.surfarray.pixels3d(self.screen)

        # Initialize the surface white
        #self.screen.lock()
        #self.W0[:, :, :] = WHITE
        #self.screen.unlock()
        pygame.surfarray.blit_array(self.screen, self.W0)
        pygame.display.flip()
    
    def update(self, world):
        #self.W0[:, :, :] = W1[:, :, :]
        im = scipy.misc.toimage(world, cmin=0.0, cmax=1.0, mode='P')
        size = tuple((np.array(im.size)*self.scale).astype(int))
        imnew = im.resize(size, resample=0)
        buff = scipy.misc.fromimage(imnew)
        #self.W0 = buff
        #self.screen.lock()
        #self.W0[:, :, :] = buff[:, :, :]
        pygame.surfarray.blit_array(self.screen, buff)
        #self.screen.unlock()
        pygame.display.flip()
    
    def destroy(self):
        pygame.quit()
