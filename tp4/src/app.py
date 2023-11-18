from module import ant_path, compute_distances
from task_definition_manager import open_file
from greedy import find_greedy
from module2 import find_AS

d_c2 = open_file("data/cities2.dat")
dist2 = compute_distances(d_c2)
# greedy
g_path2, g_length2, g_time2 = find_greedy(d_c2, dist2)
# AS
a_path2, a_length2, a_time2 = find_AS(d_c2, g_length2, dist2, tmax=10, ants=5, alpha=1, beta=1)
