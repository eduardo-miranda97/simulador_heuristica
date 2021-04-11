# -*- coding:utf-8 -*-

from colour import Color
from copy import deepcopy
from math import exp
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
import re

class StaticMap(object):
    """Responsable to calc the distance from the exit doors for each field in the map.

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

    Methods
    -------
    load_static_map(structure_map)
        Based on the structure map the static map is started to be constructed.
    calc_static_field(exit_gates)
        After the static map be pre constructed the real values are calculed using a recursion principle based in FIFO lists.
    is_expansible(field)
        Return if one field is going to be expanded or not based on location and value.
    field_exist(field)
        Check if the position of the field is in the map range.
    calc_static_value(row, col, individual_KS)
        Calculate the static value of a field based in an individual.
    draw_static_map(diretorio)
        Draw the static map using a range of colors from red to blue.

    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    # Object Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_PERSON = 5
    M_OBJECT = 6
    M_VOID = 8
    
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

    def __init__(self, label):
        self.label = label
        self.map = []
        self.len_row = 0
        self.len_col = 0

    def load_static_map(self, structure_map):
        """Based on the structure map the static map is started to be constructed.

        Parameters
        ----------
        structure_map : StructureMap
            The structure map that contains the informations of the map.
        """
        self.map = []
        exit_gates = []

        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

        for i in range(self.len_row):
            static_map_row = []
            for j in range(self.len_col):
                if (structure_map.map[i][j] == self.M_DOOR): # If it is a DOOR
                    exit_gates.append([i, j, 1])
                    static_map_row.append(1)
                elif (structure_map.map[i][j] == self.M_WALL or structure_map.map[i][j] == self.M_VOID): # If it is a WALL or VOID
                    static_map_row.append(self.S_WALL)
                elif (structure_map.map[i][j] == self.M_EMPTY):
                    static_map_row.append(self.M_EMPTY)
            self.map.append(static_map_row)

        self.calc_static_field(deepcopy(exit_gates))

    def calc_static_field(self, exit_gates):
        """After the static map be pre constructed the real values are calculed using 
        a recursion principle based in FIFO lists.

        Parameters
        ----------
        exit_gates : list of list of int
            Contains the location of each door placed in map.
        """
        fifo_list = exit_gates
        for field in exit_gates:
            self.map[field[0]][field[1]] = field[2]
        while fifo_list:
            field = fifo_list.pop(0)  

            for direction in ([self.D_TOP, self.D_TOP_RIGHT, self.D_RIGHT, self.D_BOTTOM_RIGHT, self.D_BOTTOM, self.D_BOTTOM_LEFT, self.D_LEFT, self.D_TOP_LEFT]):
                new_field = (field[0] + direction[0], field[1] + direction[1], field[2] + direction[2])
                if (self.is_expansible(new_field)):
                    fifo_list.append(new_field)
                    self.map[new_field[0]][new_field[1]] = new_field[2]
        
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
        if (self.map[field[0]][field[1]] == self.S_WALL):
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

    def calc_static_value(self, row, col, individual_KS):
        """Calculate the static value of a field based in an individual.

        Parameters
        ----------
        row : int
            The row of the field that is going to be calculated the static value.
        col : int
            The col of the field that is going to be calculated the static value.
        individual_KS: float
            The static map constant of an individual.
        Returns
        -------
        float
            Returns the value based in the individual_KS and the new location.
        """
        return exp(individual_KS * -self.map[row][col])

    def draw_static_map(self, directory):
        """Draw the static map using a range of colors from red to blue.

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
                if (self.map[i][j] != self.S_WALL and self.map[i][j] > greater_value):
                    greater_value = self.map[i][j]
        colors = list(Color("red").range_to(Color("blue"), (int(greater_value) + 1)))

        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] == self.S_WALL): # Wall or void case
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), black, black)
                elif (self.map[i][j] == 1): # Door case
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), red, black)
                else: # Draw or empty case
                    color = str(colors[int(self.map[i][j])].hex)
                    color = re.sub('[#]', '', color)
                    if (color.__len__() == 3):
                        color = color[0] + color[0] + color[1] + color[1] + color[2] + color[2]
                    color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
                    if color == (255,0,0):
                        color = (0,0,255)
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), color, black)
        Path(directory).mkdir(parents=True, exist_ok=True)
        image_name = directory + "/" + self.label + "_static-field.png"
        image.save(image_name)