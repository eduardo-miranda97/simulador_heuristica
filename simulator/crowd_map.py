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

    draw_map(directory)
        Draw the crowd map using the individual's location.

    place_individuals(individuals)
        
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
        

    # def geraIndividuosAleatoriamente(self, individuals):
    #     #ao iniciar uma simulacao gera a posicao individuos em posicoes aleatorioas em mapas aleatorios
    #     #print("Carregando "+str(self.dados.QTD_PESSOAS)+" Individuos Aleatoriamente")
        
    #     for i in range(self.dados.QTD_PESSOAS):

    #         idMapa = randint(0, self.listaMapas.__len__()-1)
    #         coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
    #         linha  = randint(0, self.listaMapas[idMapa].tam_linhas-1)
            
    #         while(not self.verificaPosicaoVazia(idMapa, coluna, linha)):
    #             idMapa = randint(0, self.listaMapas.__len__()-1)
    #             coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
    #             linha = randint(0, self.listaMapas[idMapa].tam_linhas-1)

    #         self.listaIndividuos[i].posicionaIndividuoMapa(coluna, linha, idMapa)

    #         #self.listaMapas[idMapa].mapa_individuo[linha][coluna] = Util.M_INDIVIDUO
            
    #         #print("Individuo Gerado | Mapa: " + str(idMapa) + " Linha: " + str(linha) + " Coluna: " + str(coluna))
    #     #self.listaIndividuosInicial.append(deepcopy(self.listaIndividuos))
    #     #for i in range(self.dados.DIRETORIO_MAPAS.__len__()):
    #         #self.listaMapasIndividuosInicial.append(deepcopy(self.listaMapas[i].mapa_individuo))
    #         #print("Mapa: "+ str(i))
    #         #self.listaMapas[i].imprimeMapaIndividuo()
    #         #self.listaMapas[i].imprimeMapaParedes()
    
    # def atribuiMapaIndividuoInicial(self):
        
    #     for ind in self.listaIndividuos:
    #         self.listaMapas[ind.idMapa].mapa_individuo[ind.linha][ind.coluna] = Util.M_INDIVIDUO


    
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



    def draw_map(self, directory, individuals):
        """Draw the crowd map using the structe map and the individuals colors.

        Parameters
        ----------
        directory : str
            Contain the directory that the image will be saved.

        individuals : list of Individual
            Contains specific information about individuals.
        """
        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (192, 192, 192)
        red = (255, 0, 0)
        field_size = 20
        image = Image.new("RGB", (field_size * self.len_col, field_size * self.len_row), white)
        draw = ImageDraw.Draw(image)

        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.structure_map.map[i][j] == Constants.M_WALL):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), black, black)
                elif (self.structure_map.map[i][j] == Constants.M_VOID):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), gray, black)
                elif (self.structure_map.map[i][j] == Constants.M_EMPTY):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), white, black)             
                elif (self.structure_map.map[i][j] == Constants.M_DOOR):
                    draw.rectangle((j * field_size, i * field_size, (j + 1) * field_size, (i + 1) * field_size), red, black)
        for individual in individuals:
            if (self.structure_map.map[individual.row][individual.col] != Constants.M_DOOR):
                draw.ellipse((individual.col * field_size, individual.row * field_size, (individual.col + 1) * field_size, (individual.row + 1) * field_size), individual.color, black)
                        
        image_name = directory + "/" + self.label + "_crowd_map.png"
        image.save(image_name)