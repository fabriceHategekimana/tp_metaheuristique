import csv
import numpy as np

Matrice = list[list[float]]


def open_data(file_name: str) -> Matrice:
    with open(file_name, newline="") as f:
        data = list(csv.reader(f, quoting=csv.QUOTE_NONNUMERIC))
    return [[float(element) for element in sub_list] for sub_list in data]


def open_X_Y(x_file: str, y_file: str) -> tuple[Matrice, Matrice]:
    return tuple([open_data(f) for f in [x_file, y_file]])


X_dat, Y_dat = open_X_Y("X.dat", "Y.dat")

# 2D array of shape (200, 400),
# each row (image) contains the 400 grey values of each image
X = np.array(X_dat).reshape(200, 400)

# list of 200 labels, label for each image,
# 1 if image is "2" and 0 if image is "3"
y_k = [y[0] for y in Y_dat]


# Checks if all elements of a list are equal
def checkEqual(lst):
    """
    checks if all elements of a list are equal
    (by checking if the count of the first element is equal to the list length)

    Parameters:
    -----------
    lst : list of x elements

    Returns:
    --------
    True if all x elements of the list are equal, and False otherwise
    """
    return lst.count(lst[0]) == len(lst)


def fun_sigmoid(x):
    """
    compute sigmoid of value x

    Parameters:
    -----------
    x : scalar value

    Returns:
    --------
    sigmoid(x)
    """
    return 1/(1 + np.exp(-x))


# Calculate h-w1-w2
def h12(pso, X):
    """
    Valculate state of activation of the output layer
        of neurons (list of 200 values, a value for each image)

    Parameters:
    -----------
    pso : position vector of one particle
    X : 2D array of shape (200, 400),
        each row (image) contains the 400 grey values of each image

    Returns:
    --------
    h : list of 200 values representing the state of
        activation of the output layer of neurons
    """
    # w2 matrix, (1, 26) of last 26 elements of pso
    w2 = np.array(pso[-26:])

    # w1 matrix (25, 401) of first 25*401 elements of pso
    w1 = np.array(pso[:25*401]).reshape((25, 401))

    # results" list containing h value for each image
    results = []
    # for every image x
    for x in X:
        # get image (& copy !!)
        image = x.copy()
        # add 1 at 0-position
        image.insert(0, 1)
        # reshape
        image = np.array(image)
        # calculate c = matrix multiplication of weight matrix 1 and
        # image vector(with 1 at position 0)
        res1 = w1.dot(image)
        # apply sigmoidal function on elements of c
        res1 = fun_sigmoid(res1)
        # add 1 at 0-position
        res1 = list(res1).insert(0, 1)
        # reshape
        res1 = np.array(res1)
        # calculate matrix multiplication of weight matrix 2 and vector z
        # (with 1 at position 0), answer is scalar
        res2 = w2.dot(image)
        # apply sigmoidal function on answer
        res2 = fun_sigmoid(res1)
        # results, append all h12 for all images
        results.append(list(res2))

    return results


# Calculate overall fitness J
def calculate_J(h, y_k):
    """
    calculate overall fitness J (equation #5 in TP PDF)

    Parameters:
    -----------
    h : list of 200 values representing the state of
        activation of the output layer of neurons
    y_k : list of 200 labels "1" or "0", for each image

    Returns:
    --------
    fitness_J : overall fitness, mean of all J for each image
    """
    return (np.power(np.array(y_k)-np.array(h), 2).sum())/len(h)


# prediction accuracy of images
def pred_acc(h, X, y_k):
    """
    calculate the prediction accuracy (%) by comparing prediction & true labels
    y_p (predicted label) = 1 if h>=0.5 & 0 otherwise

    Parameters:
    -----------
    h : list of 200 values representing the state of
        activation of the output layer of neurons (to be used for best h12)
    X : 2D array of shape (200, 400),
        each row (image) contains the 400 grey values of each image
    y_k : list of 200 labels "1" or "0", for each image

    Returns:
    --------
    acc : prediction accuracy
    """

    # get predicted labels
    y_pred = np.vectorize(lambda x: 1 if x >= 0.5 else 0)(h12(X))
    # get prediction accuracy (%)
    correct_pred = np.sum(y_pred == y_k)
    # Calcul du pourcentage de précision
    precision = (correct_pred / len(y_k)) * 100.0
    return precision


def incrementer_generator(max_num):
    nombre = 0

    def incrementer():
        nonlocal nombre
        nombre += 1
        return True if nombre >= max_num+1 else False

    return incrementer


def counter_generator(i: int):
    tab = [None]*(i+1)

    def count():
        tab.pop()
        return len(tab) > 0
    return count


# Algorithm, and training the network
def pso_NN(X, y_k, N, vmax_coeff):
    """
    perfom PSO algorithm with NN training

    Parameters:
    -----------
    X : 2D array of shape (200, 400),
        each row (image) contains the 400 grey values of each image
    y_k : list of 200 labels "1" or "0", for each image
    N : number of particles
    vmax_coeff : velocity cutoff coefficient (% of coordinates range,
        for eg: vmax_coeff=0.1
        means vmax=0.1*(xmax_coordinate-xmin_coordinate))

    Returns:
    --------
    J_global : global best fitness
    b_global : global best position
    h12_min : global best state activation of
        output neurons (needed later for prediction)
    J_local : list of all global best positions
        (for each iteration, needed to plot later on)
    """
    # Fixed Parameters
    # cognitive & social parameters
    c1 = c2 = 2
    # inertia constant
    w = 0.9
    # number of coefficients "n" of weight matrices 1 & 2, combined
    # (go back to h12 function for a reminder if needed)
    n = (200*501*26)

    # Variate Parameters
    # coordinates" range
    c_range = [-1, 1]  # or [-0.5, 0.5]
    # velocity threshold vmax = vmax_coeff*(c_max - c_min)
    vmax = vmax_coeff*(c_range[1] - c_range[0])

    # NOTE : STOPPING CONDITION
    # choose one of these two stopping conditions:
    # 1. number of iterations, tmax=?
    # 2. last _ fitness values are equal (or not improving?)

    # Initialize
    # initialize "s" : np array of size
    # (N=number of particles, n=number of coefficients of weight matrices 1&2)
    # with values from coefficients ranging in c_range
    s = np.random.uniform(low=c_range[0],
                          high=c_range[1],
                          size=(N*n)).reshape((N, n))
    # initialize "v" : np array of size(N, n) of velocity vectors of values 0
    v = np.zeros((N, n))

    # Compute Initial J
    # Compute h12 for all pso in s
    h = np.apply_along_axis(lambda pso: h12(pso, X), axis=1, arr=s)
    # compute and save J for all particles
    J = np.apply_along_axis(lambda hi: calculate_J(hi, y_k), axis=1, arr=h)
    # get minimum J, and idx (index of minimum)
    J_min, idx = np.min(J), np.argmin(J)
    # set local & global J
    # (local J is best J for each particle, global J is best overall J)
    J_local = J
    J_global = J_min
    # set local & global positions
    # (local position is best b for each particle,
    # global position is best overall b)
    b_local = s
    b_global = s[idx]
    # save minimum h12
    h12_min = np.min(h)

    # Run algorithm

    # STOPPING CONDITION
    still_counting = incrementer_generator(10)
    while still_counting():
        # For every particle position in s:
        # r1, r2 random numbers between 0 & 1
        [r1, r2] = np.random.random((2))
        # Update v
        v = w*v + c1*r1*(b_local-s) + c2*r2*(b_global-s)
        # Check velocity if crossing upper/lower threshold
        v = np.min([v, vmax])
        # Update position
        s = s + v
        # crossing_position = set_crossing_position(s)
        # Calculate new J (by first calculating h12)
        h_new = np.apply_along_axis(lambda pso: h12(pso, X),
                                    axis=1, arr=s)
        J_new = np.apply_along_axis(lambda hi: calculate_J(hi, y_k),
                                    axis=1, arr=h)
        # Check if found new best fitness, set to local fitness
        J_local = np.apply_along_axis(lambda old, new: min(old, new),
                                      axis=0, arr=np.array(J, J_new))
        # Get minimum of all new best J, if best is < global J, set to global J
        J_min, idx = np.min(J_local), np.argmin(J_local)
        J_global = J_min
        b_local = s
        b_global = s[idx]
        # save best h12
        h12_min = np.min(h_new)
        # Update if Stopping Condition #2
    return J_global, b_global, h12_min, J_local
