import scipy.stats
import math

class TStudent:

    def calcular_intervalo(self, numero_de_amostras, valor_medio):
        alfa = .05 # o valor do intervalo de confianca de 95% foi definido no enunciado do trabalho
        graus_de_liberdade = numero_de_amostras - 1
        t_student = scipy.stats.t.ppf(1 - (alfa / 2), graus_de_liberdade)
        intervalo = (t_student * math.sqrt(valor_medio)) / math.sqrt(numero_de_amostras)
        return intervalo

    def calcular_limites(self, numero_de_amostras, media, variancia):
        intervalo = self.calcular_intervalo(numero_de_amostras,variancia)
        return media - intervalo, media + intervalo

    def verifica_intervalo_de_confianca(self, numero_de_amostras, valor_medio):
        intervalo_de_confianca = 2 * self.calcular_intervalo(numero_de_amostras, valor_medio)
        return intervalo_de_confianca <= (valor_medio / 10)
