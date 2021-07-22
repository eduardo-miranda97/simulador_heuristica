# -*- coding:utf-8 -*-

from colour import Color
from copy import deepcopy
from math import exp
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from random import randint
import re

from constants import Constants

class CrowdMap(object):
    """Responsable to control the individual's location in the map.


    Attributes
    ----------
    label : str
        The name of the crowd map.

    structure_map : StructureMap
        The structure map contains information about the physical map.

    map : list of list of int
        The map with the individual's location.

    len_row : int
        The horizontal size of the map.

    len_col : int
        The vertical size of the map.

    Methods
    -------
    load_map(individuals)
        Based on the structure map the crowd map is started to be constructed.

    place_individuals(individuals)
        Based on the structure map the individuals are placed in the crowd map.

    draw_map(directory, iteration)
        Draw the crowd map using the individual's location.
        
    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    def __init__(self, label, structure_map):
        self.label = label
        self.structure_map = structure_map
        self.map = []
        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

    def load_map(self, individuals):
        """Based on the structure map and individuals, the crowd map is constructed.

        Parameters
        ----------
        individuals : list of Individual
            Contains specific information about individuals.
        """
        self.map = []

        self.map = [[0] * self.len_col for _ in range(self.len_row)]
        self.place_individuals(individuals)

    def place_individuals(self, individuals):
        """Based on the structure map the individuals are placed in the crowd map.

        Parameters
        ----------
        individuals : list of Individual
            Contains specific information about individuals.
        """        
        empty_positions = self.structure_map.get_empty_positions()
        for individual in individuals:
            individual.row, individual.col = empty_positions.pop(randint(0, len(empty_positions) - 1))
            self.map[individual.row][individual.col] = individual

    def check_empty_position(self, row, col):
        """Check if a position in the map is empty

        Parameters
        ----------
        row : int
            Row index.
        col : int
            Column index.
            
        Returns
        -------
        boolean
            Returns True for empty position
        """
        if (self.map[row][col] == 0):
            return True
        return False

    def update_individual_position(self, original_row, original_col, new_row, new_col):
        """Update the position of an individual

        Parameters
        ----------
        original_row : int
            Row of the map that the individual was.
        original_col : int
            Column of the map that the individual was.
        new_row : int
            Row of the map that the individual will be.
        new_col : int
            Column of the map that the individual will be.
        """  
        self.map[new_row][new_col] = self.map[original_row][original_row]
        self.map[original_row][original_row] = 0

    def free_exit_gates(self):
        return

    
    # ''' Funcao que vai fazer o movimento do individuo, chamara a propria funcao do individuo
    # para que ele descubra para onde ira se mover
    # '''
    # def move_individual(self, individual):
    #     linha    = individual.linha
    #     coluna   = individual.coluna
    #     campoMov = [0,0,0,0,0,0,0,0,0]
    #     campoMov = self.calculaProbabilidadesMovimentoBruto(linha, coluna, individual, campoMov)
    #     #Normalizacao
    #     total = self.calculaTotalNormalizacao(campoMov)
    #     campoMov = self.calculaProbabilidadesMovimentoNormalizado(campoMov, total)
    #     caminho = self.sorteiaCaminhoDestino(campoMov)
    #     resp = self.converteDirecao(individual, caminho)
    #     direcao = resp[0]
    #     caminho = resp[1]
    #     #atualiza no mapa o individuo
    #     if(caminho[1] != linha or caminho[2] != coluna):
    #         if(self.listaMapas[individual.idMapa].verificaMovimentoValido(caminho[1], caminho[2])):
    #             self.MovsPerIter = self.MovsPerIter + 1
    #             #atualiza os dados no mapa de individuos
    #             self.listaMapas[individual.idMapa].mapa_individuo[caminho[1]][caminho[2]] = Util.M_INDIVIDUO
    #             self.listaMapas[individual.idMapa].mapa_individuo[linha][coluna]  = Util.M_VAZIO
    #             self.listaMapas[individual.idMapa].mapa_dinamico1[linha][coluna] += 1
    #             #atualiza nos dados do individuo sua posicao
    #             individual.linha  = caminho[1]
    #             individual.coluna = caminho[2]
    #             individual.ultimaDirecao = direcao
    #             individual.movimentosFeitos += 1
    #     else:
    #         individual.movimentosWaiting += 1



    def draw_map(self, directory, iteration):
        """Draw the crowd map using the structe map and the individuals colors.

        Parameters
        ----------
        directory : str
            Contain the directory that the image will be saved.

        iteration : int
            Number of the iteration.
        """
        field_size = 20
        image = Image.new("RGB", (field_size * self.len_col, field_size * self.len_row), Constants.C_WHITE)
        draw = ImageDraw.Draw(image)

        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.structure_map.map[i][j] == Constants.M_WALL):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), Constants.C_BLACK, Constants.C_BLACK)
                elif (self.structure_map.map[i][j] == Constants.M_OBJECT):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), Constants.C_GRAY, Constants.C_GRAY)
                elif (self.structure_map.map[i][j] == Constants.M_VOID):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), Constants.C_LIGHT_BLACK, Constants.C_LIGHT_BLACK)
                elif (self.structure_map.map[i][j] == Constants.M_EMPTY):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), Constants.C_WHITE, Constants.C_BLACK)             
                elif (self.structure_map.map[i][j] == Constants.M_DOOR):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), Constants.C_RED, Constants.C_BLACK)
                if (self.map[i][j] != 0): # If the field have an individual
                    if (self.structure_map.map[i][j] != Constants.M_DOOR):
                        draw.ellipse((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), self.map[i][j].color, Constants.C_BLACK) 
        
        image_name = directory + "/" + self.label + "_crowd_map_" + str(iteration) + ".png"
        image.save(image_name)