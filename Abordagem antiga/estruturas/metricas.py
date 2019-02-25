

class Metricas():
    '''
    Objeto que faz a auditoria dos eventos e obtem algumas metricas estatisticas
    '''

    def __init__(self):
        self.__num_fregueses_entraram_em_servico = 0
        self.__tempo_total_espera_na_fila = 0.0
        self.__tempos_na_fila = []
        self.__num_fregueses_sairam_do_sistema = 0
        self.__tempo_total_no_sistema = 0.0
        self.__tempos_no_sistema = []

    @property
    def num_fregueses_entraram_em_servico(self):
        return self.__num_fregueses_entraram_em_servico

    def incrementar_num_fregueses_entraram_em_servico(self):
        self.__num_fregueses_entraram_em_servico += 1

    @property
    def tempo_total_espera_na_fila(self):
        return self.__tempo_total_espera_na_fila

    def incrementar_tempo_de_espera_na_fila(self, tempo_acumulado):
        tempo_incrementado = tempo_acumulado - self.__tempo_total_espera_na_fila
        if (tempo_incrementado <= 0):
            raise Exception("Tempo incrementado nao esta positivo")
        self.__tempos_na_fila.append(tempo_incrementado)
        self.__tempo_total_espera_na_fila = tempo_acumulado

    @property
    def num_fregueses_sairam_do_sistema(self):
        return self.__num_fregueses_sairam_do_sistema

    def incrementar_num_fregueses_sairam_do_sistema(self):
        self.__num_fregueses_sairam_do_sistema += 1

    @property
    def tempo_total_no_sistema(self):
        return self.__tempo_total_no_sistema

    def incrementar_tempo_total_no_sistema(self, tempo_acumulado):
        tempo_incrementado = tempo_acumulado - self.__tempo_total_no_sistema
        if (tempo_incrementado <= 0):
            raise Exception("Tempo incrementado nao esta positivo")
        self.__tempos_no_sistema.append(tempo_incrementado)
        self.__tempo_total_no_sistema = tempo_acumulado

    def __estimador_variancia(self, xis, n):
        quadrados_dos_xis = [x * x for x in xis]
        somatorio_xis = sum(xis)
        try:
            variancia = sum(quadrados_dos_xis) / (n - 1) + somatorio_xis * somatorio_xis / n * (n - 1)
        except ZeroDivisionError:
            variancia = float('inf')
        return variancia

    @property
    def tempo_medio_na_fila(self):
        return self.tempo_total_espera_na_fila / self.num_fregueses_entraram_em_servico

    @property
    def estimador_variancia_tempo_na_fila(self):
        xis = self.__tempos_na_fila
        n = self.num_fregueses_entraram_em_servico
        return self.__estimador_variancia(xis, n)

    @property
    def tempo_medio_no_sistema(self):
        return self.tempo_total_no_sistema / self.num_fregueses_sairam_do_sistema

    @property
    def estimador_variancia_tempo_no_sistema(self):
        xis = self.__tempos_no_sistema
        n = self.num_fregueses_sairam_do_sistema
        return self.__estimador_variancia(xis, n)


