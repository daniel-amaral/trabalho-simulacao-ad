from enums import disciplina

FCFS = disciplina.Disciplina.FCFS
LCFS = disciplina.Disciplina.LSFS

class FilaDeEspera:
    '''
    A fila de espera do sistema
    '''

    def __init__(self, disciplina):
        self.__disciplina = disciplina
        self.__fila = []

    def insere_fregues(self, fregues):
        self.__fila.append(fregues)

    def proximo_evento(self):
        if (self.disciplina == FCFS):
            return self.__fila.pop(0)
        return  self.__fila.pop()