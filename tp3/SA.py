Cities = list[str]
Path = list[str]  # same city at the beginning and at the end


def get_energy(path):
    return len(path)


def simulated_annealing(cities: Cities):
    path = generate_path(cities)  # random
    temperature = generate_temperatur(cities) # see initial temperature equation
    while not frozen():
        while equilibrum():
            new_path = update(path)  # random permutation
            new_path = acceptance(new_path, temperature)
    return path
