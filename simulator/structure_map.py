# -*- coding:utf-8 -*-

class StructureMap(object):

    # Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_INVISIVEL = 3
    M_PERSON = 5
    M_OBJECT = 6
    M_VOID = 8
    M_PLACEBO = 9

    def __init__(self, label, path):
        self.label = label
        self.path = path
        self.map = []
        self.len_row = 0
        self.len_col = 0

    def load_map(self):
        file = open(self.path, 'r')
        for line in file:
            line = line.strip('\n')
            self.map.append([])
            for col in line:
                self.map[self.len_row].append(int(col))
            self.len_row += 1
        file.close()
        self.len_col = len(self.map[0])