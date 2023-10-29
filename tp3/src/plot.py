from src.module import Path, Cities
import matplotlib.pyplot as plt
import numpy as np


def plot_path(title: str, path: Path, cities: Cities):
    points = [cities[city] for city in path]
    x, y = np.array([p[0] for p in points]), np.array([p[1] for p in points])
    plt.plot(x, y)
    plt.grid()
    plt.savefig(title, dpi=300)
    plt.title(title)
    plt.show()
