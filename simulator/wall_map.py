# -*- coding:utf-8 -*-

from colour import Color
from copy import deepcopy
from math import exp
import numpy
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
import re

class WallMap(object):
    """Responsable to calc the distance from each field in the map to the closest wall, door or void.
        
    ...


    Attributes
    ----------
    label : str
        The name of the wall map.
    map : list of list of int
        The map with values of wall distances.
    len_row : int
        The horizontal size of the map.
    len_col : int
        The vertical size of the map.

    Methods
    -------
    load_wall_map(structure_map)
        Based on the structure map the wall map is started to be constructed.
    nearest_wall_distance(structure_map, row, col)
        Return the distance of the nearest wall of a specific field in the map.
    calc_wall_value(row, col, individual_KW):
        Calculate the wall value of a field based in an individual.
    draw_wall_map(directory):
        Draw the wall map using a range of colors from red to blue.

    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    # Object Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_INDIVIDUAL = 5
    M_OBJECT = 6
    M_VOID = 8

    # Directions Constant
    D_TOP = (-1, 0, 1)
    D_TOP_RIGHT = (-1, 1, 1.5)
    D_RIGHT = (0, 1, 1)
    D_BOTTOM_RIGHT = (1, 1, 1.5)
    D_BOTTOM = (1, 0, 1)
    D_BOTTOM_LEFT = (1, -1, 1.5)
    D_LEFT = (0, -1, 1)
    D_TOP_LEFT = (-1, -1, 1.5)

    def __init__(self, label):
        self.label = label
        self.map = []
        self.len_row = 0
        self.len_col = 0

    def load_wall_map(self, structure_map):
        """Based on the structure map the wall map is started to be constructed.

        Parameters
        ----------
        structure_map : StructureMap
            The structure map that contains the informations of the map.
        """
        self.map = []
        walls = []

        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

        for i in range(self.len_row):
            wall_map_row = []
            for j in range(self.len_col):
                if (structure_map.map[i][j] == self.M_DOOR or structure_map.map[i][j] == self.M_WALL): # If it is a DOOR or WALL
                    self.wall_direction(structure_map, walls, i, j)
                    wall_map_row.append(0)
                elif (structure_map.map[i][j] == self.M_EMPTY or structure_map.map[i][j] == self.M_VOID):
                    wall_map_row.append(self.M_EMPTY)
            self.map.append(wall_map_row)

        self.calc_wall_field(deepcopy(walls))
        for i in range(self.len_row):
            for j in range(self.len_col):
                if (structure_map.map[i][j] == self.M_DOOR or structure_map.map[i][j] == self.M_WALL): # If it is a DOOR or WALL
                    self.map[i][j] = 0

    def wall_direction(self, structure_map, walls, i, j):
        """Check in each direction if it needs to be expanded.

        Parameters
        ----------
        structure_map : StructureMap
            The structure map that contains the informations of the map.
        walls : List of tuple
            Defines the position, inicial value and direction that a wall need to be expanded.
        i : int
            X axis position.
        j : int
            Y axis position.
        """
        if (structure_map.map[i - 1][j] == self.M_EMPTY or structure_map.map[i - 1][j] == self.M_VOID): # TOP
            walls.append([i, j, 0, self.D_TOP])
        if ((structure_map.map[i - 1][j] == self.M_EMPTY or structure_map.map[i - 1][j] == self.M_VOID) and (structure_map.map[i][j + 1] == self.M_EMPTY or structure_map.map[i][j + 1] == self.M_VOID)): # TOP RIGHT
            walls.append([i, j, 0, self.D_TOP_RIGHT])
        if (structure_map.map[i][j + 1] == self.M_EMPTY or structure_map.map[i][j + 1] == self.M_VOID): # RIGHT
            walls.append([i, j, 0, self.D_RIGHT])
        if ((structure_map.map[i + 1][j] == self.M_EMPTY or structure_map.map[i + 1][j] == self.M_VOID) and (structure_map.map[i][j + 1] == self.M_EMPTY or structure_map.map[i][j + 1] == self.M_VOID)): # BOTTOM RIGHT
            walls.append([i, j, 0, self.D_BOTTOM_RIGHT])
        if (structure_map.map[i + 1][j] == self.M_EMPTY or structure_map.map[i + 1][j] == self.M_VOID): # BOTTOM
            walls.append([i, j, 0, self.D_BOTTOM])
        if ((structure_map.map[i + 1][j] == self.M_EMPTY or structure_map.map[i + 1][j] == self.M_VOID) and (structure_map.map[i][j - 1] == self.M_EMPTY or structure_map.map[i][j - 1] == self.M_VOID)): # BOTTOM LEFT
            walls.append([i, j, 0, self.D_BOTTOM_LEFT])
        if (structure_map.map[i][j - 1] == self.M_EMPTY or structure_map.map[i][j - 1] == self.M_VOID): # LEFT
            walls.append([i, j, 0, self.D_LEFT])
        if ((structure_map.map[i - 1][j] == self.M_EMPTY or structure_map.map[i - 1][j] == self.M_VOID) and (structure_map.map[i][j - 1] == self.M_EMPTY or structure_map.map[i][j - 1] == self.M_VOID)): # TOP LEFT
            walls.append([i, j, 0, self.D_TOP_LEFT])

    def calc_wall_field(self, walls):
        """After the wall map be pre constructed the real values are calculed using 
        a recursion principle based in FIFO lists.

        Parameters
        ----------
        walls : list of list of int
            Contains the location of each door or wall placed in map.
        """
        fifo_list = walls
        for field in walls:
            self.map[field[0]][field[1]] = field[2]
        while fifo_list:
            field = fifo_list.pop(0)  

            new_field = (field[0] + field[3][0], field[1] + field[3][1], field[2] + field[3][2], field[3])
            if (self.is_expansible(new_field)):
                fifo_list.append(new_field)
                self.map[new_field[0]][new_field[1]] = new_field[2]

            # If the position is a diagonal, is necessary to expand to two more directions
            if (field[3] == self.D_TOP_RIGHT):
                fifo_list.append((field[0], field[1], field[2], self.D_TOP))
                fifo_list.append((field[0], field[1], field[2], self.D_RIGHT))
            if (field[3] == self.D_BOTTOM_RIGHT):
                fifo_list.append((field[0], field[1], field[2], self.D_BOTTOM))
                fifo_list.append((field[0], field[1], field[2], self.D_RIGHT))
            if (field[3] == self.D_BOTTOM_LEFT):
                fifo_list.append((field[0], field[1], field[2], self.D_BOTTOM))
                fifo_list.append((field[0], field[1], field[2], self.D_LEFT))
            if (field[3] == self.D_TOP_LEFT):
                fifo_list.append((field[0], field[1], field[2], self.D_TOP))
                fifo_list.append((field[0], field[1], field[2], self.D_LEFT))            


    def is_expansible(self, field):
        """Return if one field is going to be expanded or not based on location and value.

        Parameters
        ----------
        fields : list of int
            Contain the information of one field of the map (locationX, locationY, value).
            
        Returns
        -------
        bool
            True if the field is going to be expanded, False otherwise.
        """
        if (not self.field_exist(field)):
            return False
        if (self.map[field[0]][field[1]] <= field[2] and self.map[field[0]][field[1]] != 0):
            return False
        return True

    def field_exist(self, field):
        """Check if the position of the field is in the map range.

        Parameters
        ----------
        fields : list of int
            Contain the information of one field of the map (locationX, locationY, value).
        
        Returns
        -------
        bool
            True if the field location is in range of the map, False otherwise.
        """
        if (field[0] < 0 or field[0] >= self.len_row):
            return False
        if (field[1] < 0 or field[1] >= self.len_col):
            return False
        return True

    def calc_wall_value(self, row, col, individual_KW):
        """Calculate the wall value of a field based in an individual.

        Parameters
        ----------
        row : int
            The row of the field that is going to be calculated the static value.
        col : int
            The col of the field that is going to be calculated the static value.
        individual_KW: float
            The wall map constant of an individual.
        Returns
        -------
        float
            Returns the value based in the individual_KW and the new location.
        """
        return exp(individual_KW * numpy.min([Util.DMax, self.map[row][col]]))

    def draw_wall_map(self, directory, structure_map):
        """Draw the wall map using a range of colors from red to blue.

        Parameters
        ----------
        directory : str
            Contain the directory that the image will be saved
        """
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        gray = (192, 192, 192)
        field_size = 20
        image = Image.new("RGB", (field_size * self.len_col, field_size * self.len_row), white)
        draw = ImageDraw.Draw(image)

        greater_value = 0
        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] > greater_value):
                    greater_value = self.map[i][j]
        colors = list(Color("red").range_to(Color("blue"), (int(greater_value) + 1)))

        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] == 0): # Wall, void or door case
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), black, black)
                else:
                    color = str(colors[int(self.map[i][j])].hex)
                    color = re.sub('[#]', '', color)
                    if (color.__len__() == 3):
                        color = color[0] + color[0] + color[1] + color[1] + color[2] + color[2]
                    color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
                    if color == (255,0,0):
                        color = (0,0,255)
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), color, black)
        Path(directory).mkdir(parents=True, exist_ok=True)
        image_name = directory + "/" + self.label + "_wall_map.png"
        image.save(image_name)