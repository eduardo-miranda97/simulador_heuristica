# -*- coding:utf-8 -*-

class Individual(object):

    def __init__(self, configuration, col, row):
        self.label = configuration["label"]
        self.red = configuration["red"]
        self.green = configuration["green"]
        self.blue = configuration["blue"]
        self.speed = configuration["speed"]
        self.KD = configuration["KD"] # Dinamic map const
        self.KS = configuration["KS"] # Static map const
        self.KW = configuration["KW"] # Wall map const
        self.KI = configuration["KI"] # Inertia const

        self.col = col
        self.row = row
        self.evacuated = False
        self.steps = 0

    def __str__(self):
        string = f"Label: {self.label}\t R:{self.red}\t G:{self.green}\t B:{self.blue}\t Speed:{self.speed}\t"
        string += f"KD: {self.KD}\t KS:{self.KS}\t KW:{self.KW}\t KI:{self.KI}\t KD:{self.KD}"
        return string
