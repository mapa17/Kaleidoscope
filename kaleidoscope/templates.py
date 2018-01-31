import numpy as np

# Are needed in world as default functions
def dummy_agent(ROI, dx, dy):
    return ROI[dx, dy]
def dummy_environment(world):
    pass
def dummy_genesis(world):
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
        #else:
        #    nstate = BLACK
    else:
        # Reproduction
        if pop == 3:
            nstate = BLACK
        #else:
        #    nstate = WHITE

    ROI[dx, dy] = nstate

def arrow_up(ROI, next_ROI, dx, dy):
    if ROI[dx, dy] == BLACK:
        next_ROI[dx, dy] = WHITE
        next_ROI[dx, dy-1] = BLACK


def arrow_left(ROI, dx, dy):
    if ROI[dx, dy] == BLACK:
        ROI[dx, dy] = WHITE
        ROI[dx-1, dy] = BLACK


def block(world, x, y, xsize, ysize, filling):
    world[x:x+xsize, y:y+ysize] = filling

def center_seed_genesis(world, x, y, seed_value=100):
    #world[x/2, y/2] = seed_value
    world[int(x/2), int(y/2)] = seed_value 

def snowflake_spawn(world, x, y, dx, dy):
    """
    Spawn a new point on the border using a uniform distribution
    """
    side, position = np.random.randint(x+y, size=2)
    side = side % 4
    if side == 0:
        xi = 0+dx+1
        yi = (position % y) + dy
    elif side == 1:
        xi = x+dx-1
        yi = (position % y) + dy
    elif side == 2:
        xi = (position % x) + dx
        yi = 0+dy+1
    elif side == 3:
        xi = (position % x) + dx
        yi = y+dy-1

    print('Spawning (%d/%d)'  % (xi, yi))
    world[xi, yi] = BLACK


def snowflake(ROI, dx, dy, seed_value=100):
    pop = (ROI == seed_value).astype(int).sum()

    if ROI[dx, dy] == BLACK:
        # If there is no seed neighbor, move the particle
        if pop < 1:
            ROI[dx, dy] = WHITE
            npos = np.random.randint(3, size=(1,2))[0]
            ROI[npos[0], npos[1]] = BLACK 
        else:
            # If we are next to a seed_point, fix this one, making it a new seed
            ROI[dx, dy] = seed_value

