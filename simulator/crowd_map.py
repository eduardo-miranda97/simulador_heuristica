# -*- coding:utf-8 -*-

from colour import Color
from copy import deepcopy
from math import exp
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
import re

class CrowdMap(object):
    """Responsable to control the individual's location in the map.

    ...

    Attributes
    ----------
    label : str
        The name of the crowd map.
    map : list of list of int
        The map with the individual's location.
    len_row : int
        The horizontal size of the map.
    len_col : int
        The vertical size of the map.

    Methods
    -------
    load_crowd_map(structure_map)
        Based on the structure map the crowd map is started to be constructed.
    draw_crowd_map(directory)
        Draw the crowd map using the individual's location.

    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    # Object Map Constant
    M_EMPTY = 0
    M_WALL = 1
    M_DOOR = 2
    M_INDIVIDUAL = 5
    M_OBJECT = 6
    M_VOID = 8

    def __init__(self, label):
        self.label = label
        self.map = []
        self.len_row = 0
        self.len_col = 0

    def load_crowd_map(self, structure_map):
        """Based on the structure map the crowd map is started to be constructed.

        Parameters
        ----------
        structure_map : StructureMap
            The structure map that contains the informations of the map.
        """
        self.map = []
        self.len_row = structure_map.len_row
        self.len_col = structure_map.len_col

        matrix = [[0] * self.len_col for _ in range(len_row)]
        
        

    def geraIndividuosAleatoriamente(self):
        #ao iniciar uma simulacao gera a posicao individuos em posicoes aleatorioas em mapas aleatorios
        #print("Carregando "+str(self.dados.QTD_PESSOAS)+" Individuos Aleatoriamente")
        
        for i in range(self.dados.QTD_PESSOAS):

            idMapa = randint(0, self.listaMapas.__len__()-1)
            coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
            linha  = randint(0, self.listaMapas[idMapa].tam_linhas-1)
            
            while(not self.verificaPosicaoVazia(idMapa, coluna, linha)):
                idMapa = randint(0, self.listaMapas.__len__()-1)
                coluna = randint(0, self.listaMapas[idMapa].tam_colunas-1)
                linha = randint(0, self.listaMapas[idMapa].tam_linhas-1)

            self.listaIndividuos[i].posicionaIndividuoMapa(coluna, linha, idMapa)

            #self.listaMapas[idMapa].mapa_individuo[linha][coluna] = Util.M_INDIVIDUO
            
            #print("Individuo Gerado | Mapa: " + str(idMapa) + " Linha: " + str(linha) + " Coluna: " + str(coluna))
        #self.listaIndividuosInicial.append(deepcopy(self.listaIndividuos))
        #for i in range(self.dados.DIRETORIO_MAPAS.__len__()):
            #self.listaMapasIndividuosInicial.append(deepcopy(self.listaMapas[i].mapa_individuo))
            #print("Mapa: "+ str(i))
            #self.listaMapas[i].imprimeMapaIndividuo()
            #self.listaMapas[i].imprimeMapaParedes()
    
    def atribuiMapaIndividuoInicial(self):
        
        for ind in self.listaIndividuos:
            self.listaMapas[ind.idMapa].mapa_individuo[ind.linha][ind.coluna] = Util.M_INDIVIDUO