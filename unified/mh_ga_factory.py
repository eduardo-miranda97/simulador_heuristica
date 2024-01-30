
from heuristic.nsgaii.nsgaii import ChromosomeFactory


class Gene:

    def __init__(self, exits):
        self.exits = exits


class Factory(ChromosomeFactory):

    def decode(self, gene):
        scen = Scenario("cult_experiment",True,5,12)
        simulator = Simulator(scen)
        iterations, qtdDistance = simulator.simulate()
        return iterations, qtdDistance