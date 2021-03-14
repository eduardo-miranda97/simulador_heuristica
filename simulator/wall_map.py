# -*- coding:utf-8 -*-

from colour import Color
from math import exp
import numpy
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

    # Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_PERSON = 5
    M_OBJECT = 6
    M_VOID = 8
    M_PLACEBO = 9

    # Directions Constant
    D_TOP = (-1, 0,)
    D_TOP_RIGHT = (-1, 1)
    D_RIGHT = (0, 1)
    D_BOTTOM_RIGHT = (1, 1)
    D_BOTTOM = (1, 0)
    D_BOTTOM_LEFT = (1, -1)
    D_LEFT = (0, -1)
    D_TOP_LEFT = (-1, -1)

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
        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

        for i in range(self.len_row):
            row = []
            for j in range(self.len_col):
                row.append(self.nearest_wall_distance(structure_map, i, j))
            self.map.append(row)

    def nearest_wall_distance(self, structure_map, row, col):
        """Return the distance of the nearest wall of a specific field in the map.

        Parameters
        ----------
        structure_map : StructureMap
            The structure map that contains the informations of the map.
        row : int
            The row of the field that is going to be calculated.
        col : int
            The col of the field that is going to be calculated.
            
        Returns
        -------
        int
            Integer value of the distance of the nearest wall
        """
        rows = {self.D_TOP: row, self.D_TOP_RIGHT: row, self.D_RIGHT: row, self.D_BOTTOM_RIGHT: row, self.D_BOTTOM: row, self.D_BOTTOM_LEFT: row, self.D_LEFT: row, self.D_TOP_LEFT: row}
        cols = {self.D_TOP: col, self.D_TOP_RIGHT: col, self.D_RIGHT: col, self.D_BOTTOM_RIGHT: col, self.D_BOTTOM: col, self.D_BOTTOM_LEFT: col, self.D_LEFT: col, self.D_TOP_LEFT: col}
        distance = 0

        while (True):
            for direction in ([self.D_TOP, self.D_TOP_RIGHT, self.D_RIGHT, self.D_BOTTOM_RIGHT, self.D_BOTTOM, self.D_BOTTOM_LEFT, self.D_LEFT, self.D_TOP_LEFT]):
                if (structure_map.map[rows[direction]][cols[direction]] != self.M_WALL and structure_map.map[rows[direction]][cols[direction]] != self.M_DOOR and structure_map.map[rows[direction]][cols[direction]] != self.M_VOID):
                    rows[direction] += direction[0]
                    cols[direction] += direction[1]
                else:
                    return distance
            distance += 1

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

    def draw_wall_map(self, directory):
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
        image_name = self.label + "_wall_map.png"
        image.save(image_name)