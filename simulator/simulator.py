# -*- coding:utf-8 -*-


from random import randint
from numpy import random
from copy import deepcopy
from Individuo import Individuo
from tkinter import Frame
from Util import Util
from Mapa import Mapa
from Logs import Logs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import os
import datetime
import time

#from PIL import Image
#from PIL import ImageDraw
#from tkinter import Button
#from tkinter import Canvas
#import time

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

            
    def simulacao(self):
        while (not self.check_evacuated_individuals() and self.iteration < self.MAX_ITERATIONS):
            # self.desenhaMapa(self.iteration)
            self.iteration += 1

            self.sort_individuals_by_distance()

            for individual in self.individuals:
                # Increment the amount of steps for the individual to move based in individual's speed
                individual.steps += 1 
                if (not individual.evacuated):
                    if (individual.steps == individual.speed):

                        self.moveIndividuo(individual)

                        if(self.structure_map.isSaida(individual.row, individual.col)):

                            individual.evacuated = True

                        individual.steps = 0

            #ao finalizar o movimento possivel de todos os individuos libera os individuos que chegaram a saida
            self.liberaSaidas()

            #depois dos movimentos eh realizado o calibramento do mapa dinamicos
            self.difusaoDecaimento(deepcopy(self.dinamic_map), self.dinamic_map)

        return self.iteration


    def difusaoDecaimento(self, oldMapa, newMapa):
        for i in range(1, newMapa.__len__()-1):
            for j in range(1, newMapa[0].__len__()-1):
                newMapa[i][j] = oldMapa[i][j] + ((Util.DD_ALFA/4)*(oldMapa[i+1][j] + oldMapa[i-1][j] + oldMapa[i][j+1] + oldMapa[i][j-1] + 
                                                                   oldMapa[i-1][j-1] + oldMapa[i-1][j+1] + oldMapa[i+1][j-1] + oldMapa[i+1][j+1]))
                newMapa[i][j] = oldMapa[i][j] - (Util.DD_SIGMA*oldMapa[i][j])


    def moveIndividuo(self, individual):
        linha    = individual.linha
        coluna   = individual.coluna
        campoMov = [0,0,0,0,0,0,0,0,0]
        campoMov = self.calculaProbabilidadesMovimentoBruto(linha, coluna, individual, campoMov)
        #Normalizacao
        total = self.calculaTotalNormalizacao(campoMov)
        campoMov = self.calculaProbabilidadesMovimentoNormalizado(campoMov, total)
        caminho = self.sorteiaCaminhoDestino(campoMov)
        resp = self.converteDirecao(individual, caminho)
        direcao = resp[0]
        caminho = resp[1]
        #atualiza no mapa o individuo
        if(caminho[1] != linha or caminho[2] != coluna):
            if(self.listaMapas[individual.idMapa].verificaMovimentoValido(caminho[1], caminho[2])):
                self.MovsPerIter = self.MovsPerIter + 1
                #atualiza os dados no mapa de individuos
                self.listaMapas[individual.idMapa].mapa_individuo[caminho[1]][caminho[2]] = Util.M_INDIVIDUO
                self.listaMapas[individual.idMapa].mapa_individuo[linha][coluna]  = Util.M_VAZIO
                self.listaMapas[individual.idMapa].mapa_dinamico1[linha][coluna] += 1
                #atualiza nos dados do individuo sua posicao
                individual.linha  = caminho[1]
                individual.coluna = caminho[2]
                individual.ultimaDirecao = direcao
                individual.movimentosFeitos += 1
        else:
            individual.movimentosWaiting += 1

    def calculaProbabilidadesMovimentoBruto(self, linha, coluna, individual, campoMov):
        if(self.listaMapas[individual.idMapa].qtdSaidasVizinhas(linha, coluna) == 0):  
            #superior esquerdo - individual 0
            campoMov[Util.C_SE] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna-1, Util.C_SE, individual)
            #superior direito - individual 1
            campoMov[Util.C_SD] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna+1, Util.C_SD, individual)
            #inferior direito - individual 2
            campoMov[Util.C_ID] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna+1, Util.C_ID, individual)
            #inferior esquerdo - individual 3
            campoMov[Util.C_IE] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna-1, Util.C_IE, individual)
            #topo - individual 4
            campoMov[Util.C_TO] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna,   Util.C_TO, individual)
            #baixo - individual 5
            campoMov[Util.C_BA] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna,   Util.C_BA, individual)
            #esquerdo - individual 6
            campoMov[Util.C_ES] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna-1,   Util.C_ES, individual)
            #direito - individual 7
            campoMov[Util.C_DI] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna+1,   Util.C_DI, individual)
            #meio - individual 8
            campoMov[Util.C_ME] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna,     Util.C_ME, individual)
        else:
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna-1)):
                campoMov[Util.C_SE] = 1
            else:
                campoMov[Util.C_SE] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna+1)):
                campoMov[Util.C_SD] = 1
            else:
                campoMov[Util.C_SD] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna+1)):
                campoMov[Util.C_ID] = 1
            else:
                campoMov[Util.C_ID] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna-1)):
                campoMov[Util.C_IE] = 1
            else:
                campoMov[Util.C_IE] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna)):
                campoMov[Util.C_TO] = 1
            else:
                campoMov[Util.C_TO] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna)):
                campoMov[Util.C_BA] = 1
            else:
                campoMov[Util.C_BA] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha, coluna-1)):
                campoMov[Util.C_ES] = 1
            else:
                campoMov[Util.C_ES] = 0
            if(self.listaMapas[individual.idMapa].isSaidaVazia(linha, coluna+1)):
                campoMov[Util.C_DI] = 1
            else:
                campoMov[Util.C_DI] = 0
            campoMov[Util.C_ME] = 0
            
        return campoMov
    
    def calculaTotalNormalizacao(self, campoMov):
        total = campoMov[Util.C_SE] + campoMov[Util.C_SD] + campoMov[Util.C_ID] + campoMov[Util.C_IE] + campoMov[Util.C_TO]
        return total + campoMov[Util.C_BA] + campoMov[Util.C_ES] + campoMov[Util.C_DI] + campoMov[Util.C_ME]
    
    def calculaProbabilidadesMovimentoNormalizado(self, campoMov, total):
        if(total==0):
            campoMov[Util.C_SE] = 0
            campoMov[Util.C_SD] = 0
            campoMov[Util.C_ID] = 0
            campoMov[Util.C_IE] = 0
            campoMov[Util.C_TO] = 0
            campoMov[Util.C_BA] = 0
            campoMov[Util.C_ES] = 0
            campoMov[Util.C_DI] = 0
            campoMov[Util.C_ME] = 0
        else:
            campoMov[Util.C_SE] = campoMov[Util.C_SE]/total
            campoMov[Util.C_SD] = campoMov[Util.C_SE] + campoMov[Util.C_SD]/total
            campoMov[Util.C_ID] = campoMov[Util.C_SD] + campoMov[Util.C_ID]/total
            campoMov[Util.C_IE] = campoMov[Util.C_ID] + campoMov[Util.C_IE]/total
            campoMov[Util.C_TO] = campoMov[Util.C_IE] + campoMov[Util.C_TO]/total
            campoMov[Util.C_BA] = campoMov[Util.C_TO] + campoMov[Util.C_BA]/total
            campoMov[Util.C_ES] = campoMov[Util.C_BA] + campoMov[Util.C_ES]/total
            campoMov[Util.C_DI] = campoMov[Util.C_ES] + campoMov[Util.C_DI]/total
            campoMov[Util.C_ME] = campoMov[Util.C_DI] + campoMov[Util.C_ME]/total
        return campoMov

    def sorteiaCaminhoDestino(self, campoMov):
        ini = 0
        sort = randint(0, 100)/100
        for i in range(campoMov.__len__()):
            if(sort < campoMov[i] and sort > ini):
                return i
            ini = campoMov[i]

    def converteDirecao(self, individual, caminho):
        #Retorna ["direcao","[caminho]"]
        linha    = individual.linha
        coluna   = individual.coluna
        direcao  = 0
        if(caminho == Util.C_SE):
            linha   = linha-1
            coluna  = coluna-1
            direcao = Util.C_SE
        if(caminho == Util.C_SD):
            linha   = linha-1
            coluna  = coluna+1
            direcao = Util.C_SD
        if(caminho == Util.C_ID):
            linha   = linha+1
            coluna  = coluna+1
            direcao = Util.C_ID
        if(caminho == Util.C_IE):
            linha   = linha+1
            coluna  = coluna-1
            direcao = Util.C_IE
        if(caminho == Util.C_TO):
            linha   = linha-1
            coluna  = coluna
            direcao = Util.C_TO
        if(caminho == Util.C_BA):
            linha   = linha+1
            coluna  = coluna
            direcao = Util.C_BA
        if(caminho == Util.C_ES):
            linha   = linha
            coluna  = coluna-1
            direcao = Util.C_ES
        if(caminho == Util.C_DI):
            linha   = linha
            coluna  = coluna+1   
            direcao = Util.C_DI 
        return [direcao, [self.listaMapas[individual.idMapa].mapa_estatico[linha][coluna], linha, coluna]]

    def liberaSaidas(self):
        #para cada saida neste mapa, todos os individuos nestas posicoes sao evacuados
        for mapa in self.listaMapas:
            for saida in mapa.saidas:
                mapa.mapa_individuo[saida[0]][saida[1]] = Util.M_VAZIO

    def desenhaMapa(self, iteracao):
        #para cada mapa, desenha uma imagem do estado atual do mapa
        for mapa in self.listaMapas:
            #Recalcula o mapa estatico a cada 20 iteracoes
            if iteracao == 0:
               mapa.desenhaDistribuicaoMapaBanner(self.diretorioImagens,iteracao)

            else:
                if iteracao % Util.QTD_ITER_CALC_CAMPO_STATICO == 0:
                    #mapa.calculaMapaEstaticoAndCalor([],Util.ESTATICO_MAPA)
                    if self.dados.FLAG_ATIVACAO_FOGO:
                        mapa.calculaMapaEstatico()
                    mapa.desenhaDistribuicaoMapaBanner(self.diretorioImagens,iteracao)

            mapa.desenhaMapa(iteracao, self.diretorioImagens, self.listaIndividuos)
            mapa.desenhaMapaTracing(iteracao, self.diretorioImagens)
            if self.dados.FLAG_ATIVACAO_FOGO:
                mapa.desenhaMapaFogo(iteracao, self.diretorioImagens)
    
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

    
    def sorteiaNaRoleta(self, roletaProbabilidades):
        ini = 0
        sort = randint(0, 100)/100
        for i in range(roletaProbabilidades.__len__()):
            if(sort <= roletaProbabilidades[i] and sort >= ini):
                return i
            ini = roletaProbabilidades[i]
             
    def verificaPosicaoVazia(self, idMapa, coluna, linha):
        #verifica se a posicao nao eh referente a um local que contenha um objeto, 
        #ou se existe alguma pessoa naquele local
        if(self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_VAZIO or self.listaMapas[idMapa].mapa_objetos[linha][coluna] == Util.M_DESENHO):
            if(self.listaMapas[idMapa].mapa_individuo[linha][coluna] == Util.M_VAZIO):
                return True
        return False

