from enums import disciplina
import heapq

class ListaDeEventos:
    '''
    Este objeto representa a lista de eventos do sistema
    '''

    def __init__(self):
        self.__lista_de_eventos = []

    def insere_evento(self, evento):
        heapq.heappush(self.__lista_de_eventos, evento)

    def proximo_evento(self):
        return heapq.heappop(self.__lista_de_eventos)

    @property
    def proximo_instante_de_evento(self):
        proximo_evento = heapq.heappop(self.__lista_de_eventos)
        instante = proximo_evento.instante
        heapq.heappush(self.__lista_de_eventos, proximo_evento)
        return instante

