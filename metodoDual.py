from ControladorMetodoGranM import *
from DosFases import *
class MetodoDual:
	def __init__(self):
		pass

	def mainDual(self, matrizInicial, esMaximo, archivo):
		self.archivo = archivo
		arrayColumnas=[]
		arrayFilas=[]
		matrizSinRestricciones=self.quitarRestricciones(matrizInicial)
		matrizSinRestricciones=self.verificarFilas(matrizInicial,matrizSinRestricciones,esMaximo)
		matrizSinRestricciones=self.moverUDeFilaAbajo(matrizSinRestricciones)
		matrizTranspuesta=self.transpuesta(matrizSinRestricciones)
		matrizDual=self.moverUDeFilaArriba(matrizTranspuesta)
		matrizDualFinal=self.agregarRestricciones(matrizDual,esMaximo)
		dosFases = metodoDosFases()
		solucionDosFases = dosFases.mainDosFases(matrizDualFinal,not esMaximo,archivo)
		

		# granM = Controlador(not esMaximo,matrizDualFinal[0][:-1],matrizDualFinal[1:],len(matrizDualFinal[0])-1,archivo)
		# granM.inicioControlador()

	def transpuesta(self, matrizDual):
		resultado =[]
		for j in range(len(matrizDual)):
			fila = []
			for i in range(len(matrizDual[0])):
				print(matrizDual[i][j])
				fila.append(matrizDual[i][j])
			resultado.append(fila)
			
		return resultado

	def verificarFilas(self,matriz,matrizSinRestricciones,esMaximo):
		indice = -1
		lista=[]
		for fila in matriz:
			indice+=1
			if(esMaximo and fila[-1] == ">="):
				lista.append(self.cambiarSigno(matrizSinRestricciones[indice]))
			elif(not esMaximo and fila[-1] == "<="):
				lista.append(self.cambiarSigno(matrizSinRestricciones[indice]))
			else:
				lista.append(matrizSinRestricciones[indice])

		return lista


	def moverUDeFilaAbajo(self, matrizDual):
		matriz = matrizDual[1:]
		matriz.append(matrizDual[0])
		return matriz

	def moverUDeFilaArriba(self, matrizDual):
		matriz = matrizDual[:-1]
		matriz.insert(0,matrizDual[-1])
		return matriz

	def quitarRestricciones(self, matrizDual):
		tabla=[]
		for fila in matrizDual:
			tabla.append(fila[:-1])
		return tabla

	def cambiarSigno(self, lista):
		listaDeItems = []
		for item in lista:
			listaDeItems.append(item*-1)
		return listaDeItems

	def agregarRestricciones(self, matriz, esMaximo):
		tabla = []
		len = 0
		for fila in matriz:
			if( len != 0 ):
				if(esMaximo):
					fila.append(">=")
				else:
					fila.append("<=")
				tabla.append(fila)
			else:
				tabla.append(fila)
				len=len+1
		return tabla
