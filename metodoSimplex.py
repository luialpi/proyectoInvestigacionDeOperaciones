class SimplexMethod:

	def __init__(self, matriz, variablesColumnas, variablesFilas, esMaximo):
		self.matrizTabla = matriz
		self.esMaximo = esMaximo
		self.variablesColumnas = variablesColumnas
		self.variablesFilas = variablesFilas

	'''
	funcion principal del metodo simplex
	'''
	def simplex(self):
		cantidadDeFilas = len(self.matrizTabla)
		cantidadDeColumnas = len(self.matrizTabla[0])
		columnaPivot = -1
		filaPivot = -1

		print(self.matrizTabla)
		print(self.variablesFilas)

		while(self.optimo(cantidadDeColumnas)):
			columnaPivot = self.encontrarColumnaPivot(cantidadDeColumnas)
			filaPivot = self.encontrarFilaPivot(cantidadDeFilas,cantidadDeColumnas,columnaPivot)
			self.intercambiarVariableEntrante(columnaPivot,filaPivot)

			if(filaPivot < 0):
				print("solucion no acotada...")
				break

			self.modificarFilaPivot(cantidadDeColumnas,columnaPivot,filaPivot)
			self.modificarFilas(cantidadDeFilas,cantidadDeColumnas,columnaPivot,filaPivot)

			print(self.matrizTabla)
			print(self.variablesFilas, self.variablesColumnas)

	'''
	Funcion encargada de encontrar el mas negativo
	para asi saber cual es la columna pivot
	'''
	def encontrarColumnaPivot(self,cantidadDeColumnas):
		if self.esMaximo:
			return self.encontrarColumnaPivotMax(cantidadDeColumnas)
		else:
			return self.encontrarColumnaPivotMin(cantidadDeColumnas)
			
	'''
	Funcion encargada de encontrar el mas negativo
	para asi saber cual es la columna pivot
	'''
	def encontrarColumnaPivotMax(self,cantidadDeColumnas):
		
		pivot=self.matrizTabla[0][0]
		columna_pivot_indice=0
		for x in range(cantidadDeColumnas-2):
			if pivot > self.matrizTabla[0][x] and self.matrizTabla[0][x] < 0 :
				pivot = (self.matrizTabla[0][x])
				columna_pivot_indice=x
		return columna_pivot_indice

	'''
	Funcion encargada de encontrar el mas positivo
	para asi saber cual es la columna pivot
	'''
	def encontrarColumnaPivotMin(self,cantidadDeColumnas):
		pivot=(self.matrizTabla[0][0])
		columna_pivot_indice=0
		for x in range(cantidadDeColumnas-2):
			if pivot < self.matrizTabla[0][x] and self.matrizTabla[0][x] > 0 :
				pivot = (self.matrizTabla[0][x])
				columna_pivot_indice=x
		return columna_pivot_indice

	'''
	Funcion encargada de encontrar cual es el menor positivo
	y asi poder encontrar el numero pivot en la iteraccion
	'''
	def encontrarFilaPivot(self,cantidadDeFilas,cantidadDeColumnas,columnaPivot):
		pivot = -1
		pivotAuxiliar = 0
		indiceDeControl = 0
		for x in range(1,cantidadDeFilas):
			if self.matrizTabla[x][columnaPivot] > 0:
				division = self.matrizTabla[x][cantidadDeColumnas-1] / self.matrizTabla[x][columnaPivot]
				if( indiceDeControl == 0):
					indiceDeControl=indiceDeControl+1
					pivotAuxiliar = division
					pivot = x
				elif( division > 0 and division < pivotAuxiliar):
					pivotAuxiliar = division
					pivot = x
		return pivot

	'''
	Funcion que verifica la optimalidad de los resultados
	verifica la columna de resultados que ninguno sea negativo
	'''
	def optimalidadDeResultado(self,cantidadDeFilas):
		n=0
		fila=-1
		for x in range(1,cantidadDeFilas):
			if self.matrizTabla[x][lenMatrizTabla-1] < 0:
				return False
		return True

	'''
	Funcion que verifica si ya se obtuvo el valor optimo en el caso de maximizacion
	para ello verifica que aun existan numeros positivos y retorna true en caso de que aun exista una columna con u positivo
	'''
	def optimo(self,cantidadDeColumnas):
		countMax = 0
		countMin = 0
		for x in range(0,cantidadDeColumnas-1):
			valor = self.matrizTabla[0][x]
			if(valor < float(0)):
				countMax+=1
			if(valor > float(0)):
				countMin+=1

		if self.esMaximo:
			return True if countMax > 0 else False
		else:
			return True if countMin > 0 else False
					
	'''
	Funcion que modifica la fila pivot para poner el numero pivot en 1
	'''
	def modificarFilaPivot(self,cantidadDeColumnas,columnaPivot,filaPivot):
		numeroPivot =  self.matrizTabla[filaPivot][columnaPivot]
		for i in range(0, cantidadDeColumnas):
			self.matrizTabla[filaPivot][i] = self.matrizTabla[filaPivot][i] / numeroPivot

	'''
	Funcion que efectua operaciones en las filas de manera que se logre obtener un 0 en la columna pivot
	'''
	def modificarFilas(self,cantidadDeFilas,cantidadDeColumnas,columnaPivot,filaPivot):
		for i in range(0,cantidadDeFilas):
			variableParaDivision = self.matrizTabla[i][columnaPivot]
			if( i != filaPivot ):
				for j in range(0,cantidadDeColumnas):
					self.matrizTabla[i][j] = self.matrizTabla[i][j] - ( self.matrizTabla[filaPivot][j] * variableParaDivision)

	'''
	Funcion que modifica la variable entrante y la pone en lugar de la saliente
	'''
	def intercambiarVariableEntrante(self,columnaPivot,filaPivot):
		self.variablesFilas[filaPivot]=self.variablesColumnas[columnaPivot]

