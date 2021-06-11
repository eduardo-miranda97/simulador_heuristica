# -*- coding:utf-8 -*-

class StructureMap(object):
    """Responsable to store the map fisical informations: doors, walls, etc.

    ...

    Attributes
    ----------
    label : str
        The name of the static map.
    map : list of list of int
        The map with values of static fields.
    len_row : int
        The horizontal size of the map.
    len_col : int
        The vertical size of the map.
    path : str
        Directory path which contains the map file.

    Methods
    -------
    load_map()
        Read the map file to construct the structure map.
    get_empty_positions()
        Returns a list which contains the empty positions of the structure map.
    
    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    # Object Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_OBJECT = 6
    M_VOID = 8

    def __init__(self, label, path):
        self.label = label
        self.path = path
        self.map = []
        self.len_row = 0
        self.len_col = 0

    def load_map(self):
        """Read the map file to construct the structure map.
        """
        file = open(self.path, 'r')
        for line in file:
            line = line.strip('\n')
            self.map.append([])
            for col in line:
                self.map[self.len_row].append(int(col))
            self.len_row += 1
        file.close()
        self.len_col = len(self.map[0])

    def get_empty_positions(self):
        """Returns a list which contains the empty positions of the structure map.

        Returns
        -------
        list of tuple
            List that contains the empty positions of the structure map.
        """
        empty_positions = []
        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] == self.M_EMPTY):
                    empty_positions.append((i, j))
        return empty_positions