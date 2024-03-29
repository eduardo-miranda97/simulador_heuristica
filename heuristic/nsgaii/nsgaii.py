"""Generic NSGA-II interface.

The nondominated sort genetic algorithm II is a multi-objective evolutionary
algorithm aimed to solve optimization problems. Using a fast non dominated
sorting algorithm and a operation that requires no user defined parameter this
can be used to solve any kind of multi-objective optimization problem.
"""

import ctypes
import numpy as np


class Chromosome:
    """Object representing an individual.

    Genetic algorithms use the concept of population of solutions to represent
    it's search space. Each individual of the population stands for a unique
    solution carrying a gene that can be decoded into a real solution.

    The gene can be any kind of object as long as it can be decoded into a
    solution.

    Parameters
    ----------
    gene: object
        Abstract representation for a solution
    obj: list of float
        The evaluation of each objective function for this indivual.

    Attributes
    ----------
    generation: int
        The generation that this individual was born.
    gene: object
        Abstract representation for a solution.
    obj: list of float
        The evaluation of each objective function for this indivual.
    rank: int
        The front on which this indiviual is.
    dist: float
        The crowded distance of this individual.
    """

    def __init__(self, generation, gene, obj):
        self.generation = generation
        self.gene = gene
        self.obj = obj
        self.rank = 0
        self.dist = .0

    def __lt__(self, other):
        """Crowded comparision operation."""
        return ((self.rank < other.rank) or (self.rank == other.rank) and
                (self.dist > other.dist))

    def __eq__(self, other):
        return self.obj == other.obj

    def __le__(self, other):
        """Dominance operation."""
        for obja, objb in zip(self.obj, other.obj):
            if obja > objb:
                return False
        return True

    def __hash__(self):
        k = 2166136261
        for obj in self.obj:
            k *= 16777619
            k ^= ctypes.c_uint.from_buffer(ctypes.c_float(obj)).value
        return k

class ChromosomeFactory:
    """Abstract class to generate chromossomes.

    All the individuals of a population need to be generated from somewhere,
    either randomly or being borned based on older individuals. When a new
    gene appears it needs to be evaluated so that the resulting chromosome can
    be placed in the population.

    Parameters
    ----------
    instance: object
        Instance of the problem to be solved.
    *args: list of functions
        Functions that will be used to evaluate a solution.

    Attributes
    ----------
    instance: object
        Instance of the problem to be solved.
    objective_functions: list of functions
        Functions that will be used to evaluate a solution.
    obj_count: int
        Number of objective functions.

    Methods
    -------
    decode(gene)
        Decode a gene into a solution.
    new()
        Create a random solution.
    crossover(parent_a, parent_b)
        Generate the offspring for two genes.
    mutate(gene)
        Change the structure of a gene.
    build(gene)
        Create a chromosome based on a gene.
    """

    def __init__(self, instance, *args):
        self.instance = instance
        self.objective_functions = list(args)
        self.obj_count = len(self.objective_functions)

    def decode(self, gene):
        """Decode a gene into a solution.

        Virtual method to decode a gene. When inheriting from this class it is
        mandatory to implement this method otherwise the generated genes cannot
        be transformed into chromosomes.

        Parameters
        ----------
        gene: object
            The gene to be decoded.

        Returns
        -------
        object
            A soltion for this instance of the problem being solved.

        Raises
        ------
        NotImplementedError
            When the child class didn't implemented this method.
        """
        raise NotImplementedError

    def new(self):
        """Create a random solution.

        This method is called to generate the individuals of the first
        population. When inheriting from this class it is mandatory to
        implement this method otherwise the initial population cannot born.

        Returns
        -------
        object
            A gene object that has no parents.

        Raises
        ------
        NotImplementedError
            When the child class didn't implemented this method.
        """
        raise NotImplementedError

    def crossover(self, parent_a, parent_b):
        """Generate the offspring for two genes.

        This method is called to generate the offsprings of a given population.
        When inheriting from this class it is mandatory to implement this
        method otherwise the next generations cannot born.

        Parameters
        ----------
        parent_a: Chromosome
            The chromosome for parent a.
        parent_b: Chromosome
            The chromosome for parent b.

        Returns
        -------
        object
            The gene generated by the coupling of the parents.

        Raises
        ------
        NotImplementedError
            When the child class didn't implemented this method.
        """
        raise NotImplementedError

    def mutate(self, gene):
        """Change the structure of a gene.

        This method is called to change the structure of a gene. When
        inheriting from this class it is mandatory to implement this method
        otherwise there will be no way for the population to get better, and 
        the solutions will be stuck.

        Parameters
        ----------
        gene: object
            The gene that will be modified.

        Raises
        ------
        NotImplementedError
            When the child class didn't implemented this method.
        """
        raise NotImplementedError

    def build(self, generation, gene):
        """Create a chromosome based on a gene.

        This method is called to generate the chromosome that will be put in
        the next generation.

        Parameters
        ----------
        gene: object
            The gene for the new individual.

        Returns
        -------
        Chromosome
            The new individual for the next generation.
        """
        solution = self.decode(gene)
        obj = [f(solution, self.instance) for f in self.objective_functions]
        return Chromosome(generation, gene, obj)


def fast_non_dominated_sort(solution_set):
    """Sort the chromosomes into non dominated fronts.

    In a multi objective optimization problem the solutions are given in a set,
    the solutions that belongs to this set are no better than each other since
    one cannot get better for a given objective function without getting worse
    in other. In a given population one solution dominates another solution
    olny and if only all of its objective values are better than the oter.
    Therefore in a multi objective genetic algorithm the non dominating
    solutions must be separated into sets and those sets sorted in order of
    dominance.

    Parameters
    ----------
    solution_set: set of chromosome
        An unordered set containing a population of individuals that must be
        sorted.

    Returns
    -------
    list of chromosome list
        Each chromosome list represents a non dominated front.
    """
    frontier = [set(), ]
    # p: [set of solutions dominated by p, number of solutions dominating p]
    dominated_by = {x: [set(), 0] for x in solution_set}
    for solution_p in solution_set:
        for solution_q in solution_set:
            if solution_p <= solution_q:
                dominated_by[solution_p][0].add(solution_q)
            elif solution_q <= solution_p:
                dominated_by[solution_p][1] += 1
        # if p is not dominated it belongs to the pareto frontier
        if dominated_by[solution_p][1] == 0:
            frontier[0].add(solution_p)
            solution_p.rank = 0
    i = 0
    while True:
        new_front = set()
        for solution_p in frontier[i]:
            for solution_q in dominated_by[solution_p][0]:
                dominated_by[solution_q][1] -= 1
                if dominated_by[solution_q][1] == 0:
                    solution_q.rank = i + 1
                    new_front.add(solution_q)
        # stops when there is no solution to be added in this front
        if not new_front:
            break
        frontier.append(new_front)
        i += 1
    return [[y for y in x] for x in frontier]


def crowding_distance_assignment(front):
    """Assign the crowding distance for solutions in a front.

    The crownding distance is a mesurement of density of the solutions in a
    given front, smaller values means that the solution is more crowded.

    Parameters
    ----------
    front: list of chromosomes
        A non dominated front of individuals.
    """
    front_size = len(front)
    obj_count = len(front[0].obj)
    # ensure that all the solutions have distance 0 in the begining
    for solution_p in front:
        solution_p.dist = 0
    # for each objective function
    for idx in range(obj_count):
        # sort the solutions based on their objective values
        front.sort(key=lambda x, id=idx: x.obj[id])
        # best and worse solutions are taken away
        front[0].dist = float('inf')
        front[-1].dist = float('inf')
        delta = front[-1].obj[idx] - front[0].obj[idx]
        for i in range(1, front_size-1):
            front[i].dist += (front[i+1].obj[idx] - front[i-1].obj[idx])/delta


def nsgaii(factory, selector, population_size, mutation_probability,
           max_generations):
    """Multi objective genetic algorithm.

    Parameters
    ----------
    factory: ChromosomeFactory
        The chromosome factory that will act like the problem definition.
    selector: function
        Function to choose two parents for breeding.
    population_size: int
        The number of individuals in each generation.
    mutation_probability: float
        Mutation rate in each generation.
    max_generations: int
        Number of generations to execute.

    Returns
    -------
    list of Chromosome
        Non dominated solutions from the pareto frontier.
    """
    # generate the first population and offspring
    population = set()
    while len(population) < population_size:
        chromosome = factory.new()
        chromosome = factory.build(0, chromosome)
        population.add(chromosome)

    for generation in range(max_generations):
        # GENERATE OFFSPRING
        offspring = set()
        while len(offspring) < population_size:
            parent_a, parent_b = selector(population)
            child = factory.crossover(parent_a.gene, parent_b.gene)
            if np.random.uniform() < mutation_probability:
                factory.mutate(child)
            child = factory.build(generation, child)
            offspring.add(child)

        population.update(offspring)
        pareto = fast_non_dominated_sort(population)
        population = set()
        for front in pareto:
            crowding_distance_assignment(front)
            if len(population) + len(front) > population_size:
                remaining = population_size - len(population)
                front.sort(reverse=True)
                population.update(front[:remaining])
                break
            population.update(set(front)) 
    return pareto[0]  # return the best solutions