from scipy.stats import chisquare

class ChiSquare:

    def tabela(self, numero_de_amostras):
        alfa = 0.05 # intervalo de confianca de 95% definido no enunciado do trabalho
        valor_da_tabela = chisquare()
