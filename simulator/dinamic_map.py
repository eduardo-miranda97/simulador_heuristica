
from copy import deepcopy
from math import exp 

from constants import Constants

class DinamicMap(object):
    """Responsable to control the individual's tracing in the map.


    Attributes
    ----------
    label : str
        The name of the dinamic map.

    structure_map : StructureMap
        The structure map contains information about the physical map.

    map : list of list of int *******************************************************************************************
        The map with the individual's location.*************************************************************

    len_row : int
        The horizontal size of the map.

    len_col : int
        The vertical size of the map.

    Methods
    -------
    
        
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

    
    def load_map(self):
        for i in range(self.len_row):
            self.map.append([])
            for _ in range(self.len_col):
                self.map[i].append(0)

    def draw_map(self, directory, iteration):

        return


    def difusion_decay(self):
        aux_map = deepcopy(self.map)
        for i in range(1, len(self.map)):
            for j in range(1, len(self.map)):
                aux_map[i][j] = ((1 - Constants.DIFUSIONDECAY_ALFA) * (1 - Constants.DIFUSIONDECAY_SIGMA) *
                    self.map[i][j] + Constants.DIFUSIONDECAY_ALFA  * (1 - Constants.DIFUSIONDECAY_SIGMA) / 8 *
                    (aux_map[i + 1][j] + aux_map[i][j + 1] + aux_map[i - 1][j] + aux_map[i][j - 1] +
                    aux_map[i + 1][j + 1] + aux_map[i + 1][j - 1] + aux_map[i - 1][j + 1] + aux_map[i - 1][j - 1]))
        return


    def calc_dinamic_value(self, row, col, individual_KW):
        return 1
        # return exp(individual_KW * self.map[row][col])

    # def difusaoDecaimento(self, oldMapa, newMapa):
    #     for i in range(1, newMapa.__len__()-1):
    #         for j in range(1, newMapa[0].__len__()-1):
    #             newMapa[i][j] = oldMapa[i][j] + ((Util.DD_ALFA/4)*(oldMapa[i+1][j] + oldMapa[i-1][j] + oldMapa[i][j+1] + oldMapa[i][j-1] + 
    #                                                                oldMapa[i-1][j-1] + oldMapa[i-1][j+1] + oldMapa[i+1][j-1] + oldMapa[i+1][j+1]))
    #             newMapa[i][j] = oldMapa[i][j] - (Util.DD_SIGMA*oldMapa[i][j])