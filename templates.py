import numpy as np
from world import BLACK, WHITE


def dummy_agent(ROI, dx, dy):
    return ROI[dx, dy]


def random_agent(ROI, dx, dy):
    if np.random.random() >= 0.5:
        return WHITE
    else:
        return BLACK


def dummy_environment(world):
    pass
    

def dummy_genesis(world):
    pass


def random_genesis(world, threshold=0.5):
    decision = np.random.random(world.shape)
    world[decision >= threshold, ] =  BLACK


def gol_agent(ROI, dx, dy):
    
    binary = (ROI == BLACK).astype(int) 
    pop = binary.sum()

    # Define next state
    nstate = ROI[dx, dy] 

    if binary[dx, dy]:
        # Starvation
        if pop < 3:
            nstate = WHITE
        # Overpopulation
        elif pop > 4:
            nstate = WHITE
        else:
            nstate = BLACK
    else:
        # Reproduction
        if pop == 3:
            nstate = BLACK
        else:
            nstate = WHITE
        
    return nstate 
