class Evento:

    def __init__(self, tipo_de_evento, instante):
        self.__tipo_de_evento = tipo_de_evento
        self.__instante = instante
        self.__fregues = None

    @property
    def tipo_de_evento(self):
        return self.__tipo_de_evento

    @property
    def instante(self):
        return self.__instante

    def set_fregues(self, fregues):
        self.__fregues = fregues

    @property
    def fregues(self):
        return self.__fregues

    def __lt__(self, other):
        return self.instante < other.instante