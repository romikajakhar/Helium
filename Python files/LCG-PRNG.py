class LCG:
    def __init__(self, seed):
        self.seed = seed

    def rand(self):
        a = 1664525
        c = 1013904223
        m = 2 ** 32
        self.seed = (a * self.seed + c) % m
        return self.seed

v=LCG(2).rand()
print(v)

import random
import matplotlib.pyplot as plt
def randseq():

    numbers = list(range(8))
    random.shuffle(numbers)
    sequence = [i for i in numbers]

    return sequence


data=[]
for i in range(10):
    data+=randseq()

plt.plot(data)
plt.show()