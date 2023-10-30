from src.module import Path, Cities
import matplotlib.pyplot as plt
import numpy as np
import os


def file_exist(file_name: str):
    complet_path = os.path.join(os.getcwd(), file_name)
    return os.path.isfile(complet_path)


def adapt_title(file_name: str):
    if file_exist(file_name+".png"):
        new_file_name = file_name
        i = 0
        while(file_exist(new_file_name + ".png")):
            new_file_name = file_name + str(i)
            i += 1
        return new_file_name
    else:
        return file_name


def plot_path(title: str, path: Path, cities: Cities):
    title = adapt_title(title)
    points = [cities[city] for city in path]
    x, y = np.array([p[0] for p in points]), np.array([p[1] for p in points])
    plt.plot(x, y)
    plt.grid()
    plt.savefig(title, dpi=300)
    plt.title(title)
    plt.show()
