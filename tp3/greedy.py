# Test all cases possible
# Do it 10 times


from module import TaskDefinitionFile, Path, read_city, get_energy_generator
import numpy as np
import itertools


def greedy(file: TaskDefinitionFile):
    path, cities = read_city(file)
    permutations = list(itertools.permutations(path))
    get_energy = get_energy_generator(cities)
    energies = [get_energy(p) for p in permutations]
    new_path = permutations[np.argmin(energies)]
    return new_path, get_energy(new_path)


if __name__ == '__main__':
    res = greedy("03/circle.dat")
    print("res:", res)
