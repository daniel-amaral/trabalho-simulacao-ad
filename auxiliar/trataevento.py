from enums.estadoservidor import EstadoServidor
from enums.tipoevento import TipoEvento
from entidades.evento import Evento
from entidades.fregues import Fregues

class TrataEvento:

    def trata(self, evento, estado_do_servidor, lista_de_eventos, fila_de_espera, gerador_exponencial, id_proximo_fregues, metricas):
        if evento.tipo_de_evento == TipoEvento.chegada:
            return self.\
                __trata_evento_de_chegada(evento, estado_do_servidor, lista_de_eventos,
                                          fila_de_espera, gerador_exponencial, id_proximo_fregues, metricas)
        if evento.tipo_de_evento == TipoEvento.atendimento:
            return self.__trata_evento_de_atendimento(evento, lista_de_eventos, gerador_exponencial, metricas)
        return self.__trata_evento_de_saida(evento, fila_de_espera, lista_de_eventos, metricas)

    def __trata_evento_de_chegada(self, evento, estado_do_servidor, lista_de_eventos,
                                  fila_de_espera, gerador_exponencial, id_proximo_fregues, metricas):
        evento.set_fregues(Fregues(id_proximo_fregues, evento.instante))
        # print 'Fregues ' + str(evento.fregues.id) + ' chegou em ' + str(evento.fregues.instante_de_chegada)
        if estado_do_servidor == EstadoServidor.livre:
            evento_atendimento = Evento(TipoEvento.atendimento, evento.instante)
            if fila_de_espera.esta_vazia():
                evento_atendimento.set_fregues(evento.fregues)
            else:
                evento_atendimento.set_fregues(fila_de_espera.proximo_fregues())
            lista_de_eventos.insere_evento(evento_atendimento)
        else:
            fila_de_espera.insere_fregues(evento.fregues)
        proximo_instante = gerador_exponencial.amostra_taxa_de_chegada() + evento.instante
        proximo_evento_chegada = Evento(TipoEvento.chegada, proximo_instante)
        lista_de_eventos.insere_evento(proximo_evento_chegada)
        return estado_do_servidor

    def __trata_evento_de_atendimento(self, evento, lista_de_eventos, gerador_exponencial, metricas):
        fregues = evento.fregues
        fregues.set_instante_de_atendimento(evento.instante)
        # print 'Fregues ' + str(fregues.id) + ' iniciou atendimento em ' + str(fregues.instante_de_atendimento)
        proximo_instante = gerador_exponencial.amostra_taxa_de_servico() + evento.instante
        proximo_evento_saida = Evento(TipoEvento.saida, proximo_instante)
        proximo_evento_saida.set_fregues(evento.fregues)
        lista_de_eventos.insere_evento(proximo_evento_saida)
        metricas.incrementar_num_fregueses_entraram_em_servico()
        metricas.incrementar_tempo_de_espera_na_fila(fregues.tempo_de_espera_na_fila)
        return EstadoServidor.ocupado

    def __trata_evento_de_saida(self, evento, fila_de_espera, lista_de_eventos, metricas):
        fregues = evento.fregues
        fregues.set_instante_de_saida(evento.instante)
        # print 'Fregues ' + str(fregues.id) + ' saiu em ' + str(fregues.instante_de_saida)
        if not fila_de_espera.esta_vazia():
            proximo_evento_atendimento = Evento(TipoEvento.atendimento, evento.instante)
            proximo_evento_atendimento.set_fregues(fila_de_espera.proximo_fregues())
            lista_de_eventos.insere_evento(proximo_evento_atendimento)
        metricas.incrementar_num_fregueses_sairam_do_sistema()
        metricas.incrementar_tempo_total_no_sistema(fregues.tempo_total_no_sistema)
        return EstadoServidor.livre