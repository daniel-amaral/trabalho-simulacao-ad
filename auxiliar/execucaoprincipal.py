import time
from auxiliar.metricas import Metricas
from entidades.evento import Evento
from auxiliar.tstudent import TStudent
from enums.estadoservidor import EstadoServidor
from enums.tipoevento import TipoEvento
import matplotlib.pyplot as plt

class ExecucaoPrincipal:

    def __init__(self):
        self.__t_student = TStudent()

    # funcao que executa uma unica rodada
    def executar_rodadas(self, numero_de_coletas, kmin, id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_do_servidor,
              trata_evento, gerador_exponencial, metricas_fase_principal, utilizacao):

        # Configuracao de inicio da rodada
        id_rodada = 0
        total_coletas = 0

        # Rodadas da execucao principal:
        while id_rodada < kmin:

            metricas_fase_principal.append(Metricas())
            trata_evento.set_primeiro_fregues_a_avaliar(id_proximo_fregues)# preparacao para evitar fregueses de rodadas anteriores
            coleta_id = 0

            while coleta_id < numero_de_coletas:
                proximo_evento = lista_de_eventos.proximo_evento()
                estado_do_servidor = trata_evento. \
                    trata(proximo_evento, estado_do_servidor, lista_de_eventos, fila_de_espera,
                          gerador_exponencial, id_proximo_fregues, metricas_fase_principal[id_rodada])

                # uma coleta e' contabilizada quando uma saida de um fregues detro da rodada e' realizada
                if proximo_evento.tipo_de_evento == TipoEvento.saida and \
                                proximo_evento.fregues.id >= trata_evento.primeiro_fregues_a_avaliar:
                    coleta_id += 1
                    total_coletas += 1

                # em caso de ter sido tratado uma nova chegada, incrementar o id do proximo fregues
                if proximo_evento.tipo_de_evento == TipoEvento.chegada:
                    id_proximo_fregues = proximo_evento.fregues.id + 1
            id_rodada += 1

        # obtencao de metricas das rodadas realizadas
        soma_variancias_tempos_na_fila = 0.0
        variancias_para_chi_quadrado = []
        for metrica in metricas_fase_principal:
            soma_variancias_tempos_na_fila += metrica.estimador_variancia_tempo_na_fila
            variancias_para_chi_quadrado.append(metrica.estimador_da_variancia_para_chi_quadrado)

        media_variancias_tempo_na_fila = soma_variancias_tempos_na_fila / kmin
        media_variancias_para_chi_quadrado = sum(variancias_para_chi_quadrado) / kmin

        # verificacao de atendimento de intervalo de confianca
        media_ok = self.__t_student.verifica_intervalo_de_confianca(kmin, media_variancias_tempo_na_fila)
        chi_quadrado_ok = self.__t_student.verifica_intervalo_de_confianca(kmin, media_variancias_para_chi_quadrado)

        return media_ok, chi_quadrado_ok, lista_de_eventos, id_proximo_fregues, estado_do_servidor

    # funcao que e' chamada externamente pelo main.py para rodar multiplas rodadas numa mesma disciplica e atendimento
    def rodar(self, kmin, id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_do_servidor,
              trata_evento, gerador_exponencial, metricas_fase_principal, utilizacao):

        print ('Inicio da execucao principal: %s, utilizacao: %.1f' % (fila_de_espera.disciplina.name, utilizacao))
        inicio_execucao_principal = time.time()

        numero_de_coletas = 10 # inicialmente o numero de coletas por rodada e' fixada em apenas 10
        while True:
            print ('Numero de coletas: %d. kmin: %d' % (numero_de_coletas, kmin))
            metricas_fase_principal = []
            media_ok, variancia_ok, lista_de_eventos, id_proximo_fregues, estado_do_servidor\
                = self.executar_rodadas(numero_de_coletas, kmin, id_proximo_fregues, lista_de_eventos, fila_de_espera,
                                       estado_do_servidor, trata_evento, gerador_exponencial,
                                        metricas_fase_principal, utilizacao)

            # verificacao da necessidade de se realizar outra rodada maior que a anterior para atender aos criterios de IC
            if media_ok:
                if variancia_ok:
                    break
                kmin += 100
            else:
                numero_de_coletas *= 2

        duracao = time.time() - inicio_execucao_principal
        duracao_minutos = int(duracao / 60)
        duracao_segundos = duracao - (duracao_minutos * 60)

        # obtendo valores medios da rodada valida
        soma_medias_tempos_na_fila = 0.0
        soma_variancias_tempos_na_fila = 0.0
        for metrica in metricas_fase_principal:
            soma_variancias_tempos_na_fila += metrica.estimador_variancia_tempo_na_fila
            soma_medias_tempos_na_fila += metrica.estimador_tempo_medio_na_fila

        media_variancias_tempo_na_fila = soma_variancias_tempos_na_fila / kmin
        media_medias_tempo_na_fila = soma_medias_tempos_na_fila / kmin

        # intervalo de confianca dos tempos medios
        intervalo_de_confianca = self.__t_student.calcular_intervalo(kmin, media_variancias_tempo_na_fila)

        print('Tempo medio na fila de espera: %.4f, IC: %.4f. ' %
              (media_medias_tempo_na_fila, intervalo_de_confianca))

        print ('Fim da execucao principal! #coletas/rodada: %d, duracao: %dmin%.2fs' %
               (numero_de_coletas, duracao_minutos, duracao_segundos))
        print ('Tempo medio de espera na fila: %.2f, Var: %.2f' %
               (media_medias_tempo_na_fila,
                media_variancias_tempo_na_fila))

        # calculo das variancias  medias da simulacao na rodada
        soma_medias_tempos_no_sistema = 0.0
        soma_variancias_tempos_no_sistema = 0.0
        for metrica in metricas_fase_principal:
            soma_medias_tempos_no_sistema += metrica.estimador_tempo_medio_no_sistema
            soma_variancias_tempos_no_sistema += metrica.estimador_variancia_tempo_no_sistema

        media_medias_tempo_no_sistema = soma_medias_tempos_no_sistema / kmin
        media_variancias_tempo_no_sistema = soma_variancias_tempos_no_sistema / kmin


        print ('Tempo medio no sistema: %.2f, Var: %.2f' %
               (media_medias_tempo_no_sistema, media_variancias_tempo_no_sistema))
        print '\n'

        return lista_de_eventos, id_proximo_fregues, estado_do_servidor