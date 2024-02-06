
import json

class Instance:

    def __init__(self, experiment, draw, scenario_seed, simulation_seed):
        self.experiment = experiment
        self.draw = draw
        self.scenario_seed = scenario_seed
        self.simulation_seed = simulation_seed


def read_instance(config_file):
    data = None
    with open(config_file, 'r') as f:
        data = json.load(f)

    return Instance(data["experiment"], data["draw"], data["scenario_seed"], data["simulation_seed"])

