def counter_generator(i: int):
    tab = [None]*(i+1)

    def count():
        tab.pop()
        return len(tab) > 0
    return count


still_counting = counter_generator(3)

while still_counting():
    print("Hey")
