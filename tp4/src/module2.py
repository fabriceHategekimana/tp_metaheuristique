from module import ant_path, get_pheromone, compute_distances, get_coordinates
from task_definition_manager import open_file
from collections import OrderedDict
import matplotlib.pyplot as plt
from greedy import find_greedy
import pandas as pd
import random
import time
import sys


def do_follow_in(c1, c2, path):
    ic1 = path.index(c1)
    ic2 = path.index(c2)
    return abs(ic1 - ic2) == 1


def new_pheromone(solutions, c1, c2, Q):
    return [(do_follow_in(c1, c2, path) * Q) / length
            for (path, length) in solutions]


def find_AS(setting, g_fitness, dist, tmax, ants, alpha, beta):
    """
    perform the Ant System algorithm

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    g_fitness : fitness that we get from greedy algorithm (best one)
    dist : a dictionary of distances between all points (c1, c2) in the setting
    tmax : number of iterations
    ants : number of ants
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    c : path (list)
    fitness : fitness of path
    exec_time : execution time

    NOTE : the function ant_path can be parallelized,
    since at each iteration, ants are independent
    """
    start = time.time()
    # Intro
    setting = open_file("data/cities.dat")
    distances = compute_distances(setting)
    T = pd.DataFrame({
        "c1": distances["c1"].to_list(),
        "c2": distances["c2"].to_list(),
        "pheromone": [1 / g_fitness] * len(distances["distance"]),
        })
    Q = g_fitness
    solutions = []
    for x in range(tmax):
        # solutions
        solutions = list(
            map(
                lambda x: ant_path(setting, distances, T, 1, 1, ["a", "b", "c"]),
                range(ants),
            )
        )
        # update
        for i, (c1, c2) in enumerate(zip(T["c1"], T["c2"])):
            # rho = 0.1
            T.at[i, "pheromone"] = (1 - (0.1)) * get_pheromone(T, c1, c2) + sum(
                new_pheromone(solutions, c1, c2, Q)
            )
    min_fitness = sys.maxsize
    min_path = None

    for path, fitness in solutions:
        if fitness < min_fitness:
            min_fitness = fitness
            min_path = path
    stop = time.time()
    return min_path, min_fitness, stop-start


# plot the path of a combination
def plot_path(combination, setting, title, filename):
    """
    plot the path of a combination

    Parameters:
    -----------
    combination : list of cities' path
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    title : title of plot
    filename : name to save output figure (can be removed)
    """

    # get coordinates of each city (in order)
    coords = [get_coordinates(setting, city) for city in combination]
    fig = plt.gcf()
    fig.set_size_inches(15, 15)
    x, y = list(zip(*coords))
    plt.scatter(x, y, c=["r"] + ["k"] * (len(combination) - 1))
    plt.title(f"{title}-{len(setting)}cities")
    plt.gca().set_aspect("equal", adjustable="box")

    data_xrange = plt.xlim()[1] - plt.xlim()[0]
    head_scale = data_xrange * 0.3

    for i in range(len(coords)):
        x, y = list(zip(*(coords[i], coords[(i + 1) % len(coords)])))
        plt.arrow(
            x[0],
            y[0],
            (x[1] - x[0]),
            (y[1] - y[0]),
            length_includes_head=True,
            head_width=0.05 * head_scale,
            head_length=0.05 * head_scale,
            overhang=0.5,
            alpha=0.6,
        )
    plt.axis("off")
    plt.savefig(filename)
    plt.show()


# plot box_plot for statistics
def box_plot(setting, methods, results):
    """
    plot statistics' box plot

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    methods : list of methods ['greedy', 'AS']
    results : path, fitness, and execution time results of each method
    """
    # for every setting, for every method, plot fitness boxplot
    boxes = {m: results[m]["fitness"] for m in methods}
    fig, ax = plt.subplots()
    ax.boxplot(boxes.values(), showmeans=True, labels=list(boxes.keys()))

    plt.title(f"Fitness Distribution for {len(setting)} cities")
    plt.savefig(f"Fitness Distribution for {len(setting)} cities")
    plt.show(fig)
    plt.close(fig)


# def compare_methods(setting, tmax, ants, alpha, beta, filename=None):
    # """
    # compare greedy & AS methods, output statistics to file + box_plot,
    # & plot paths for initial, best greedy, and best AS
# 
    # Parameters:
    # -----------
    # setting : dictionary of cities' coordinates in form k:v
    # where k is the city name
    # & v are the coordinates (x, y)
    # t_max : number of iterations
    # ants : number of ants
    # alpha : controls the relative importance of the pheromone
    # beta : controls the relative importance of the heuristic information η_ij
# 
    # Returns:
    # --------
    # c : path (list)
    # fitness : fitness of path
    # exec_time : execution time
# 
    # NOTE : the function ant_path can be parallelized,
    # since at each iteration, ants are independent
    # """
# 
    # dist = compute_distances(setting)
# 
    # methods = ("greedy", "AS")
    # results = dict.fromkeys(methods)
    # for m in methods:
        # results[m] = {"path": [], "fitness": [], "exec_time": []}
# 
    # # run greedy 10 times
    # for _ in range(10):
        # path, fitness, exec_time = find_greedy(setting, dist)
        # results["greedy"]["path"].append(path)
        # results["greedy"]["fitness"].append(fitness)
        # results["greedy"]["exec_time"].append(exec_time)
# 
    # # TODO --------------------------------
    # # get g_fitness (L_nn), best solution of the greedy algorithm
    # g_fitness = 1
    # # --------------------------------------
# 
    # # run AS 5 times
    # for _ in range(5):
        # path, fitness, exec_time = find_AS(
            # setting, g_fitness, dist, tmax, ants, alpha, beta
        # )
        # results["AS"]["path"].append(path)
        # results["AS"]["fitness"].append(fitness)
        # results["AS"]["exec_time"].append(exec_time)
# 
    # box_plot(setting, methods, results)
# 
    # # for every method, print statistics
    # min_greedy_fitness = min(results["greedy"]["fitness"])
    # std_greedy_fitness = statistics.stdev(results["greedy"]["fitness"])
    # mean_greedy_fitness = statistics.mean(results["greedy"]["fitness"])
    # std_greedy_exec = statistics.stdev(results["greedy"]["exec_time"])
    # mean_greedy_exec = statistics.mean(results["greedy"]["exec_time"])
    # min_greedy_path = results["greedy"]["path"][
        # results["greedy"]["fitness"].index(min_greedy_fitness)
    # ]
    # min_as_fitness = min(results["AS"]["fitness"])
    # std_as_fitness = statistics.stdev(results["AS"]["fitness"])
    # mean_as_fitness = statistics.mean(results["AS"]["fitness"])
    # std_as_exec = statistics.stdev(results["AS"]["exec_time"])
    # mean_as_exec = statistics.mean(results["AS"]["exec_time"])
    # min_as_path = results["AS"]["path"][results["AS"]["fitness"].index(min_as_fitness)]
# 
    # outfile = "Results"
    # if filename:
        # outfile += "_" + filename
    # outfile += ".txt"
    # f = open(outfile, "a")
    # s0 = f"\n For {len(setting)} cities:\n"
    # s1 = f"Greedy: Best Path = {min_greedy_path}, Minimum Fitness = {min_greedy_fitness}, Mean Fitness= {mean_greedy_fitness}, Std Fitness= {std_greedy_fitness}, Mean exec_time= {mean_greedy_exec}, Std exec_time= {std_greedy_exec}\n"
    # s2 = f"AS: Best Path = {min_as_path}, Minimum Fitness = {min_as_fitness}, Mean Fitness= {mean_as_fitness}, Std Fitness= {std_as_fitness}, Mean exec_time= {mean_as_exec}, Std exec_time= {std_as_exec}\n"
    # f.write(s0 + s1 + s2)
    # f.close()
# 
    # # TODO --------------------------------
    # # choose initial combination
    # initial = 1
    # # shuffle initial
    # # --------------------------------------
# 
    # plot_path(initial, setting, "Initial", f"path_initial_{len(setting)}.png")
    # plot_path(min_greedy_path, setting, "Greedy", f"path_greedy_{len(setting)}.png")
    # plot_path(
        # min_as_path,
        # setting,
        # "AS",
        # f"path_AS_{len(setting)}_{tmax}_{ants}_{alpha}_{beta}.png",
    # )


def compare_AS_tmax(setting, dist, g_fitness, ants, alpha, beta, tmax: list[int]):
    """
    compare AS algorithm for different tmax & plot

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    dist : a dictionary of distances between all points (c1, c2) in the setting
    g_fitness : fitness that we get from greedy algorithm (best one)
    ants : number of ants
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij
    """
    all_fitness = []
    all_exec_time = []
    for t in tmax:
        c, fitness, exec_time = find_AS(
            setting, g_fitness, dist, tmax=t, ants=ants, alpha=alpha, beta=beta
        )
        all_fitness.append(fitness)
        all_exec_time.append(exec_time)
    plt.plot(tmax, all_fitness, c="b")
    plt.xlabel("Tmax")
    plt.ylabel("Fitness")
    plt.savefig("Fitness-Iterations.png")
    plt.show()
    plt.plot(tmax, all_exec_time, c="r")
    plt.xlabel("Tmax")
    plt.ylabel("Execution Time")
    plt.savefig("Time-Tmax.png")
    plt.show()


def compare_AS_ants(setting, dist, g_fitness, tmax, alpha, beta, ants: list[int]):
    """
    compare AS algorithm for different tmax & plot

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    dist : a dictionary of distances between all points (c1, c2) in the setting
    g_fitness : fitness that we get from greedy algorithm (best one)
    t_max : number of iterations
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij
    """
    all_fitness = []
    all_exec_time = []
    for m in ants:
        c, fitness, exec_time = find_AS(
            setting, g_fitness, dist, tmax=tmax, ants=m, alpha=alpha, beta=beta
        )
        all_fitness.append(fitness)
        all_exec_time.append(exec_time)
    plt.plot(ants, all_fitness, c="b")
    plt.xlabel("Number of ants")
    plt.ylabel("Fitness")
    plt.savefig("Fitness-Ants.png")
    plt.show()
    plt.plot(ants, all_exec_time, c="r")
    plt.xlabel("Number of ants")
    plt.ylabel("Execution Time")
    plt.savefig("Time-Ants.png")
    plt.show()
