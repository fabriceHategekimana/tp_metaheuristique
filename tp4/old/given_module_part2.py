# find solution by Ant System Algorithm
def find_AS(setting, g_fitness, dist, tmax, ants, alpha, beta):
    # TODO
    '''
    perform the Ant System algorithm

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    g_fitness : fitness that we get from greedy algorithm (best one)
    dist : a dictionary of distances between all points (c1, c2) in the setting
    t_max : number of iterations 
    ants : number of ants
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    c : path (list)
    fitness : fitness of path
    exec_time : execution time

    NOTE : the function ant_path can be parallelized, since at each iteration, ants are independent
    '''

# plot the path of a combination
def plot_path(combination, setting, title, filename):
    '''
    plot the path of a combination 

    Parameters:
    -----------
    combination : list of cities' path
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    title : title of plot
    filename : name to save output figure (can be removed)
    '''
    
    # get coordinates of each city (in order)
    coords = [setting[city] for city in combination]
    fig = plt.gcf()
    fig.set_size_inches(15, 15)
    x,y = list(zip(*coords))
    plt.scatter(x, y, c=['r'] + ['k'] * (len(combination) - 1))
    plt.title(f'{title}-{len(setting)}cities')
    plt.gca().set_aspect('equal', adjustable='box')
    
    data_xrange = plt.xlim()[1] - plt.xlim()[0]
    head_scale = data_xrange * 0.3
    
    for i in range(len(coords)):
        x,y = list(zip(*(coords[i], coords[(i + 1) % len(coords)])))
        plt.arrow(x[0], y[0], (x[1] - x[0]), (y[1] - y[0]), length_includes_head=True,
          head_width=0.05 * head_scale, head_length=0.05 * head_scale, overhang=0.5, alpha=0.6)
    plt.axis("off")
    plt.savefig(filename)
    plt.show()
    
# plot box_plot for statistics    
def box_plot(setting, methods, results):
    '''
    plot statistics' box plot

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    methods : list of methods ['greedy', 'AS']
    results : path, fitness, and execution time results of each method
    '''
    # for every setting, for every method, plot fitness boxplot
    boxes = {m: results[m]['fitness'] for m in methods}
    fig, ax = plt.subplots()
    ax.boxplot(boxes.values(), showmeans = True, labels=list(boxes.keys()))
    
    plt.title(f'Fitness Distribution for {len(setting)} cities')
    plt.savefig(f'Fitness Distribution for {len(setting)} cities')
    plt.show(fig)
    plt.close(fig)

def compare_methods(setting, tmax=??, ants=??, alpha=??, beta=??, filename=None):
    # TODO (Some Parts)
    '''
    compare greedy & AS methods, output statistics to file + box_plot, & plot paths for initial, best greedy, and best AS 

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    t_max : number of iterations 
    ants : number of ants
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    c : path (list)
    fitness : fitness of path
    exec_time : execution time

    NOTE : the function ant_path can be parallelized, since at each iteration, ants are independent
    '''
    
    dist = compute_distances(setting)
    
    methods = ('greedy', 'AS')
    results = dict.fromkeys(methods)
    for m in methods:
        results[m] = {
            'path': [],
            'fitness': [],
            'exec_time': []
        }
    
    #run greedy 10 times
    for _ in range(10):
        path, fitness, exec_time = find_greedy(setting, dist)
        results['greedy']['path'].append(path)
        results['greedy']['fitness'].append(fitness)
        results['greedy']['exec_time'].append(exec_time)
        
    ## TODO --------------------------------
    # get g_fitness (L_nn), best solution of the greedy algorithm
    g_fitness = ??
    # --------------------------------------
    
    #run AS 5 times
    for _ in range(5):
        path, fitness, exec_time = find_AS(setting, g_fitness, dist, tmax, ants, alpha, beta)
        results['AS']['path'].append(path)
        results['AS']['fitness'].append(fitness)
        results['AS']['exec_time'].append(exec_time)
    
    box_plot(setting, methods, results)
    
    # for every method, print statistics 
    min_greedy_fitness = min(results['greedy']['fitness'])
    std_greedy_fitness = statistics.stdev(results['greedy']['fitness'])
    mean_greedy_fitness = statistics.mean(results['greedy']['fitness'])
    std_greedy_exec = statistics.stdev(results['greedy']['exec_time'])
    mean_greedy_exec = statistics.mean(results['greedy']['exec_time'])
    min_greedy_path = results['greedy']['path'][results['greedy']['fitness'].index(min_greedy_fitness)]
    min_as_fitness = min(results['AS']['fitness'])
    std_as_fitness = statistics.stdev(results['AS']['fitness'])
    mean_as_fitness = statistics.mean(results['AS']['fitness'])
    std_as_exec = statistics.stdev(results['AS']['exec_time'])
    mean_as_exec = statistics.mean(results['AS']['exec_time'])
    min_as_path = results['AS']['path'][results['AS']['fitness'].index(min_as_fitness)]

    outfile = "Results"
    if filename:
        outfile += "_" + filename
    outfile += ".txt"
    f = open(outfile, "a")
    s0 = f'\n For {len(setting)} cities:\n'
    s1 = f'Greedy: Best Path = {min_greedy_path}, Minimum Fitness = {min_greedy_fitness}, Mean Fitness= {mean_greedy_fitness}, Std Fitness= {std_greedy_fitness}, Mean exec_time= {mean_greedy_exec}, Std exec_time= {std_greedy_exec}\n'
    s2 = f'AS: Best Path = {min_as_path}, Minimum Fitness = {min_as_fitness}, Mean Fitness= {mean_as_fitness}, Std Fitness= {std_as_fitness}, Mean exec_time= {mean_as_exec}, Std exec_time= {std_as_exec}\n'
    f.write(s0+s1+s2)
    f.close()

    ## TODO --------------------------------
    # choose initial combination 
    initial = ??
    # shuffle initial
    # --------------------------------------

    plot_path(initial, setting, 'Initial', f"path_initial_{len(setting)}.png")
    plot_path(min_greedy_path, setting, 'Greedy', f"path_greedy_{len(setting)}.png")
    plot_path(min_as_path, setting, 'AS', f"path_AS_{len(setting)}_{tmax}_{ants}_{alpha}_{beta}.png")

def compare_AS_tmax(setting, dist, g_fitness, ants=??, alpha=??, beta=??):
    # TODO (Some Parts)
    '''
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
    '''
    ## TODO --------------------------------
    # different possibilities of tmax
    tmax = [??]
    # --------------------------------------
    all_c = []
    all_fitness = []
    all_exec_time = []
    for t in tmax:
        c, fitness, exec_time = find_AS(setting, g_fitness, dist, tmax=t, ants=ants, alpha=alpha, beta=beta)
        all_fitness.append(fitness)
        all_exec_time.append(exec_time)
    plt.plot(tmax, all_fitness, c='b')
    plt.xlabel("Tmax")
    plt.ylabel("Fitness")
    plt.savefig("Fitness-Iterations.png")
    plt.show()
    plt.plot(tmax, all_exec_time, c='r')
    plt.xlabel("Tmax")
    plt.ylabel("Execution Time")
    plt.savefig("Time-Tmax.png")
    plt.show()

def compare_AS_ants(setting, dist, g_fitness, tmax=??, alpha=??, beta=??):
    '''
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
    '''
    ## TODO --------------------------------
    # different possibilities of ants
    ants = [??]
    # --------------------------------------

    all_c = []
    all_fitness = []
    all_exec_time = []
    for m in ants:
        c, fitness, exec_time = find_AS(setting, g_fitness, dist, tmax=tmax, ants=m, alpha=alpha, beta=beta)
        all_fitness.append(fitness)
        all_exec_time.append(exec_time)
    plt.plot(ants, all_fitness, c='b')
    plt.xlabel("Number of ants")
    plt.ylabel("Fitness")
    plt.savefig("Fitness-Ants.png")
    plt.show()
    plt.plot(ants, all_exec_time, c='r')
    plt.xlabel("Number of ants")
    plt.ylabel("Execution Time")
    plt.savefig("Time-Ants.png")
    plt.show()

# dictionary of coordinates of cities from 'cities.dat' file
d_c1 = cities_coordinates('cities.dat')
# dictionary of coordinates of cities from 'cities2.dat' file
d_c2 = cities_coordinates('cities2.dat')

# dictionary of dictionaries for each 50, 60, 80, and 100 cities with their coordinates
c = [50, 60, 80, 100]
d_pt = OrderedDict()
for i in c:
    points = [str("p"+str(x)) for x in range(i)]
    coord = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(i)]
    value = zip(points, coord)

    d_pt[i] = d50 = {k: v for (k, v) in value}

## Study effect of parameters, example on 'cities2.dat' file
dist = compute_distances(d_c2)
#run greedy once to get Lnn
path, g_fitness, exec_time = find_greedy(d_c2, dist)
# Tmax variation
compare_AS_tmax(d_c2, dist, g_fitness)
# Number of Ants variation
compare_AS_ants(d_c2, dist, g_fitness)

## compare greedy vs AS for 'cities.dat', 'cities2.dat', and 50, 60, 80, & 100 cities' configurations
compare_methods(setting=d_c1, filename="c1")
compare_methods(setting=d_c2, filename="c2")
for k in d_pt:
    compare_methods(setting=d_pt[k], filename=f'dpt_{k}')
