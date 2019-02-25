from enums import estadoservidor


class EventoAtendimento:

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
        if estado_servidor == estadoservidor.EstadoServidor.livre:
            fila_de_eventos.insere_evento(gera_evento.gera_evento_de_saida(self.tempo, self.id_fregues))
            metricas.incrementar_num_fregueses_entraram_em_servico()
            metricas.incrementar_tempo_de_espera_na_fila(self.tempo)
            return estadoservidor.EstadoServidor.ocupado
        else:
            fila_de_eventos.insere_evento(self)
            return estado_servidor

