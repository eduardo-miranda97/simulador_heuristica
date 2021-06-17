class Constants(object):

    def __init__(self):
        pass
    
    # Object Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_VOID = 3
    
    # Static Field Constant
    S_WALL = 9999

    # Directions Constant
    D_TOP = (-1, 0, 1)
    D_TOP_RIGHT = (-1, 1, 1.5)
    D_RIGHT = (0, 1, 1)
    D_BOTTOM_RIGHT = (1, 1, 1.5)
    D_BOTTOM = (1, 0, 1)
    D_BOTTOM_LEFT = (1, -1, 1.5)
    D_LEFT = (0, -1, 1)
    D_TOP_LEFT = (-1, -1, 1.5)