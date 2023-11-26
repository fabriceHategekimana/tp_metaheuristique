import matplotlib.pyplot as plt
from module import open_X_Y
from module import pso_NN
from module import pred_acc
import pandas as pd
import numpy as np

X_dat, Y_dat = open_X_Y("X.dat", "Y.dat")

# 2D array of shape (200, 400),
# each row (image) contains the 400 grey values of each image
X = np.array(X_dat).reshape(200, 400)

# list of 200 labels, label for each image,
# 1 if image is "2" and 0 if image is "3"
y_k = np.array([y[0] for y in Y_dat])


def N_particles(X, y_k):
    Ns = [10, 20, 30, 50]
    vmax_coeff = 0.1
    best_fit_N = [pso_NN(X, y_k, n, vmax_coeff)[0] for n in Ns]
    plt.plot(Ns, best_fit_N)
    plt.xlabel("N (number of particle)")
    plt.ylabel("Best fitness")
    plt.title("Evolution of the fitness according to the number of particles")
    plt.show()


# By increasing the number of particles, we diminish the fitness of the algorithm
# We will retain 50 as the best result
def vmax(X, y_k):
    N = 50
    vmax_coeffs = [0, 0.1, 0.2, 0.3]
    best_fit_vmax = [pso_NN(X, y_k, N, vmc)[0] for vmc in vmax_coeffs]
    plt.plot(vmax_coeffs, best_fit_vmax)
    plt.xlabel("N (number of particle)")
    plt.ylabel("Maximal velocity coefficient")
    plt.title("Evolution of the fitness according to the maximal velocity coefficient")
    plt.show()

# Like the experiment with the number of particle, increasing the velocity conduct to a better result.
# I will keep 0.3 as the velocity


# J_global, b_global, h12_min, J_local = pso_NN(X, y_k, N, vmax_coeff)
N = 50
vmax_coeff = 0.3
df = pd.DataFrame(
        [list(pso_NN(X, y_k, N, vmax_coeff, 10*i)[-2:]) for i in range(1, 10)],
        columns=["h12_min", "J_local"])
# pred_acc(h, X, y_k):
df["accuracy"] = df["h12_min"].apply(lambda h: pred_acc(h, X, y_k))

print("df:\n", df)
