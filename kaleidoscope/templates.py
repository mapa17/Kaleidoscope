import numpy as np

# Are needed in world as default functions
def dummy_agent(ROI, dx, dy):
    return ROI[dx, dy]
def dummy_environment(world):
    pass
def dummy_genesis(worl):
    pass

from .world import BLACK, WHITE

def random_agent(ROI, dx, dy):
    if np.random.random() >= 0.5:
        return WHITE
    else:
        return BLACK


def random_genesis(world, threshold=0.5):
    decision = np.random.random(world.shape)
    world[decision >= threshold, ] =  BLACK

def gol_agent(ROI, dx, dy):
    """
    Game of Life
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

    Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overpopulation.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    >>> roi0 = np.ones(shape=(3, 3))

    >>> # Starvation
    >>> roi1 = roi0.copy()
    >>> roi1[1, 1] = 0.0
    >>> gol_agent(roi1, 1, 1)
    array([[ 1.,  1.,  1.],
           [ 1.,  1.,  1.],
           [ 1.,  1.,  1.]])

    >>> # Overpopulation
    >>> roi1 = roi0.copy()
    >>> roi1[0, :] = 0.0
    >>> gol_agent(roi1, 1, 1)
    array([[ 0.,  0.,  0.],
           [ 1.,  0.,  1.],
           [ 1.,  1.,  1.]])

    >>> # Overpopulation
    >>> roi1 = roi0.copy()
    >>> roi1[:, :] = 0.0
    >>> gol_agent(roi1, 1, 1)
    array([[ 0.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  0.]])

    >>> # Remain
    >>> roi1 = roi0.copy()
    >>> roi1[0, :] = 0.0
    >>> roi1[2, :] = 0.0
    >>> gol_agent(roi1, 1, 1)
    array([[ 0.,  0.,  0.],
           [ 1.,  1.,  1.],
           [ 0.,  0.,  0.]])

    >>> # Reproduce 
    >>> roi1 = roi0.copy()
    >>> roi1[1, :] = 0.0
    >>> roi1[2, :] = 0.0
    >>> gol_agent(roi1, 1, 1)
    array([[ 1.,  1.,  1.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  0.]])

    """
    pop = ROI.sum()

    # Define next state
    nstate = ROI[dx, dy] 

    if ROI[dx, dy]:
        # Starvation
        if pop < 3:
            nstate = WHITE
        # Overpopulation
        elif pop > 4:
            nstate = WHITE
        #else:
        #    nstate = BLACK
    else:
        # Reproduction
        if pop == 3:
            nstate = BLACK
        #else:
        #    nstate = WHITE

    ROI[dx, dy] = nstate

def snowflake(ROI, dx, dy):
    pop = ROI.sum()

    if ROI[dx, dy]:
        # If there is no neighbor, move the particle
        if pop < 2:
            ROI[dx, dy] = WHITE
            ROI[np.random.randint(3, size=(1,2))] = BLACK
