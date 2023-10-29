# Test all cases possible
# Do it 10 times


from module import TaskDefinitionFile, Path, read_city, get_energy_generator
import numpy as np
import itertools


def greedy(file: TaskDefinitionFile):
    path, cities = read_city(file)
    get_energy = get_energy_generator(cities)
    energy = get_energy(path)
    for ipath in itertools.permutations(path):
        new_energy = min(energy, get_energy(ipath))
        if new_energy == energy:
            new_path = ipath
            energy = new_energy
    return new_path, new_energy


if __name__ == '__main__':
    res = greedy("03/circle.dat")
    print("res:", res)
