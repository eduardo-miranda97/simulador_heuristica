# -*- coding:utf-8 -*-

class Individual(object):

    def __init__(self, configuration, col, row):
        self.label = configuration["label"]
        self.color = (configuration["red"], configuration["green"], configuration["blue"])
        self.speed = configuration["speed"]
        self.KD = configuration["KD"] # Dinamic map const
        self.KS = configuration["KS"] # Static map const
        self.KW = configuration["KW"] # Wall map const
        self.KI = configuration["KI"] # Inertia const

        self.row = row
        self.col = col
        self.evacuated = False
        self.steps = 0

    # def calculaProbabilidadesMovimentoBruto(self, linha, coluna, individual, campoMov):
    #     if(self.listaMapas[individual.idMapa].qtdSaidasVizinhas(linha, coluna) == 0):  
    #         #superior esquerdo - individual 0
    #         campoMov[Util.C_SE] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna-1, Util.C_SE, individual)
    #         #superior direito - individual 1
    #         campoMov[Util.C_SD] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna+1, Util.C_SD, individual)
    #         #inferior direito - individual 2
    #         campoMov[Util.C_ID] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna+1, Util.C_ID, individual)
    #         #inferior esquerdo - individual 3
    #         campoMov[Util.C_IE] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna-1, Util.C_IE, individual)
    #         #topo - individual 4
    #         campoMov[Util.C_TO] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha-1, coluna,   Util.C_TO, individual)
    #         #baixo - individual 5
    #         campoMov[Util.C_BA] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha+1, coluna,   Util.C_BA, individual)
    #         #esquerdo - individual 6
    #         campoMov[Util.C_ES] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna-1,   Util.C_ES, individual)
    #         #direito - individual 7
    #         campoMov[Util.C_DI] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna+1,   Util.C_DI, individual)
    #         #meio - individual 8
    #         campoMov[Util.C_ME] = self.listaMapas[individual.idMapa].calculaValorMovimentoBruto(linha, coluna,     Util.C_ME, individual)
    #     else:
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna-1)):
    #             campoMov[Util.C_SE] = 1
    #         else:
    #             campoMov[Util.C_SE] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna+1)):
    #             campoMov[Util.C_SD] = 1
    #         else:
    #             campoMov[Util.C_SD] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna+1)):
    #             campoMov[Util.C_ID] = 1
    #         else:
    #             campoMov[Util.C_ID] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna-1)):
    #             campoMov[Util.C_IE] = 1
    #         else:
    #             campoMov[Util.C_IE] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha-1, coluna)):
    #             campoMov[Util.C_TO] = 1
    #         else:
    #             campoMov[Util.C_TO] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha+1, coluna)):
    #             campoMov[Util.C_BA] = 1
    #         else:
    #             campoMov[Util.C_BA] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha, coluna-1)):
    #             campoMov[Util.C_ES] = 1
    #         else:
    #             campoMov[Util.C_ES] = 0
    #         if(self.listaMapas[individual.idMapa].isSaidaVazia(linha, coluna+1)):
    #             campoMov[Util.C_DI] = 1
    #         else:
    #             campoMov[Util.C_DI] = 0
    #         campoMov[Util.C_ME] = 0
            
    #     return campoMov
    
    # def calculaTotalNormalizacao(self, campoMov):
    #     total = campoMov[Util.C_SE] + campoMov[Util.C_SD] + campoMov[Util.C_ID] + campoMov[Util.C_IE] + campoMov[Util.C_TO]
    #     return total + campoMov[Util.C_BA] + campoMov[Util.C_ES] + campoMov[Util.C_DI] + campoMov[Util.C_ME]
    
    # def calculaProbabilidadesMovimentoNormalizado(self, campoMov, total):
    #     if(total==0):
    #         campoMov[Util.C_SE] = 0
    #         campoMov[Util.C_SD] = 0
    #         campoMov[Util.C_ID] = 0
    #         campoMov[Util.C_IE] = 0
    #         campoMov[Util.C_TO] = 0
    #         campoMov[Util.C_BA] = 0
    #         campoMov[Util.C_ES] = 0
    #         campoMov[Util.C_DI] = 0
    #         campoMov[Util.C_ME] = 0
    #     else:
    #         campoMov[Util.C_SE] = campoMov[Util.C_SE]/total
    #         campoMov[Util.C_SD] = campoMov[Util.C_SE] + campoMov[Util.C_SD]/total
    #         campoMov[Util.C_ID] = campoMov[Util.C_SD] + campoMov[Util.C_ID]/total
    #         campoMov[Util.C_IE] = campoMov[Util.C_ID] + campoMov[Util.C_IE]/total
    #         campoMov[Util.C_TO] = campoMov[Util.C_IE] + campoMov[Util.C_TO]/total
    #         campoMov[Util.C_BA] = campoMov[Util.C_TO] + campoMov[Util.C_BA]/total
    #         campoMov[Util.C_ES] = campoMov[Util.C_BA] + campoMov[Util.C_ES]/total
    #         campoMov[Util.C_DI] = campoMov[Util.C_ES] + campoMov[Util.C_DI]/total
    #         campoMov[Util.C_ME] = campoMov[Util.C_DI] + campoMov[Util.C_ME]/total
    #     return campoMov

    # def sorteiaCaminhoDestino(self, campoMov):
    #     ini = 0
    #     sort = randint(0, 100)/100
    #     for i in range(campoMov.__len__()):
    #         if(sort < campoMov[i] and sort > ini):
    #             return i
    #         ini = campoMov[i]

    # def converteDirecao(self, individual, caminho):
    #     #Retorna ["direcao","[caminho]"]
    #     linha    = individual.linha
    #     coluna   = individual.coluna
    #     direcao  = 0
    #     if(caminho == Util.C_SE):
    #         linha   = linha-1
    #         coluna  = coluna-1
    #         direcao = Util.C_SE
    #     if(caminho == Util.C_SD):
    #         linha   = linha-1
    #         coluna  = coluna+1
    #         direcao = Util.C_SD
    #     if(caminho == Util.C_ID):
    #         linha   = linha+1
    #         coluna  = coluna+1
    #         direcao = Util.C_ID
    #     if(caminho == Util.C_IE):
    #         linha   = linha+1
    #         coluna  = coluna-1
    #         direcao = Util.C_IE
    #     if(caminho == Util.C_TO):
    #         linha   = linha-1
    #         coluna  = coluna
    #         direcao = Util.C_TO
    #     if(caminho == Util.C_BA):
    #         linha   = linha+1
    #         coluna  = coluna
    #         direcao = Util.C_BA
    #     if(caminho == Util.C_ES):
    #         linha   = linha
    #         coluna  = coluna-1
    #         direcao = Util.C_ES
    #     if(caminho == Util.C_DI):
    #         linha   = linha
    #         coluna  = coluna+1   
    #         direcao = Util.C_DI 
    #     return [direcao, [self.listaMapas[individual.idMapa].mapa_estatico[linha][coluna], linha, coluna]]

    def __str__(self):
        string = f"Label: {self.label}\t R:{self.red}\t G:{self.green}\t B:{self.blue}\t Speed:{self.speed}\t"
        string += f"KD: {self.KD}\t KS:{self.KS}\t KW:{self.KW}\t KI:{self.KI}\t KD:{self.KD}"
        return string
