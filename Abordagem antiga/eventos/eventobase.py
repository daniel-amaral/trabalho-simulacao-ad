
class EventoBase:

    def __init__(self, instante_do_evento, id_fregues):
        self.__instante_do_evento = instante_do_evento
        self.__id_fregues = id_fregues

    @property
    def instante_do_evento(self):
        return self.__instante_do_evento

    @property
    def id_fregues(self):
        return self.__id_fregues
