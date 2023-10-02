---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Import

```{code-cell}

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
```

-----

# Histogram

```{code-cell}

def my_hist(generator, exp=10000):
	x = [generator() for i in range(exp)]
	counts, bins = np.hist(x)
```

# Playground

```{code-cell}

plt.plot(range(8), range(8))
plt.show()
```

# Notation

|       |       |       |    |
|-------|-------|-------|----|
| Hello | world | voila | la |
|       |       |       |    |
