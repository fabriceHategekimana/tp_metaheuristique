# Test all cases possible
# Do it 10 times


from module import TaskDefinitionFile, Path, read_city, get_energy_generator
import numpy as np
import itertools


def greedy(file: TaskDefinitionFile) -> tuple[Path, int]:
    path, cities = read_city(file)
    permutations = np.array(list(itertools.permutations(path)))
    energies = get_energy_generator(cities)(permutations)
    new_path = permutations[np.argmin(energies)]
    return new_path, get_energy(new_path)


if __name__ == '__main__':
    res = greedy("03/simple_circle.dat")
    print("res:", res)
