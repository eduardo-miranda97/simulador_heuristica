# -*- coding:utf-8 -*-

import argparse
import cProfile as profile
import json
import pstats

from crowd_map import CrowdMap
from individual import Individual
from pheromone_map import PheromoneMap
from simulator import Simulator
from static_map import StaticMap
from structure_map import StructureMap
from wall_map import WallMap

parser = argparse.ArgumentParser(description='Simulator')
parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")
parser.add_argument('-d', action="store_const", dest='draw', const=True, default=False, help="Enable Draw Mode.")

if __name__ == "__main__":
    args = parser.parse_args()

    # p = profile.Profile()
    # p.enable()

    structure_map = StructureMap(args.experiment, "../input/" + args.experiment + "/map.txt")
    structure_map.load_map()

    wall_map = WallMap(args.experiment, structure_map)
    wall_map.load_map()
    if (args.draw):
        wall_map.draw_map("../output/" + args.experiment)

    static_map = StaticMap(args.experiment, structure_map)
    static_map.load_map()
    if (args.draw):
        static_map.draw_map("../output/" + args.experiment)
        
    individuals = []
    with open("../input/" + args.experiment + "/individuals.json", 'r') as json_file:
        data = json.load(json_file)
        for caracterization in data['caracterizations']:
            for _ in range(caracterization['amount']):
                individuals.append(Individual(caracterization, 0, 0))

    crowd_map = CrowdMap(args.experiment, structure_map)
    crowd_map.load_map(individuals)
    if (args.draw):
        crowd_map.draw_map("../output/" + args.experiment, 0)

    pheromone_map = PheromoneMap(args.experiment, structure_map)
    pheromone_map.load_map()

    # SIMULATOR
    directory = ''
    simulator = Simulator(structure_map, wall_map, static_map, crowd_map, pheromone_map, individuals, directory)
    #simulator.simulate()


    # p.disable()
    # pstats.Stats(p).sort_stats('cumulative').print_stats(30)
