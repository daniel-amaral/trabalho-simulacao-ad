class Fregues:

    def __init__(self, id, instante_de_chegada):
        self.__id = id
        self.__instante_de_chegada = instante_de_chegada
        self.__instante_de_atendimento = None
        self.__instante_de_saida = None

    @property
    def id(self):
        return self.__id

    @property
    def instante_de_chegada(self):
        return self.__instante_de_chegada

    @property
    def instante_de_atendimento(self):
        return self.__instante_de_atendimento

    def set_instante_de_atendimento(self, instante):
        self.__instante_de_atendimento = instante

    @property
    def instante_de_saida(self):
        return self.__instante_de_saida

    def set_instante_de_saida(self, instante):
        self.__instante_de_saida = instante

    @property
    def tempo_de_espera_na_fila(self):
        return self.instante_de_atendimento - self.instante_de_chegada

    @property
    def tempo_total_no_sistema(self):
        return self.instante_de_saida - self.instante_de_chegada