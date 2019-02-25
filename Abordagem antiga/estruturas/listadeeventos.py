from enums import disciplina

FCFS = disciplina.Disciplina.FCFS
LCFS = disciplina.Disciplina.LSFS

class ListaDeEventos:
    '''
    Este objeto representa a lista de eventos do sistema
    '''

    def __init__(self, disciplina):
        self.__disciplina = disciplina
        self.__lista_de_eventos = []

    @property
    def disciplina(self):
        return self.__disciplina

    def insere_evento(self, evento):
        self.__lista_de_eventos.append(evento)

    def proximo_evento(self):
        ret = self.__lista_de_eventos[0]
        for evento in self.__lista_de_eventos[1:]:
            ret = evento if evento.instante_do_evento < ret.instante_do_evento else ret
        return ret

