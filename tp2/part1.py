from module import *

ITR = 1
COMBINATION = [0, 1, 2, 3]
N = len(COMBINATION)


def demo1():
    # 1.  get n (number of locations, facilities), D (Distance Matrix), and W (Weights/Flows Matrix)
    n, D, W = read_input(filename='1.dat')
    print("n:", n)
    print("D:", D)
    print("W:", W)


def demo2():
    combination2 = swap_two(COMBINATION.copy(), 0, 1)
    print("combination:", COMBINATION)
    print("combination2:", combination2)


def demo3():
    tabu_list = np.zeros((N, N))
    tabu_list = update_tabu(tabu_list, COMBINATION, 0, 1, ITR, 2)
    print("tabu_list:\n", tabu_list)
    return tabu_list


def demo4():
    tabu_list = demo3()
    res = is_tabu(tabu_list, COMBINATION, 0, 1, 3)
    print("res:", res)


def demo5():
    combination = [0, 1, 2, 3]
    div_matrix = np.random.randint(0, 25, (N, N))
    print("div_matrix:\n", div_matrix)
    relations = filter_diversification(div_matrix, COMBINATION)
    print("relations:", relations)


def demo6():
    combination = [0, 1, 2, 3]
    div_matrix = np.zeros((N, N))
    combination2 = swap_two(COMBINATION.copy(), 0, 1)
    div_matrix = update_diversification(div_matrix, COMBINATION, 0, 1)
    print("div_matrix:", div_matrix)


'''Test the above functions, and show your results for eg. :
1. print outputs n, D, and W
2. show an example of a two-swap (show before & after lists)
3. initialize an empty tabu-list, perform a swap, update the tabu-list (matrix), and print it
4. test is_tabu fuction
5. initialize a diversification matrix with few zero items, and check filter_diversification function
6. test update_diversification matrix with a swap (print the matrix before and after the swap)'''

demo4()
