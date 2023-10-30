def cities_coordinates(filename):
    '''
    read .dat file and return a dictionary of cities' coordinates

    Parameters:
    -----------
    filename

    Returns:
    --------
    d_c : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    '''
    cities = []
    coordinates = []
    with open(filename, "r") as f:
        for l in f:
            line = list(filter(None, l.rstrip().split(' ')))
            cities.append(line[0])
            coordinates.append((float(line[1]), float(line[2])))
    d_c = {k: v for (k, v) in zip(cities, coordinates)}
    return d_c

# compute distances between all points, and store into a dictionary
def compute_distances(setting):
    # TODO
    '''
    compute the distances between all points of a setting (coordinates of cities)

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)

    Returns:
    --------
    dist : a dictionary of distances between all points (c1, c2) in the setting
    NOTE: 
    1. You can implement by computing the distances everytime, but since the distance between 2 cities will be needed frequently, 
    this step saves computations.
    2. In case you use this dictionary implementation, remember that distance(c1, c2) = distance(c2, c1) --> even less calculations (but more memory !)
    '''
 
# compute fitness by computing length of the path    
def compute_fitness(combination, dist):
    # TODO
    '''
    compute path length of a combination (of cities)

    Parameters:
    -----------
    combination : list of cities' path
    dist : a dictionary of distances between all points (c1, c2) in the setting

    Returns:
    --------
    fitness : path length
    '''

# compute the probability of choosing a next city from unvisited cities
def prob_to_city(i, j, J, dist, T, alpha, beta):
    # TODO
    '''
    compute the probability of moving from city i to city j (j belongs to J)

    Parameters:
    -----------
    i : current city
    j : city belonging to J 
    J : list of unvisited cities
    dist : a dictionary of distances between all points (c1, c2) in the setting
    T : dictionary of pheremone quantities between points (c1, c2)
    alpha : parameter that controls the relative importance of the pheromone
    beta : parameter that controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    p : probability to go to city j from city i
    '''

# find solution by greedy algorithm
def find_greedy(setting, dist):
    '''
    perform the greedy algorithm

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    dist : a dictionary of distances between all points (c1, c2) in the setting

    Returns:
    --------
    c : path (list)
    fitness : fitness of path
    exec_time : execution time
    '''

# path of each individual ant (run later in parallel, independent at each time t)
def ant_path(setting, dist, T, alpha, beta):
    # TODO
    '''
    path of each individual ant (out of m ants)
    this function can be parallelized and used later in the main AS function

    Parameters:
    -----------
    setting : dictionary of cities' coordinates in form k:v
    where k is the city name
    & v are the coordinates (x, y)
    dist : a dictionary of distances between all points (c1, c2) in the setting
    T : dictionary of pheremone quantities between points (c1, c2)
    alpha : controls the relative importance of the pheromone
    beta : controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    c : path (list)
    fitness : fitness of path
    '''
