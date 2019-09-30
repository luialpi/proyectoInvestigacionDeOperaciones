class MetodoSimplex:

	def __init__(self):
		pass

	'''
	simpexVar True para generar la matriz con variables
	'''
	def inicializarSimplex(self, simplexVar, matriz, esMaximo, archivo, variablesColumnas=None, variablesFilas=None):
		self.archivo = archivo
		if simplexVar == True:
			self.tablaSimplex = self.agregarVariablesDeHolgura(matriz)
			self.simularDespejeDeU()
		else:
			self.tablaSimplex = matriz
		self.esMaximo = esMaximo
		self.variablesColumnas = variablesColumnas if variablesColumnas != None else self.generarVariablesParaColumnas()
		self.variablesFilas = variablesFilas if variablesFilas != None else self.generarVariablesParaFilas()

	'''
	funcion principal del metodo simplex
	'''
	def mainSimplex(self):
		cantidadDeFilas = len(self.tablaSimplex)
		cantidadDeColumnas = len(self.tablaSimplex[0])
		columnaPivot = -1
		filaPivot = -1
		while(self.optimo(cantidadDeColumnas)):
			columnaPivot = self.encontrarColumnaPivot(cantidadDeColumnas)
			filaPivotYDegenerada = self.encontrarFilaPivot(cantidadDeFilas,cantidadDeColumnas,columnaPivot)
			filaPivot = filaPivotYDegenerada[0]
			self.intercambiarVariableEntrante(columnaPivot,filaPivot)
			if(self.verificarDegenerada(filaPivotYDegenerada[1])):
				print("solucion degenerada...")
			if(filaPivot < 0):
				print("solucion no acotada...")
				return []
			self.modificarFilaPivot(cantidadDeColumnas,columnaPivot,filaPivot)
			self.modificarFilas(cantidadDeFilas,cantidadDeColumnas,columnaPivot,filaPivot)
		return [self.tablaSimplex, self.variablesColumnas, self.variablesFilas]

	'''
	Funcion encargada la columnaPivot
	'''
	def encontrarColumnaPivot(self,cantidadDeColumnas):
		pivotMax=self.tablaSimplex[0][0]
		pivotMin=self.tablaSimplex[0][0]
		columna_pivot_indice_max=0
		columna_pivot_indice_min=0
		for x in range(cantidadDeColumnas-2):
			if pivotMax > self.tablaSimplex[0][x] and self.tablaSimplex[0][x] < 0 :
				pivotMax = (self.tablaSimplex[0][x])
				columna_pivot_indice_max=x
			if pivotMin < self.tablaSimplex[0][x] and self.tablaSimplex[0][x] > 0 :
				pivotMin = (self.tablaSimplex[0][x])
				columna_pivot_indice_min=x
		return columna_pivot_indice_max if self.esMaximo else columna_pivot_indice_min

	'''
	Funcion encargada de encontrar cual es el menor positivo
	y asi poder encontrar el numero pivot en la iteraccion
	'''
	def encontrarFilaPivot(self,cantidadDeFilas,cantidadDeColumnas,columnaPivot):
		pivot = -1
		pivotAuxiliar = 0
		indiceDeControl = 0
		listaParaDegenerada = []
		for x in range(1,cantidadDeFilas):
			if self.tablaSimplex[x][columnaPivot] > 0:
				division = self.tablaSimplex[x][cantidadDeColumnas-1] / self.tablaSimplex[x][columnaPivot]
				listaParaDegenerada.append(division)
				if( indiceDeControl == 0):
					indiceDeControl=indiceDeControl+1
					pivotAuxiliar = division
					pivot = x
				elif( division > 0 and division < pivotAuxiliar):
					pivotAuxiliar = division
					pivot = x
		return [pivot, listaParaDegenerada]

	'''
	Funcion que verifica la optimalidad de los resultados
	verifica la columna de resultados que ninguno sea negativo
	'''
	def optimalidadDeResultado(self,cantidadDeFilas):
		n=0
		fila=-1
		for x in range(1,cantidadDeFilas):
			if self.tablaSimplex[x][lentablaSimplex-1] < 0:
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
			valor = self.tablaSimplex[0][x]
			if(valor < 0):
				countMax+=1
			if(valor > 0):
				countMin+=1
		if self.esMaximo:
			return countMax > 0 
		else:
			return countMin > 0 
					
	'''
	Funcion que modifica la fila pivot para poner el numero pivot en 1
	'''
	def modificarFilaPivot(self,cantidadDeColumnas,columnaPivot,filaPivot):
		numeroPivot =  self.tablaSimplex[filaPivot][columnaPivot]
		for i in range(0, cantidadDeColumnas):
			self.tablaSimplex[filaPivot][i] = self.tablaSimplex[filaPivot][i] / numeroPivot

	'''
	Funcion que efectua operaciones en las filas de manera que se logre obtener un 0 en la columna pivot
	'''
	def modificarFilas(self,cantidadDeFilas,cantidadDeColumnas,columnaPivot,filaPivot):
		for i in range(0,cantidadDeFilas):
			variableParaDivision = self.tablaSimplex[i][columnaPivot]
			if( i != filaPivot ):
				for j in range(0,cantidadDeColumnas):
					self.tablaSimplex[i][j] = self.tablaSimplex[i][j] - ( self.tablaSimplex[filaPivot][j] * variableParaDivision)

	'''
	Funcion que modifica la variable entrante y la pone en lugar de la saliente
	'''
	def intercambiarVariableEntrante(self,columnaPivot,filaPivot):
		self.variablesFilas[filaPivot]=self.variablesColumnas[columnaPivot]

	'''
	Funcion que verifica si se trata de un problema con multiples soluciones
	'''
	def verificarMultiplesSoluciones(self):
		variablesNoBasicas=len(self.variablesFilas)
		for i in range(0,len(self.tablaSimplex[0])-2):
			numero =  self.tablaSimplex[0][i]
			variable = self.variablesColumnas[i]
			print(variable, numero)
			if variable not in self.variablesFilas and numero == 0:
				return i
		return -1

	def agregarVariablesDeHolgura(self, matriz):
		numeroDeVariables = len(matriz) -1
		iteraccion = 0
		for i in range(0, len(matriz)):
			matriz[i] = matriz[i][:-1]
			for n in range(0, numeroDeVariables):
				if i == 0:
					matriz[i].insert(len(matriz[i])-1,0)
				else:
					matriz[i].insert(len(matriz[i])-1,1) if i == n+1 else matriz[i].insert(len(matriz[i])-1,0)
		return matriz

	def simularDespejeDeU(self):
		for i in range( 0, len( self.tablaSimplex[0] ) -1 ):
			self.tablaSimplex[0][i]*=-1
 		
	def generarVariablesParaColumnas(self):
		cantidadResticciones = len(self.tablaSimplex)-1
		cantidadDeVariables = len(self.tablaSimplex[0])-(cantidadResticciones+1)
		nombresColumnas=[]
		for valor in range(cantidadDeVariables):
			nombresColumnas.append("x" + str(valor + 1))
		for valor in range(cantidadResticciones):
			nombresColumnas.append("S" + str(valor + 1))
		nombresColumnas.append("RESULTADO")
		return nombresColumnas

	def generarVariablesParaFilas(self):
		cantidadResticciones = len(self.tablaSimplex)-1
		nombresFilas = ['U']
		for valor in range(cantidadResticciones):
			nombresFilas.append("S" + str(valor + 1))
		return nombresFilas

	def verificarDegenerada(self, arreglo):
		visto = set()
		unico = [x for x in arreglo if x not in visto and not visto.add(x)] 
		return len(unico) < 0

	##No factible: que uno de los valores finales no cumple con las restricciones iniciales
##fin