# Part 2

```python
from module import ant_path, compute_distances
from task_definition_manager import open_file
from greedy import find_greedy
from module2 import find_AS, plot_path

d_c1 = open_file("data/cities.dat")
dist1 = compute_distances(d_c1)
# greedy
g_path1, g_length1, g_time1 = find_greedy(d_c1, dist1)
plot_path(g_path1, d_c1, "C1 greedy", "c1_greedy")

# AS
a_path1, a_length1, a_time1 = find_AS(d_c1, g_length1, dist1, tmax=10, ants=5, alpha=1, beta=1)
plot_path(a_path1, d_c1, "C1 AS", "c1_AS")


d_c2 = open_file("data/cities2.dat")
dist2 = compute_distances(d_c2)
# greedy
g_path2, g_length2, g_time2 = find_greedy(d_c2, dist2)
plot_path(g_path2, d_c2, "C2 greedy", "c2_greedy")
# AS
a_path2, a_length2, a_time2 = find_AS(d_c2, g_length2, dist2, tmax=10, ants=5, alpha=1, beta=1)
plot_path(a_path2, d_c2, "C2 AS", "c2_AS")
# TODO
```

Change m and t_max
```{python}
from module2 import compare_AS_tmax
from module2 import compare_AS_ants

# Tmax variation
compare_AS_tmax(d_c2, dist2, g_length2, 5, 1, 1, tmax=[10, 20, 30, 40, 50])

# Number of Ants variation
compare_AS_ants(d_c2, dist2, g_length2, 5, 1, 1, ants=[5, 10, 15, 20, 25, 30])
```

Compare with:
nearest_neighbour_algorithm

Plot 

Generate 50, 60, 80, 100
```{python}
from collections import OrderedDict
import random

c = [50, 60, 80, 100]
d_pt = OrderedDict()
for i in c:
    points = [str("p"+str(x)) for x in range(i)]
    coord = [(random.uniform(-10, 10),
              random.uniform(-10, 10)) for _ in range(i)]
    value = zip(points, coord)
    d_pt[i] = d50 = {k: v for (k, v) in value}
```

mean_standard_deviation([time, length])

## Comments

1. The effect of varying t_max and m (number of ants)
2. Greedy vs Ant System
3. Performance of the Ant System and the SA on the TSP about time and length 

In the comments, answer the following questions:
1. What is the Search Space for Ant System algorithm
2. Can you describe the neighborhood in this case
3. Takl about the impact of parameters alpha, beta and rho

