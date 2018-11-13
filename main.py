import random as random
from distributions.exponential import Exponential

seed = 12
random.seed(seed)
state = random.getstate()
exp = Exponential(1.23, random)

for _ in range(10):
    print str(exp.sample())