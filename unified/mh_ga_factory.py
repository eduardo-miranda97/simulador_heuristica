
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
        gene_size = len(parent_a.configuration)
        qtd_mut = max(int(gene_size * 0.3), 1)
        
        child1 = [0] * gene_size
        child2 = [0] * gene_size
        for i in range(gene_size):
            child1[i] = parent_a.configuration
            child2[i] = parent_b.configuration

        for i in range(qtd_mut):
            i = randint(0, gene_size)
            child1[i] = not child1[i]
            i = randint(0, gene_size)
            child2[i] = not child2[i]

        return Gene(child1), Gene(child2)


    def mutate(self, gene):
        qtd_mut = max(int(len(gene.configuration) * 0.1), 1)
        for _ in range(qtd_mut):
            i = randint(0, len(gene.configuration))
            gene.configuration[i] = not gene.configuration[i]

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