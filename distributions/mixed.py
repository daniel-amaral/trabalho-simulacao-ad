

class Mixed:

    def __init__(self, random):
        self.__random = random
        self.__p1 = self.create_probability(64, .3)
        self.__p2 = self.create_probability((512, .1))
        self.__p3 = self.create_probability(1500, .3)

    def create_probability(value, prob):
        return {
            'value': value,
            'prob': prob
        }