import time
from greedy import greedy

print("cities1")
start = time.time()
print(greedy("03/cities_tp3.dat"))
end = time.time()
print(end-start)

print("")
print("--------------")
print("")

print("cities2")
start = time.time()
print(greedy("03/cities2_tp3.dat"))
end = time.time()
print(end-start)
