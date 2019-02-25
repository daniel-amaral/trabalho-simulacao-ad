import time
from auxiliar.metricas import Metricas
from entidades.evento import Evento
from enums.estadoservidor import EstadoServidor
from enums.tipoevento import TipoEvento
import matplotlib.pyplot as plt

class FaseTransiente:

    def rodar(self, id_proximo_fregues, lista_de_eventos, fila_de_espera,
              trata_evento, gerador_exponencial, metricas_fase_transiente, utilizacao):

        print ('\nInicio de fase transiente: %s, utilizacao: %.1f' % (fila_de_espera.disciplina.name, utilizacao))
        inicio_fase_transiente = time.time()

        # Configuracao de inicio do sistema
        estado_do_servidor = EstadoServidor.livre
        evento_chegada_inicial = Evento(TipoEvento.chegada, 0.0)
        lista_de_eventos.insere_evento(evento_chegada_inicial)

        # Configuracao para avaliacao das janelas de tempo na fase transiente
        id_janela_de_tempo = 0
        metricas_fase_transiente.append(Metricas())
        janela_de_tempo = 60.0 * (10 / utilizacao)  # em segundos
        fim_janela_de_tempo = janela_de_tempo
        grafico_fase_transiente_x = []
        grafico_fase_transiente_y = []
        grafico_fase_transiente_erro = []

        # Rodadas da fase transiente:
        while True:
            proximo_evento = lista_de_eventos.proximo_evento()
            print_var = False
            if proximo_evento.tipo_de_evento == TipoEvento.saida:
                print_var = True
            estado_do_servidor = trata_evento. \
                trata(proximo_evento, estado_do_servidor, lista_de_eventos, fila_de_espera,
                      gerador_exponencial, id_proximo_fregues, metricas_fase_transiente[id_janela_de_tempo])

            # Avaliacao de fase transiente:
            if proximo_evento.instante >= fim_janela_de_tempo:
                fim_janela_de_tempo = proximo_evento.instante
                grafico_fase_transiente_x.append(fim_janela_de_tempo / 60)  # eixo x em minutos
                tempo_medio_no_sistema = metricas_fase_transiente[id_janela_de_tempo].estimador_tempo_medio_no_sistema
                grafico_fase_transiente_y.append(tempo_medio_no_sistema)
                erro_do_tempo_medio = metricas_fase_transiente[id_janela_de_tempo].estimador_variancia_tempo_na_fila / 2
                grafico_fase_transiente_erro.append(erro_do_tempo_medio)
                fim_janela_de_tempo += janela_de_tempo
                metricas_fase_transiente.append(Metricas())

                # Avaliacao termino da fase transiente:
                fim_fase_transiente = False
                numero_de_rodadas_a_avaliar = 10
                if (id_janela_de_tempo >= numero_de_rodadas_a_avaliar):
                    fim_fase_transiente = True
                    for i in range(numero_de_rodadas_a_avaliar):
                        id = id_janela_de_tempo - i
                        valor = grafico_fase_transiente_y[id]
                        erro = grafico_fase_transiente_erro[id]
                        valor_inferior = valor - erro
                        valor_superior = valor + erro
                        if tempo_medio_no_sistema < valor_inferior or tempo_medio_no_sistema > valor_superior:
                            fim_fase_transiente = False
                            break
                if fim_fase_transiente:
                    break
                id_janela_de_tempo += 1

            if proximo_evento.tipo_de_evento == TipoEvento.chegada:
                id_proximo_fregues = proximo_evento.fregues.id + 1

        duracao = time.time() - inicio_fase_transiente
        duracao_minutos = int(duracao / 60)
        duracao_segundos = duracao - (duracao_minutos * 60)
        print ('Fim da fase transiente! Duracao: %dmin%.2fs\n' % (duracao_minutos, duracao_segundos))

        # Plot de grafico sobre fase transiente (utilizado apenas em analises de corretude do trabalho):
        # media_das_variancias_na_fase_transiente = sum(grafico_fase_transiente_y) / len(grafico_fase_transiente_y)
        # extremidades_grafico_fase_transiente = [grafico_fase_transiente_x[0], grafico_fase_transiente_x[-1]]
        #
        # plt.scatter(grafico_fase_transiente_x, grafico_fase_transiente_y, s=[4] * len(grafico_fase_transiente_x))
        # plt.errorbar(grafico_fase_transiente_x, grafico_fase_transiente_y, yerr=grafico_fase_transiente_erro, linestyle="None")
        # plt.plot(extremidades_grafico_fase_transiente,
        #          [media_das_variancias_na_fase_transiente, media_das_variancias_na_fase_transiente])
        # plt.xlabel('Instante (min)')
        # plt.ylabel('Tempo medio no sistema [s]')
        # plt.title('Fase Transiente')
        # plt.show()

        return id_proximo_fregues