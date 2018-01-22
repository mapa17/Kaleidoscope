import pygame
import time
import scipy
import numpy as np

from world import WHITE, BLACK
try:
    from pudb import set_trace as st
except ModuleNotFoundError:
    st = lambda: None 


class surface2():
    def __init__(self, x, y, name, scale=10.0):
        pygame.init()
        self.scale = scale
        X, Y = int(self.scale * x), int(self.scale * y)
        self.screen = pygame.display.set_mode([X, Y])
        pygame.display.set_caption(name)
    
    def update(self, world):
        #self.W0[:, :, :] = W1[:, :, :]
        img = self.__buffer_to_image(world, self.scale)
        buff = scipy.misc.fromimage(img)

        pygame.surfarray.blit_array(self.screen, buff)
        pygame.display.flip()
    
    def __buffer_to_image(self, buffer, scale):
        im = scipy.misc.toimage(buffer, cmin=0.0, cmax=1.0, mode='P')
        size = tuple((np.array(im.size)*scale).astype(int))
        scaled_img = im.resize(size, resample=0)
        return scaled_img 
    
    def store_image(self, world, image_path):
        img = self.__buffer_to_image(world, self.scale)
        img.save(image_path)

    def destroy(self):
        pygame.quit()
