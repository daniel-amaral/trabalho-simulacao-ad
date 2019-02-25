import math


class Exponencial:
    '''
    Este objeto gera amostras exponenciais a partir de um lambda fornecido no seu construtor
    '''

    def __init__(self, taxa_de_chegada, taxa_de_servico, random):
        self.__lambda_chegada = taxa_de_chegada
        self.__lambda_servico = taxa_de_servico
        self.__random = random

    def amostra_taxa_de_chegada(self):
        amostra = self.amostra(self.__lambda_chegada)
        # print('Amostra tx chegada: %.3f' % amostra)
        return amostra

    def amostra_taxa_de_servico(self):
        amostra = self.amostra(self.__lambda_servico)
        # print('Amostra tx servico: %.3f' % amostra)
        return amostra

    def amostra(self, lambd, state = None):
        if state is not None:
            self.__random.setstate(state)
        x = self.__random.random()
        ret = - math.log(1.0 - x) / lambd
        return ret