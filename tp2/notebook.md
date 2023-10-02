---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# TP2- Ganza Fabrice Hategekimana

The main function of the tp are in the module.py file.

## part1

```{code-cell} ipython3
from part1 import demo1, demo2, demo3, demo4, demo5, demo6
```

```{code-cell} ipython3
demo1()
```

```{code-cell} ipython3
demo2()
```

```{code-cell} ipython3
demo3()
```

```{code-cell} ipython3
demo4()
```

```{code-cell} ipython3
demo5()
```

```{code-cell} ipython3
demo6()
```

## part2

```{code-cell} ipython3
from module import *
```

```{code-cell} ipython3
''' Run your algorithm 10 times on the example provided with this exercise
(the ”1.dat” file) ; make sure that you start each iteration with a different
initial state. Vary the l parameter (tabu tenure) over {1, 0.5n, 0.9n} and
for each value of l report the best, the mean and the standard deviation of
the obtained values of I. For this problem check whether the diversification
mechanism helps '''

''' We expect to see graphs/tables showing the statistics for each method 
(with/out diversification), varying tenure, and tmax(optional)
'''

## save fitness results to get statistics (minimum, mean, and standard deviation) for all 10 runs, for each method

def get_datas(tenure, tmax):
	tabu_results = []
	tabu_div_results = []
	for _ in range(10):
		global_I, global_P = tabu_QAP(tenure, tmax)
		tabu_results.append(global_I)
		global_I_div, global_P_div = tabu_QAP(tenure, tmax, with_div=True)
		tabu_div_results.append(global_I_div)
	return tabu_results, tabu_div_results
```

```{code-cell} ipython3
tenure = 1
tmax = 100
tabu_results1, tabu_div_results1 = get_datas(tenure, tmax)
```

```{code-cell} ipython3
tenure = 4*0.5
tmax = 100
tabu_results1, tabu_div_results1 = get_datas(tenure, tmax)
```

```{code-cell} ipython3
tenure = 4*0.9
tmax = 100
tabu_results1, tabu_div_results1 = get_datas(tenure, tmax)
```
