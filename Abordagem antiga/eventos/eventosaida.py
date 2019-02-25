from enums import estadoservidor


class EventoSaida:

    def __init__(self, evento_base, instante_do_evento_anterior):
        self.__evento_base = evento_base
        self.__instante_do_evento_anterior = instante_do_evento_anterior

    @property
    def tempo(self):
        return self.__evento_base.instante_do_evento

    @property
    def id_fregues(self):
        return self.__evento_base.id_fregues

    @property
    def instante_do_evento_anterior(self):
        return self.__instante_do_evento_anterior

    def trata_evento(self, estado_servidor, fila_de_eventos, fila_de_espera, id_proximo_fregues, gera_evento, metricas):
        metricas.incrementar_num_fregueses_sairam_do_sistema()
        metricas.incrementar_tempo_total_no_sistema(self.tempo)
        return estadoservidor.EstadoServidor.livre
