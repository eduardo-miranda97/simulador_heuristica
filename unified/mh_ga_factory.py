
from mh_ga_nsgaii import ChromosomeFactory, Chromosome
from sim_ca_scenario import Scenario
from sim_ca_simulator import Simulator

class Gene:

    def __init__(self, exits):
        self.exits = exits


class Factory(ChromosomeFactory):

    def decode(self, gene):
        scen = Scenario("cult_experiment",True,5,12)
        simulator = Simulator(scen)
        iterations, qtdDistance = simulator.simulate()
        return iterations, qtdDistance


    def build(self, generation, gene):
        solution = self.decode(gene)
        return Chromosome(generation, gene, list(solution))
    
