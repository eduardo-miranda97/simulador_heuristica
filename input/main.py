# -*- coding:utf-8 -*-

from individual import Individual
import json

with open('cult_experiment/individuals.json', 'r') as json_file:
    dados = json.load(json_file)
    pessoas = []
    for individuos in dados['caracterizations']:
        for _ in range(individuos['amount']):
            pessoas.append(Individual(individuos, 0, 0))

print(pessoas)