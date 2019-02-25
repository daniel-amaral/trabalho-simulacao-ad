import random as random
import time as time
import matplotlib.pyplot as plt
from auxiliar.execucaoprincipal import ExecucaoPrincipal
from auxiliar.fasetransiente import FaseTransiente
from distribuicoes import exponencial
from entidades.evento import Evento
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

# recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
gerador_numeros_aleatorios = random
try:
    nome_arquivo_seed = 'seed'
    seed = open(nome_arquivo_seed, 'r').read()
    gerador_numeros_aleatorios.seed(seed)
except:
    pass


# estruturas que controlam as fases transientes e principal
fase_transiente = FaseTransiente()
execucao_principal = ExecucaoPrincipal()


inicio_da_execucao = time.time()

# Grandes lacos (loops) do simulador:
for disciplina in disciplinas:

    # Iniciando estruturas e variaveis basicas do simulador:
    lista_de_eventos = ListaDeEventos()
    fila_de_espera = FilaDeEspera(disciplina)
    id_proximo_fregues = 0
    instante_proximo_evento = 0.0
    proximo_evento = Evento(TipoEvento.chegada, instante_proximo_evento)
    lista_de_eventos.insere_evento(proximo_evento)
    estado_do_servidor = EstadoServidor.livre

    for utilizacao in utilizacoes:

        # Variaveis basicas da simulacao numa utilizacao definida:
        taxa_de_chegada = aux.calcula_taxa_de_chegada(utilizacao, tempo_medio_servico)
        taxa_de_servico = aux.calcula_taxa_de_servico(tempo_medio_servico)
        gerador_exponencial = exponencial.Exponencial(taxa_de_chegada, taxa_de_servico, gerador_numeros_aleatorios)

        # Execucao da fase transiente:
        metricas_fase_transiente = [] # para cada Delta(t) da fase transiente metricas sao avaliadas separadamente
        trata_evento.set_primeiro_fregues_a_avaliar(id_proximo_fregues)
        lista_de_eventos, id_proximo_fregues, estado_do_servidor \
            = fase_transiente.rodar(id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_do_servidor,
                                    trata_evento, gerador_exponencial, metricas_fase_transiente, utilizacao)

        # Execucao principal em modo batch:
        kmin = 3200 # numero de rodadas inicial
        metricas_execucao_principal = [] # para cada rodada as metricas sao avaliadas separadamente
        lista_de_eventos, id_proximo_fregues, estado_do_servidor = \
            execucao_principal.rodar(kmin, id_proximo_fregues, lista_de_eventos, fila_de_espera, estado_do_servidor,
                                     trata_evento, gerador_exponencial, metricas_execucao_principal, utilizacao)


print('Duracao da simulacao: %s' %aux.duracao_to_str(inicio_da_execucao, time.time()))

# A semente do gerador de numeros aleatorios e' persistida em arquivo para ser utilizada na proxima execucao do programa
estado_final_do_gerador = gerador_numeros_aleatorios.getstate()
file = open(nome_arquivo_seed, 'w')
file.write(str(estado_final_do_gerador))