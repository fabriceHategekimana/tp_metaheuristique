from module import ant_path
from task_definition_manager import open_file
from module import compute_distances, get_distance


data = open_file("data/cities.dat")
distances = compute_distances(data)
# distance = get_distance(distances, "a", "b")
res = ant_path(data, distances, distances, 1, 1, ["a", "b", "c"])

print("res:", res)
