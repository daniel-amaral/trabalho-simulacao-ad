from enums.disciplina import Disciplina

class FilaDeEspera:
    '''
    A fila de espera do sistema
    '''

    def __init__(self, disciplina):
        self.__disciplina = disciplina
        self.__fila = []

    def insere_fregues(self, fregues):
        self.__fila.append(fregues)

    def proximo_fregues(self):
        if (self.__disciplina == Disciplina.FCFS):
            return self.__fila.pop(0)
        return  self.__fila.pop()

    def esta_vazia(self):
        if len(self.__fila) == 0:
            return True
        return False

    @property
    def count(self):
        return len(self.__fila)

    @property
    def disciplina(self):
        return self.__disciplina