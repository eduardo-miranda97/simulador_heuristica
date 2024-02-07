
from mh_ga_nsgaii import ChromosomeFactory, Chromosome
from sim_ca_scenario import Scenario
from sim_ca_simulator import Simulator

from random import choice, randint, sample

class Gene:

    def __init__(self, configuration):
        self.configuration = configuration


class Factory(ChromosomeFactory):

    def __init__(self, instance):
        super().__init__(instance)
        scen = Scenario(instance.experiment)
        self.exits = scen.doors_configurations


    def decode(self, gene):
        doors = []
        for i in range(len(gene.configuration)):
            if gene.configuration[i]:
                doors.append(self.exits[i])

        scen = Scenario(self.instance.experiment, doors, self.instance.draw,
                        self.instance.scenario_seed, self.instance.simulation_seed)
        simulator = Simulator(scen)
        iterations, qtdDistance = simulator.simulate()
        print(f"Portas: {len(doors)}, Iter: {iterations}, Dist: {qtdDistance}")
        return len(doors), iterations, qtdDistance


    def build(self, generation, gene):
        solution = self.decode(gene)
        return Chromosome(generation, gene, list(solution))


    def new(self):
        return Gene([choice([True, False]) for _ in range(len(self.exits))])
        # return Gene(sample(self.exits))


    def crossover(self, parent_a, parent_b):
        child = [0] * len(parent_a.configuration)
        for i in range(len(parent_a.configuration)):
            child[i] = parent_a.configuration[i] and parent_b.configuration[i]
        
        count_a = parent_a.configuration.count(True)
        count_b = parent_b.configuration.count(True)
        count_c = child.count(True)

        if (count_c == count_a and count_a > count_b) or (count_c == count_b and count_a <= count_b):
            j = randint(0, len(parent_a.configuration) - 1)
            while not child[j]:
                j = randint(0, len(parent_a.configuration) - 1)
            child[j] = False

        return Gene(child)


    def mutate(self, gene):
        start_mutation = randint(0, len(gene.configuration) - 2)
        aux = gene.configuration[start_mutation]
        i = start_mutation
        while i != len(gene.configuration) - 2:
            gene.configuration[i] = gene.configuration[i + 1]
            i += 1
        gene.configuration[i] = aux

        return gene


    def uncode(self, gene):
        doors = []
        for i in range(len(gene.configuration)):
            if gene.configuration[i]:
                doors.append(self.exits[i])
        return doors


def selector(population):
    """Tournament selection."""
    pool = sample(population, 4)
    pool.sort()
    return pool[0], pool[1]