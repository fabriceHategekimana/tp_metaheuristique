import random


def generate_task_definition_file(name, sample):
    f = open(name, "a")
    for i in range(1, sample+1):
        if i < sample:
            f.write(f"c{i} {random.random()} {random.random()}\n")
        else:
            f.write(f"c{i} {random.random()} {random.random()}")
    f.close()
