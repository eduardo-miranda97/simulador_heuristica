# -*- coding:utf-8 -*-

import argparse
import json

from mh_ga_instance import read_instance
from mh_ga_factory import Factory, selector
from mh_ga_nsgaii import nsgaii

parser = argparse.ArgumentParser(description='Simulator')

parser.add_argument('-e', action="store", dest='experiment', type=str, required=True, help="Experiment Folder.")

parser.add_argument(
    '--pop_size', type=int, help='Quantidade de indivíduos em cada geração',
    default=4
)

parser.add_argument(
    '--mut_prob', type=float, help='Probabilidade de mutação em cada geração',
    default=.4
)

parser.add_argument(
    '--max_gen', type=int, help='Numero de gerações para o NSGA-II',
    default=2
)

def save_result(result, instance, filename):
    self.generation = generation
    self.gene = gene
    self.obj = obj

    with open(filename, 'w+') as outfile:
        solution = {
            'objectives': result.obj,
            'generation': result.generation,

            'schedule': {
                instance.project.tasks[x].name: {
                    'start': result[2][x],
                    'duration': instance.project.tasks[x].expected_duration,
                    'developers': [
                        instance.team.developers[y].name for y in
                        filter(lambda y: x in result[1][y], result[1])],
                } for x in result[2]
            },
            'assignment': {
                instance.team.developers[x].name: [
                    instance.project.tasks[y].name for y in result[1][x]
                ] for x in result[1]
            }
        }

        json.dump(solution, outfile, indent=2)

if __name__ == "__main__":
    args = parser.parse_args()

    instance = read_instance(args.experiment)

    factory = Factory(instance)
    results = None

    results = nsgaii(factory, selector, args.pop_size, args.mut_prob,
                         args.max_gen)
    
    save_result(results)
    print(results)
