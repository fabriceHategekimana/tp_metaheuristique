from task_definition_manager import *


def cross_product(list_of_value):
    return np.array([(x, y) for x in list_of_value for y in list_of_value])


def get_distance(distances, c1, c2):
    return tuple(distances.query(f"c1 == '{c1}' and c2 == '{c2}'").iloc[0])[-1]


def get_coordinates(df, name):
    return np.array(df.query(f"name == '{name}'").iloc[0])[1:]


def compute_distance(setting, c1, c2):
    coords1 = get_coordinates(setting, c1)
    coords2 = get_coordinates(setting, c2)
    return np.linalg.norm(coords2-coords1)


# compute distances between all points, and store into a dataframe
def compute_distances(setting):
    '''
    compute the distances between all points of a setting (coordinates of cities)

    Parameters:
    -----------
    setting : dataframe of cities' coordinates in form (name, x, y)

    Returns:
    --------
    dist : a dataframe of distances between all points (c1, c2) in the setting (c1, c2, distance)
    '''
    cities = get_cities(setting)
    couples_of_cities = cross_product(cities)
    c1_c2_distances = mymap(lambda c: compute_distance(setting, c[0], c[1]), couples_of_cities)
    dataframe = {"c1": couples_of_cities[:,0], "c2": couples_of_cities[:,1], "distance": c1_c2_distances}
    return pd.DataFrame(dataframe)


# compute fitness by computing length of the path    
def compute_fitness(combination, dist):
    '''
    compute path length of a combination (of cities)

    Parameters:
    -----------
    combination : list of cities' path
    dist : a dataframe of distances between all points (c1, c2) in the setting

    Returns:
    --------
    fitness : path length
    '''
    combination_extended = combination.copy() + [combination[0]]
    couples = mymap(lambda i: [combination_extended[i], combination_extended[i+1]], range(len(combination_extended)-1))
    distances = mymap(lambda c: get_distance(dist, c[0], c[1]), couples)
    return np.sum(distances)


def get_pheromone(T, i, j):
    return tuple(T.query(f"c1 == '{i}' and c2 == '{j}'").iloc[0])[-1]


def eta(dist, i, j):
    return 1/get_distance(dist, i, j)


def tau(T, i, j):
    return get_pheromone(T, i, j)


# compute the probability of choosing a next city from unvisited cities
def prob_to_city(i, j, J, dist, T, alpha, beta):
    '''
    compute the probability of moving from city i to city j (j belongs to J)

    Parameters:
    -----------
    i : current city
    j : city belonging to J 
    J : list of unvisited cities
    dist : a dataframe of distances between all points (c1, c2) in the setting
    T : dataframe of pheremone quantities between points (c1, c2)
    alpha : parameter that controls the relative importance of the pheromone
    beta : parameter that controls the relative importance of the heuristic information η_ij

    Returns:
    --------
    p : probability to go to city j from city i
    '''
    if j in J:
       up = (tau(T,i,j))**alpha * (eta(dist,i,j))**beta
       down = sum(mymap(lambda l: tau(T,i,l)**alpha * (eta(i,l)**beta), J))
       return up/down
    else:
       return 0


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
    cities = sorted(get_cities(setting))
    random_index = random.randint(0, len(cities)-1)
    city = cities.pop(random_index)
    explored = [city]
    while len(cities) > 0:
        coords = mymap(lambda c: get_coordinates(setting, c), cities)
        probabilities = mymap(lambda c: prob_to_city(city, c, J, dist, explored, alpha, beta), cities)
        r = random.random()
        # select the one with higher probability
        # update explored and cities before iterating
