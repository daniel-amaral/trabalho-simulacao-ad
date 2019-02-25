class Fregues:

    def __init__(self, id, eventochegada):
        self.__id = id
        self.__eventochegada = eventochegada
        self.__eventoatendimento = None
        self.__eventosaida = None

    @property
    def id(self):
        return self.__id

    @property
    def eventochegada(self):
        return self.__eventochegada

    @property
    def eventoatendimento(self):
        return self.__eventoatendimento

    @property
    def eventosaida(self):
        return self.__eventosaida