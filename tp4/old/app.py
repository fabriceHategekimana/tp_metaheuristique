from task_definition_manager import *
from module import *

data = open_file("cities2.dat")

df = cities_coordinates("cities.dat")

print(df)

