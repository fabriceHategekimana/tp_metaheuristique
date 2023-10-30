# This playground file is there to avoid switching
# between two hierarchy during the experimentation

from src.SA import initial_configuration
from src.plot import plot_path

path, cities, get_energy = initial_configuration("src/data/simple_circle.dat")
plot_path("demo", path, cities)
