# -*- coding:utf-8 -*-


from random import randint
from numpy import random
from copy import deepcopy
from tkinter import Frame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import datetime
import time

class Simulator(object):

    MAX_ITERATIONS = 1200

    def __init__(self, structure_map, wall_map, static_map, crowd_map, dinamic_map, individuals, directory):

        self.structure_map = structure_map
        self.wall_map = wall_map
        self.static_map = static_map
        self.crowd_map = crowd_map
        self.dinamic_map = dinamic_map
        self.individuals = individuals
        self.directory = directory # *********************************************
        self.iteration = 0
        # self.log = Log() ********************
    

    def simulate(self):
        while (not self.check_evacuated_individuals() and self.iteration < self.MAX_ITERATIONS):
            self.crowd_map.draw_map("../output/" + self.directory, self.individuals, self.iteration)
            self.dinamic_map.draw_map(self.directory, self.iteration)
            self.iteration += 1

            self.sort_individuals_by_distance()

            for individual in self.individuals:
                # Increment the amount of steps for the individual to move based in individual's speed
                individual.steps += 1 
                if (not individual.evacuated):
                    if (individual.steps == individual.speed):

                        self.individual.move(self.structure_map, self.wall_map, self.static_map, self.crowd_map, self.dinamic_map)

                        if(self.structure_map.isSaida(individual.row, individual.col)):
                            individual.evacuated = True

                        individual.steps = 0

            # After moving all the individuals free the exit gates that are occupied
            self.crowd_map.free_exit_gates()

            # After the iteration it's recalculed the pheromone map
            self.dinamic_map.difusion_decay()

        return self.iteration
    
    # Pode ser melhorado, remover o individuo da lista ganha em processamento ***********************************
    def check_evacuated_individuals(self):
        for i in range(len(self.individuals)):
            if (not self.individuals[i].evacuated):
                return False
        return True
        
    def sort_individuals_by_distance(self):
        #a ordenacao eh util para que os movimentos dos individuos sejam feitas pelas distancias mais proximas
        self.individuals.sort(key = self.individual_exit_distance, reverse = False)

    def individual_exit_distance(self, individual):
        # retorna distancia da porta
        return self.static_map[individual.row][individual.col]

