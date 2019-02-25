import random as random
from distribuicoes import exponencial
from estruturas import listadeeventos, metricas, filadeespera
from auxiliar import funcoesauxiliares
from constantes import constantes
from enums import disciplina, estadoservidor
from eventos import geraevento, eventosaida

# Valores absolutos definidos na descricao do trabalho:
tempo_medio_servico = 1.0
numero_de_rodadas = 10

# Variaveis auxiliares para simplificar a leitura do codigo:
FCFS = disciplina.Disciplina.FCFS
LCFS = disciplina.Disciplina.LSFS
unidade_de_tempo = constantes.UNIDADE_DE_TEMPO
aux = funcoesauxiliares.FuncoesAuxiliares()

# Valores que mudam de acordo com a configuracao do simulador:
utilizacao = 0.2
k = 10  # numero de coletas por rodada


# Iniciando estruturas basicas para a simulacao
taxa_de_chegada = aux.calcula_taxa_de_chegada(utilizacao, tempo_medio_servico)
gerador_numeros_aleatorios = random
gerador_exponencial = exponencial.Exponencial(taxa_de_chegada, gerador_numeros_aleatorios)
gerador_de_eventos = geraevento.GeraEvento(gerador_exponencial)
lista_de_eventos = listadeeventos.ListaDeEventos(FCFS)
fila_de_espera = filadeespera.FilaDeEspera(FCFS)
tempo_fase_transiente = 0.0
numero_de_rodadas_da_fase_transiente = 10
id_proximo_fregues = 0
estado_servidor = estadoservidor.EstadoServidor.livre
metricas_fase_transiente = metricas.Metricas()


def roda_fase_transiente():
    global id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_servidor, gerador_de_eventos
    print 'Inicio da fase transiente'
    evento_chegada_inicial = gerador_de_eventos.gera_evento_de_chegada(0, id_proximo_fregues)
    fila_de_eventos.insere_evento(evento_chegada_inicial)
    while id_proximo_fregues < numero_de_rodadas_da_fase_transiente:
        proximo_evento = fila_de_eventos.proximo_evento()
        estado_servidor = proximo_evento\
            .trata_evento(estado_servidor, fila_de_eventos, fila_de_espera, id_proximo_fregues, gerador_de_eventos, metricas_fase_transiente)
        if proximo_evento.__class__ == eventosaida.EventoSaida:
            print 'Fregues ' + str(id_proximo_fregues) + ' saiu!'
            print 'Variancia estimada: ' + str(metricas_fase_transiente.estimador_variancia_tempo_no_sistema)
            id_proximo_fregues = proximo_evento.id_fregues
    print '\nFim da fase transiente!'

roda_fase_transiente()









# import matplotlib.pyplot as plt
#
# # seed = 12
# # random.seed(seed)
# # state = random.getstate()
# exp = exponencial.Exponencial(taxa_de_chegada, gerador_numeros_aleatorios)
# x_values = []
# y_values = []
#
# for x in range(1000):
#     sample = exp.sample()
#     print str(sample)
#     x_values.append(x)
#     y_values.append(sample)
#
# plt.plot(x_values, y_values)
# plt.xlabel('#')
# plt.ylabel('Amostras')
# plt.title('Exemplo')
# plt.show()







