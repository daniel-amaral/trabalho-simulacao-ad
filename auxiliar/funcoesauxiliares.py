

class FuncoesAuxiliares:
    '''
    Para deixar o codigo mais organizado, esta classe acumula algumas funcoes que sao rotinas comuns do simulador
    '''

    def calcula_taxa_de_chegada(self, utilizacao, tempo_medio_servico):
        return utilizacao * tempo_medio_servico

    def calcula_taxa_de_servico(self, tempo_medio_servico):
        return 1 / tempo_medio_servico

    def duracao_to_str(self, inicio, fim):
        duracao = fim - inicio
        duracao_minutos = int(duracao / 60)
        duracao_segundos = duracao - (duracao_minutos * 60)
        return '%dmin%.2fs' % (duracao_minutos, duracao_segundos)