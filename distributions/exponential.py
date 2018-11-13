import math


class Exponential:

    def __init__(self, scale, random):
        self.__scale = scale
        self.__random = random

    def sample(self, state = None):
        if state is not None:
            self.__random.setstate(state)
        x = self.__random.random()
        scale = self.__scale
        return scale * math.exp(- scale * x)