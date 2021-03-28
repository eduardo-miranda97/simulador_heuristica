# -*- coding:utf-8 -*-

class Individual(object):

    def __init__(self, configuration, col, row):
        self.label = configuration["label"]
        self.red = configuration["red"]
        self.green = configuration["green"]
        self.red = configuration["red"]
        self.blue = configuration["blue"]
        self.speed = configuration["speed"]
        self.KD = configuration["KD"] # Dinamic map const
        self.KS = configuration["KS"] # Static map const
        self.KW = configuration["KW"] # Wall map const
        self.KI = configuration["KI"] # Inertia const

        self.col = col
        self.row = row
        self.leave = False
        self.spent_iterations = 0
