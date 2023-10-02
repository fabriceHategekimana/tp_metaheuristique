import numpy as np
import random

# PART II


def to_object_coordinates_generator(combination):
    return lambda x: sorted([combination[x[0]], combination[x[1]]])


def contains_same_elements(couple):
    return True if couple[0] == couple[1] else False


def unique(input_list):
    res = []
    for el in input_list:
        if el not in res:
            res.append(el)
    return res


def filter_relations(relations):
    filtered_relations = unique(mymap(sorted, relations))
    remove_same = lambda x: not contains_same_elements(x)
    return myfilter(remove_same, filtered_relations)


def get_filtered_relations(combination):
    relations = cartesian_product(combination)
    filtered_relations = sorted(filter_relations(relations))
    return filtered_relations


def get_object_relations(location_relations, combination):
    to_object_coordinates = to_object_coordinates_generator(combination)
    wcs = mymap(to_object_coordinates, location_relations)
    return wcs


def get_object(combination, number):
    return combination.index(number)


def get_indices(elements_list, value):
    i = 0
    res = []
    while i < len(elements_list):
        if elements_list[i] == value:
            res.append(i)
        i += 1
    return res


def mymap(function, value_list):
    return list(map(function, value_list))


def myfilter(function, value_list):
    return list(filter(function, value_list))


def get_value(text):
    return int(text[0])


def to_int(string_list):
    new_list = myfilter(lambda x: x != "", string_list)
    return mymap(int, new_list)


def get_matrix(lines):
    return np.array(mymap(lambda x: to_int(x.split(" ")), lines))


def get_text(filename):
    f = open(filename)
    text = f.read().splitlines()
    f.close()
    return text


def read_input(filename):
    '''
    read .dat file and return n, D, and W

    Parameters:
    -----------
    filename

    Returns:
    --------
    n: number of facilities
    D: Distance Matrix
    W: Weight Matrix
    '''

    text = get_text(filename)
    indices = get_indices(text, "")
    n = get_value(text[:indices[0]])
    D = get_matrix(text[indices[0]+1:indices[1]])
    W = get_matrix(text[indices[1]+1:])
    return n, D, W


def cartesian_product(x):
    return [(a, b) for a in x for b in x]


def get_flow(couple_connection):
    a = couple_connection[0][0]
    b = couple_connection[1][0]
    return W[a, b]


def get_flow2(relation):
    n, D, W = read_input("1.dat")
    return W[relation[0], relation[1]]


def get_distance(couple_connection):
    a = couple_connection[0][1]
    b = couple_connection[1][1]
    return D[a, b]


def get_distance2(relation):
    return D[relation[0], relation[1]]


def compute_couple(couple_connection):
    flow_value = get_flow(couple_connection)
    distance_value = get_distance(couple_connection)
    return flow_value*distance_value


def compute_I(combination):
    '''
    compute fitness of a combination

    Parameters:
    -----------
    combination : list of facilities' assignment

    Returns:
    --------
    I: fitness score
    '''
    # create a function that return a couple (object, location) from the combination
    get_object_location_couple = lambda x: (combination.index(x), x)

    object_location_couples = mymap(get_object_location_couple, combination)

    # get group of relations between each (object, location)
    couple_connections = cartesian_product(object_location_couples)

    values = mymap(compute_couple, couple_connections)
    return sum(values)/2


def compute_delta(combination, i, j):
    '''
    compute delta fitness after swapping facilities in locations i & j (ie. delta fitness for one neighbor)

    Parameters:
    -----------
    combination : list of original facilities' assignment
    i, j : locations of facilities being swapped

    Returns:
    --------
    delta_I: delta fitness
    '''
    combination2 = swap_two(combination.copy(), i, j)
    location_relations = get_filtered_relations(combination)
    object_relations1 = get_object_relations(location_relations, combination)
    object_relations2 = get_object_relations(location_relations, combination2)
    object_location_couples = list(zip(object_relations1, object_relations2, location_relations))
    # we don't need to compute the w*d parts that will get the same results
    deltas = myfilter(lambda x: x[0] != x[1], object_location_couples)
    return sum(mymap(lambda x: (get_flow2(x[0])-get_flow2(x[1]))*get_distance2(x[2]), deltas))


def swap_two(combination, i, j):
    '''
    returns a new permutation with facilities in i & j swapped

    Parameters:
    -----------
    combination : list of original facilities' assignment
    i, j : locations of facilities being swapped

    Returns:
    --------
    neighbor : new permutation
    '''
    comb = combination
    a = comb.index(i)
    b = comb.index(j)

    comb[a], comb[b] = comb[b], comb[a]
    return comb


def is_tabu(tabu_list, combination, i, j, itr):
    # # itr is optional, depends on how you implement the tabu matrix
    '''
    returns a boolean to check if swap is tabu

    Parameters:
    -----------
    tabu_list : tabu matrix with locationsxfacilities
    combination : list of original facilities' assignment (before swap)
    i, j : locations of facilities being swapped
    itr : current iteration

    Returns:
    --------
    True : if swap is Tabu
    False : if swap is not Tabu
    '''
    val = tabu_list[get_object(combination, i), j]
    if val <= itr:
        return False
    else:
        return True


def update_tabu(tabu_list, combination, i, j, itr, tenure):
    # itr is optional, depends on how you implement the tabu matrix
    '''
    updates the tabu_list (matrix)

    Parameters:
    -----------
    tabu_list : tabu matrix with locationsxfacilities
    combination : list of original facilities' assignment(before swap)
    i, j : locations of facilities being swapped
    itr : current iteration
    tenure : tabu_list short term memory (l)
    '''
    tabu_list[get_object(combination, i), j] = itr+tenure
    return tabu_list


def filter_diversification(div_matrix, combination):
    '''
    returns a list of swaps that have not been set for the last n^2 iterations

    Parameters:
    -----------
    div_matrix : diversification matrix with locationsxfacilities
    combination : list of original facilities' assignment (before swap)

    Returns:
    --------
    list of swaps that have not been set for the last n^2 iterations
    empty list if no such swap exists
    '''
    n = len(combination)
    indices = cartesian_product(np.arange(n))
    return myfilter(lambda x: div_matrix[x[0], x[1]] >= n**2, indices)


def update_diversification(div_matrix, combination, i, j):
    '''
    updates the diversification matrix after swapping facilities in locations i & j

    Parameters:
    -----------
    div_matrix : diversification matrix with locationsxfacilities
    combination : list of original facilities' assignment(before swap)
    i, j : locations of facilities being swapped
    '''
    div_matrix = div_matrix+1
    div_matrix[i, j] = div_matrix[i, j] - 1
    return div_matrix


# PART II

def next_swap(tabu_list, combination, itr):
    '''
    returns next best non-tabu swap

    Parameters:
    -----------
    tabu_list : tabu matrix with locationsxfacilities
    combination : list of original facilities' assignment
    itr: the actual iteration

    Returns:
    --------
    (i, j) : new best non-tabu swap
    delta_fitness : delta_fitness of chosen best non-tabu swap (difference in fitness between original and new permutation)
    '''
    # get swaps
    swaps = cartesian_product(combination)
    swaps = myfilter(lambda x: not is_tabu(tabu_list, combination, x[0], x[1], itr), swaps)
    # get compute delta
    deltas = mymap(lambda x: compute_delta(combination, x[0], x[1]), swaps)
    # get best fitness
    if len(deltas) == 0:
        best_delta = None
        best_swap = None
    else:
        best_delta = min(deltas)
        best_swap = swaps[deltas.index(best_delta)]
    return best_swap, best_delta


def tabu_QAP(tenure, tmax, with_div=False):
    '''
    perform Tabu Search with/out diversification

    Parameters:
    -----------
    tenure : short-term memory (l)
    tmax : number of iterations
    with_div : True if with diversification, False if without (False by default here)

    Returns:
    --------
    global_I : global best seen fitness
    global_P : global best seen permutation
    '''
    combination = [0, 1, 2, 3]
    random.shuffle(combination)
    n = len(combination)
    tabu_list = np.zeros((n, n))
    itr = 0
    while itr < tmax:
        swap, delta = next_swap(tabu_list, combination, itr)
        if swap is None and delta is None:
            break
        tabu_list = update_tabu(tabu_list, combination, swap[0], swap[1], itr, tenure)
        combination = swap_two(combination, swap[0], swap[1])
        fitness = compute_I(combination)
        itr += 1
    return fitness, combination


n, D, W = read_input("1.dat")
