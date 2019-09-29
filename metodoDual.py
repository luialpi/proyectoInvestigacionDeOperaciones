import metodoSimplex

class metodoDual:
	def __init__(self):
		pass

	def mainDual(self, matrizInicial, esMaximo):
		matrizDual = self.transpuesta(matrizInicial)
		metodoSimplex = metodoSimplex()
		metodoSimplex.inicializarSimplex(True, matrizDual, esMaximo)
		matrizDual = metodoSimplex.mainSimplex()

	def transpuesta(self, matrizDual):
		resultado = []
		for i in range(len(matrizDual)):
			for j in range(len(matrizDual[0])):
				resultado[j][i] = matrizDual[i][j]
		return resultado