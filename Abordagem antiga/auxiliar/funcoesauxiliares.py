

class FuncoesAuxiliares:
    '''
    Para deixar o codigo mais organizado, esta classe acumula algumas funcoes que sao rotinas comuns do simulador
    '''

    def calcula_taxa_de_chegada(self, utilizacao, tempo_medio_servico):
        return utilizacao * tempo_medio_servico