import math


class Exponencial:
    '''
    Este objeto gera amostras exponenciais a partir de um lambda fornecido no seu construtor
    '''

    def __init__(self, lambd, random):
        self.__lambda = lambd
        self.__random = random

    def amostra(self, state = None):
        if state is not None:
            self.__random.setstate(state)
        x = self.__random.random()
        lambd = self.__lambda
        return - math.log(1.0 - x) / lambd