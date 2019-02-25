from eventos import eventobase, eventochegada, eventoatendimento, eventosaida
from enums import tipoevento

chegada = tipoevento.TipoEvento.chegada
atendimento = tipoevento.TipoEvento.atendimento
saida = tipoevento.TipoEvento.saida

class GeraEvento:
    '''
    Objeto auxiliar para geracao de eventos de forma semanticamente mais enxuta
    '''

    def __init__(self, gerador_exponencial):
        self.__gerador_exponencial = gerador_exponencial

    def __gera_evento_base(self, instante_do_evento, id_fregues):

        return eventobase.EventoBase(instante_do_evento + self.__gerador_exponencial.amostra(), id_fregues)

    def gera_evento_de_chegada(self, instante_do_evento, id_fregues):
        return eventochegada.EventoChegada(self.__gera_evento_base(instante_do_evento, id_fregues))

    def gera_evento_de_atendimento(self, instante_do_evento, instante_do_evento_anterior, id_fregues):
        return eventoatendimento\
            .EventoAtendimento(self.__gera_evento_base(instante_do_evento, id_fregues),
                               instante_do_evento_anterior)

    def gera_evento_de_saida(self, instante_do_evento, instante_do_evento_anterior, id_fregues):
        return eventosaida\
            .EventoSaida(self.__gera_evento_base(instante_do_evento, id_fregues),
                         instante_do_evento_anterior)