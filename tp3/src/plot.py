# Ploting module to display configurations
from module import Path, Cities
import matplotlib.pyplot as plt
import numpy as np
from SA import initial_configuration


def plot_path(path: Path, cities: Cities):
    points = [cities[city] for city in path]
    x, y = np.array([p[0] for p in points]), np.array([p[1] for p in points])
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    path, cities, get_energy = initial_configuration("data/simple_circle.dat")
    plot_path(path, cities)
