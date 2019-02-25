import random as random
import time as time
import matplotlib.pyplot as plt
from auxiliar.fasetransiente import FaseTransiente
from distribuicoes import exponencial
from enums.disciplina import Disciplina
from enums.tipoevento import TipoEvento
from enums.estadoservidor import EstadoServidor
from estruturas.listadeeventos import ListaDeEventos
from estruturas.filadeespera import FilaDeEspera
from auxiliar.metricas import Metricas
from auxiliar import funcoesauxiliares, trataevento
from entidades import fregues, evento

# Valores absolutos definidos na descricao do trabalho:
tempo_medio_servico = 1.0
numero_de_rodadas = 10

# Valores que mudam de acordo com a configuracao do simulador:
utilizacoes = [.2, .4, .6, .8, .9]
disciplinas = [Disciplina.FCFS, Disciplina.LCFS]

# Declaracao de funcoes auxiliares
trata_evento = trataevento.TrataEvento()
aux = funcoesauxiliares.FuncoesAuxiliares()
gerador_numeros_aleatorios = random
fase_transiente = FaseTransiente()

# Grandes lacos (loops) do simulador:
for disciplina in disciplinas:

    # Iniciando estruturas e variaveis basicas do simulador:
    lista_de_eventos = ListaDeEventos()
    fila_de_espera = FilaDeEspera(disciplina)
    id_proximo_fregues = 0

    for utilizacao in utilizacoes:

        # Variaveis basicas da simulacao numa utilizacao definida:
        taxa_de_chegada = aux.calcula_taxa_de_chegada(utilizacao, tempo_medio_servico)
        taxa_de_servico = aux.calcula_taxa_de_servico(tempo_medio_servico)
        gerador_exponencial = exponencial.Exponencial(taxa_de_chegada, taxa_de_servico, gerador_numeros_aleatorios)

        # Execucao da fase transiente:
        tempo_fase_transiente = 0.0
        metricas_fase_transiente = [] # para cada Delta(t) da fase transiente metricas sao avaliadas separadamente
        id_proximo_fregues = fase_transiente.rodar(id_proximo_fregues, lista_de_eventos,
                                                  fila_de_espera, trata_evento, gerador_exponencial,
                                                  metricas_fase_transiente, utilizacao)