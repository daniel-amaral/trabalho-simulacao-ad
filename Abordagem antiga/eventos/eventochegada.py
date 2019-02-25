from enums import estadoservidor
from estruturas import fregues

class EventoChegada:

    def __init__(self, evento_base):
        self.__evento_base = evento_base

    @property
    def tempo(self):
        return self.__evento_base.instante_do_evento

    @property
    def id_fregues(self):
        return self.__evento_base.id_fregues

    def trata_evento(self, estado_servidor, fila_de_eventos, fila_de_espera, id_proximo_fregues, gera_evento, metricas):
        fregues = fregues.Fregues(id_proximo_fregues, self)
        if estado_servidor == estadoservidor.EstadoServidor.livre:
            fila_de_eventos.insere_evento(gera_evento.gera_evento_de_atendimento(None, self.tempo, self.id_fregues))
            fila_de_eventos.insere_evento(gera_evento.gera_evento_de_chegada(self.tempo, self.id_fregues + 1))
        else:
            fila_de_eventos.insere_evento(self)
        return estado_servidor
