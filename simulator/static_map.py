# -*- coding:utf-8 -*-

# static_map.py
#
# 14/02/2021
#
# Eduardo Miranda
# Luiz Eduardo Pereira

from copy import deepcopy

class StaticMap(object):

    # Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_PERSON = 5
    M_OBJECT = 6
    M_VOID = 8
    M_PLACEBO = 9

    # Directions Constant
    D_TOP = (-1, 0, 1)
    D_TOP_LEFT = (-1, -1, 1.5)
    D_TOP_RIGHT = (-1, 1, 1.5)
    D_LEFT = (0, -1, 1)
    D_RIGHT = (0, 1, 1)
    D_BOTTOM = (1, 0, 1)
    D_BOTTOM_LEFT = (1, -1, 1.5)
    D_BOTTOM_RIGHT = (1, 1, 1.5)

    def __init__(self, label):
        self.label = label
        self.map = []
        self.exit_gates = []
        self.len_row = 0
        self.len_col = 0

    # *****
    def load_static_map(self, structure_map):
        self.map = []
        self.exit_gates = []

        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

        for i in range(self.len_row):
            static_map_row = []
            for j in range(self.len_col):
                if (structure_map[i][j] == self.M_DOOR): # If it is a DOOR
                    self.exit_gates.append([i, j, 1])
                    static_map_row.append(self.M_DOOR)
                elif (structure_map[i][j] == self.M_WALL or structure_map[i][j] == self.M_VOID): # If it is a WALL or VOID
                    static_map_row.append(1000)        
                elif (structure_map[i][j] == self.M_EMPTY or structure_map[i][j] == self.M_PLACEBO):
                    static_map_row.append(self.M_EMPTY)
            self.map.append(static_map_row)

        self.calc_static_field(self, deepcopy(self.exit_gates))

    # *****
    def calc_static_field(self, exit_gates):
        fifo_list = exit_gates
        while fifo_list:
            field = fifo_list.pop(0)
            self.map[field[0]][field[1]] = field[2]

            for direction in ([self.D_TOP, self.D_TOP_LEFT, self.D_TOP_RIGHT, self.D_LEFT, self.D_RIGHT, self.D_BOTTOM, self.D_BOTTOM_LEFT, self.D_BOTTOM_RIGHT]):
                new_field = (field[0] + direction[0], field[1] + direction[1], field[2] + direction[2])
                if (self.is_expansible(new_field)):
                    fifo_list.append(new_field)
                    
    # ***
    def is_expansible(self, field):
        if (not self.field_exist(field)):
            return False
        if (self.map[field[0]][field[1]] == self.M_DOOR):
        # if isWall(field):
            return False
        if (self.map[field[0]][field[1]] == self.M_VOID):
        # if isVoid(field):
            return False
        if (self.map[field[0]][field[1]] <= field[2] and self.map[field[0]][field[1]] != 0):
            return False
        return True
            
    # *****
    def field_exist(self, field):
        if (field[0] < 0 or field[0] >= self.len_row):
            return False
        if (field[1] < 0 or field[1] >= self.len_col):
            return False
        return True