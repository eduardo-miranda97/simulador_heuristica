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

from Individuo import Individuo

class Simulator(Object):

    MAX_ITERATIONS = 1200

    def __init__(self, structure_map, wall_map, static_map, crowd_map, individuals, directory):

        self.structure_map = structure_map
        self.wall_map = wall_map
        self.static_map = static_map
        self.crowd_map = crowd_map
        self.individuals = individuals
        self.directory = directory # *********************************************
        self.iteration = 0
        # self.log = Log() ********************

            
    # def simulacao(self):
    #     while (not self.check_evacuated_individuals() and self.iteration < self.MAX_ITERATIONS):
    #         # self.desenhaMapa(self.iteration)
    #         self.iteration += 1

    #         self.sort_individuals_by_distance()

    #         for individual in self.individuals:
    #             # Increment the amount of steps for the individual to move based in individual's speed
    #             individual.steps += 1 
    #             if (not individual.evacuated):
    #                 if (individual.steps == individual.speed):

    #                     self.crowd_map.move_individual(individual)

    #                     if(self.structure_map.isSaida(individual.row, individual.col)):
    #                         individual.evacuated = True

    #                     individual.steps = 0

    #         #ao finalizar o movimento possivel de todos os individuos libera os individuos que chegaram a saida
    #         self.liberaSaidas()

    #         #depois dos movimentos eh realizado o calibramento do mapa dinamicos
    #         self.difusaoDecaimento(deepcopy(self.dinamic_map), self.dinamic_map)

    #     return self.iteration


    # def difusaoDecaimento(self, oldMapa, newMapa):
    #     for i in range(1, newMapa.__len__()-1):
    #         for j in range(1, newMapa[0].__len__()-1):
    #             newMapa[i][j] = oldMapa[i][j] + ((Util.DD_ALFA/4)*(oldMapa[i+1][j] + oldMapa[i-1][j] + oldMapa[i][j+1] + oldMapa[i][j-1] + 
    #                                                                oldMapa[i-1][j-1] + oldMapa[i-1][j+1] + oldMapa[i+1][j-1] + oldMapa[i+1][j+1]))
    #             newMapa[i][j] = oldMapa[i][j] - (Util.DD_SIGMA*oldMapa[i][j])

    # def liberaSaidas(self):
    #     #para cada saida neste mapa, todos os individuos nestas posicoes sao evacuados
    #     for mapa in self.listaMapas:
    #         for saida in mapa.saidas:
    #             mapa.mapa_individuo[saida[0]][saida[1]] = Util.M_VAZIO

    # def desenhaMapa(self, iteracao):
    #     #para cada mapa, desenha uma imagem do estado atual do mapa
    #     for mapa in self.listaMapas:
    #         mapa.desenhaMapa(iteracao, self.diretorioImagens, self.listaIndividuos)
    #         mapa.desenhaMapaTracing(iteracao, self.diretorioImagens)

    
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

