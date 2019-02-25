import time
from auxiliar.metricas import Metricas
from entidades.evento import Evento
from enums.estadoservidor import EstadoServidor
from enums.tipoevento import TipoEvento
import matplotlib.pyplot as plt

class ExecucaoPrincipal:

    def rodar(self, kmin, id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_do_servidor,
              trata_evento, gerador_exponencial, metricas_fase_principal, utilizacao):

        print ('Inicio da execucao principal: %s, utilizacao: %.1f' % (fila_de_espera.disciplina.name, utilizacao))
        inicio_execucao_principal = time.time()

        # Configuracao de inicio do sistema
        metricas_fase_principal.append(Metricas())
        id_rodada = 0
        numero_de_coletas = 0

        # Rodadas da execucao principal:
        while numero_de_coletas < kmin:
            proximo_evento = lista_de_eventos.proximo_evento()
            estado_do_servidor = trata_evento. \
                trata(proximo_evento, estado_do_servidor, lista_de_eventos, fila_de_espera,
                      gerador_exponencial, id_proximo_fregues, metricas_fase_principal[id_rodada])

            # uma coleta e' contabilizada quando uma saida de um fregues detro da rodada e' realizada
            if proximo_evento.tipo_de_evento == TipoEvento.saida and \
                            proximo_evento.fregues.id >= trata_evento.primeiro_fregues_a_avaliar:
                numero_de_coletas += 1

            # em caso de ter sido tratado uma nova chegada, incrementar o id do proximo fregues
            if proximo_evento.tipo_de_evento == TipoEvento.chegada:
                id_proximo_fregues = proximo_evento.fregues.id + 1

        duracao = time.time() - inicio_execucao_principal
        duracao_minutos = int(duracao / 60)
        duracao_segundos = duracao - (duracao_minutos * 60)
        print ('Fim da execucao principal! Duracao: %dmin%.2fs\n' % (duracao_minutos, duracao_segundos))

        return lista_de_eventos, id_proximo_fregues, estado_do_servidor