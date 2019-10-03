from metodoSimplex import *
simplex = MetodoSimplex()

class metodoDosFases:
	
	def __init__(self):
		pass
		
		'''
		Se genera la tabla de la primera fase
		tabla: contiene la funcion objetivo y restricciones
		esMaximo: True si tiene que maximizar y false si no
		archivo: archivo al cual escribir
		
		Aqui se hacen las llamadas a los metodos para Fase 1 y 2
		'''    
	def mainDosFases(self,tabla,esMaximo,archivo):
		self.tabla = tabla
		self.esMaximo = esMaximo
		self.archivo = archivo
		infoF1 = self.generarTablaF1(tabla,esMaximo,archivo)
		#print("infoF1[0]",infoF1[0])
		tablaF1 = list(map(list, infoF1[0]))#Agarro la tabla
		variablesColumnas = infoF1[1]#Agarro la lista con las variables de columnas
		variablesFilas = infoF1[2]#Agarro la lista con las variables de filas
		tablaF1[0] = infoF1[3].copy()
		infoF2 = self.generarTablaF2(tablaF1, esMaximo, archivo, variablesColumnas, variablesFilas)
		tablaF2 = list(map(list, infoF2[0]))
		variablesColumnas = infoF2[1]
		variablesFilas = infoF2[2]
		#printTabla(tablaF2,variablesColumnas,variablesFilas)
		return tablaF2
	'''
	Se realiza la fase 1.
	Primero se agregan las variables de holgura o artificiales segun la restriccion.
	Luego, se copia la fila de U para poder sustituirla en la segunda fase
	luego se cambia la fila U de la tabla por la suma entre las filas artificiales
	teniendo la tabla asi, se realizan las iteraciones del metodo simplex y se devuelve la tabla 
	'''
		
	def generarTablaF1(self,tabla,esMaximo,archivo):
		aumentada = simplex.agregarVariablesSegunInecuacion(tabla)
		tablaF1 = list(map(list, aumentada[0]))
		filaUOriginal = tablaF1[0].copy()
		#print(filaUOriginal)
		variablesColumnas = aumentada[1]
		variablesFilas = aumentada[2]
		for i in range(len(tablaF1[0])):
			tablaF1[0][i] = 0
			for k in range(len(tablaF1)):
				if variablesFilas[k].startswith("R") and variablesColumnas[i].startswith(("x","S","RES")):
					tablaF1[0][i] += tablaF1[k][i]*-1
		print("Tablas Fase 1:")
		simplex.inicializarSimplex(False, tablaF1,True, archivo, variablesColumnas, variablesFilas)
		infoF1 = simplex.mainSimplex()
		infoF1+=[filaUOriginal] #Para enviarla a fase 2 a sustituir
		return infoF1
		
		'''
		Se remueven las columnas de variables artificiales. Se recibe la fila a la cual removerle dichos valores
		y se retorna esta fila sin esas variables
		'''
	def removerArtificiales(self,variablesColumnas, fila):
		filaSinArtificiales = []
		for variable in variablesColumnas:
			if not (variable.startswith("R") and variable != "RESULTADO"):
				filaSinArtificiales += [fila[variablesColumnas.index(variable)]]
		return filaSinArtificiales
	'''
	Se genera la tabla para la segunda fase
	Se mandan a remover las variables artificiales y luego a hacer ceros las variables basicas.
	una vez hecho esto se realiza el simplex para obtener la solucion
	'''
	def generarTablaF2(self, tabla, esMaximo, archivo, variablesColumnas, variablesFilas):
		tabla[0] = [x*-1 for x in tabla[0]]
		for i in range(len(tabla)):
			tabla[i] = self.removerArtificiales(variablesColumnas, tabla[i]).copy()
		variablesColumnas = self.removerArtificiales(variablesColumnas, variablesColumnas)
		#print("\n\nTabla Fase 2:")
		#self.printTabla(tabla, variablesColumnas, variablesFilas)
		#print("\n\nTabla después de hacerCeros")
		print("Tablas Fase 2:")
		tabla = self.hacerCeros(tabla,variablesColumnas,variablesFilas)
		#self.printTabla(tabla, variablesColumnas, variablesFilas)
		simplex.inicializarSimplex(False, tabla, esMaximo, archivo, variablesColumnas, variablesFilas)
		infoF2 = simplex.mainSimplex()
		return infoF2
	'''
	Se resuelve para las variables basicas. Ya que estas tendrian coeficientes por la sustitucion en U, se hacen las operaciones
	correspondientes para ponerlas en 0.
	'''
	def hacerCeros(self, tabla, variablesColumnas, variablesFilas):
		for variable in variablesFilas:
			if variable.startswith("x"):
				index = variablesFilas.index(variable)
				indexCol = variablesColumnas.index(variable)
				i = 0
				pivote = tabla[0][indexCol]
				for x in tabla[index]:
					tabla[0][i]+= x*(pivote*-1)
					i+=1
		return tabla

'''
	def printTabla(self, tabla, variablesColumnas, variablesFilas):
		for a in range(len(tabla)):
			print()
			for b in range(len(tabla[0])):
				print(tabla[a][b], end = ' ')
		print("\n\nVariables de las Columnas:")
		print(variablesColumnas)
		print("\nVariables de las Filas:")
		print(variablesFilas)
		print()

	'''

#x = metodoDosFases()
#[[0.4,0.5,0,'='],[0.3,0.1,2.7,'<='],[0.5,0.5,6,'='],[0.6,0.4,6,'>=']],False
#[[4,2,3,5,0,'='],[2,3,4,2,300,'='],[3,1,1,5,300,'=']],True
#[[2000,500,0,'='],[2,3,36,'>='],[3,6,60,'>=']],False
#x.mainDosFases([[0.4,0.5,0,'='],[0.3,0.1,2.7,'<='],[0.5,0.5,6,'='],[0.6,0.4,6,'>=']],False,"")

