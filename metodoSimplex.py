class SimplexMethod:

    def __init__(self):
        self.columnaPivot = -1
        self.filaPivot = -1

    '''
    funcion principal del metodo simplex
    '''
    def simplex(self, matriz, esMaximo):
        self.matrizTabla = matriz
        self.esMaximo = esMaximo
        self.cantidadDeFilas = len(self.matrizTabla)
        self.cantidadDeColumnas = len(self.matrizTabla[0])
        while(self.optimo()):
            self.columnaPivot = self.encontrarColumnaPivot()
            self.filaPivot = self.encontrarFilaPivot()
            self.modificarFilaPivot()
            self.modificarFilas()

    '''
    Funcion encargada de encontrar el mas negativo
    para asi saber cual es la columna pivot
    '''
    def encontrarColumnaPivot(self):
        if self.esMaximo:
            return self.encontrarColumnaPivotMax()
        else:
            return self.encontrarColumnaPivotMin()
        
    '''
    Funcion encargada de encontrar el mas negativo
    para asi saber cual es la columna pivot
    '''
    def encontrarColumnaPivotMax(self):
        
        pivot=self.matrizTabla[0][0]
        columna_pivot_indice=0
        for x in range(self.cantidadDeColumnas-2):
            if pivot>(self.matrizTabla[0][x]) :
                pivot = (self.matrizTabla[0][x])
                columna_pivot_indice=x
        return columna_pivot_indice

    '''
    Funcion encargada de encontrar el mas positivo
    para asi saber cual es la columna pivot
    '''
    def encontrarColumnaPivotMin(self):
        pivot=(self.matrizTabla[0][0])
        columna_pivot_indice=0
        for x in range(self.cantidadDeColumnas-2):
            if pivot<(self.matrizTabla[0][x]) :
                pivot = (self.matrizTabla[0][x])
                columna_pivot_indice=x
        return columna_pivot_indice

    '''
    Funcion encargada de encontrar cual es el menor positivo
    y asi poder encontrar el numero pivot en la iteraccion
    '''
    def encontrarFilaPivot(self):
        pivot = 1
        pivotAuxiliar = 0
        indiceDeControl = 0
        for x in range(1,self.cantidadDeFilas):
            if self.matrizTabla[x][self.columnaPivot] > 0:
                division = self.matrizTabla[x][self.cantidadDeColumnas-1] / self.matrizTabla[x][self.columnaPivot]
                indiceDeControl=indiceDeControl+1
                if( indiceDeControl == 1):
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
    def optimalidadDeResultado(self):
        n=0
        fila=-1
        for x in range(1,self.cantidadDeFilas):
            if self.matrizTabla[x][lenMatrizTabla-1] < 0:
                return False
        return True

    '''
    Funcion que verifica si ya se obtuvo el valor obtimo
    '''
    def optimo(self):
        if self.esMaximo:
            return self.optimoMax()
        else:
            return self.optimoMin()

    '''
    Funcion que verifica si ya se obtuvo el valor optimo en el caso de maximizacion
    para ello verifica que aun existan numeros positivos y retorna true en caso de que aun exista una columna con u positivo
    '''
    def optimoMax(self):
        count = 0
        for x in range(0,self.cantidadDeColumnas-1):
            valor = self.matrizTabla[0][x]
            if(valor < float(0)):
                count+=1
        if count > 0:
            return True
        else:
            return False
                
    
    '''
    Funcion que verifica si ya se obtuvo el valor optimo en el caso de minimizacion
    para ello verifica que aun existan numeros negaticos y retorna true en caso de que aun exista una columna con u negativo
    '''    
    def optimoMin(self):
        count = 0
        for x in range(0,self.cantidadDeColumnas-1):
            valor = self.matrizTabla[0][x]
            if(valor > float(0)):
                    count+=1
        if count > 0:
            return True
        else:
            return False
    '''
    Funcion que modifica la fila pivot para poner el numero pivot en 1
    '''
    def modificarFilaPivot(self):
        numeroPivot =  self.matrizTabla[self.filaPivot][self.columnaPivot]
        for i in range(0, self.cantidadDeColumnas):
            self.matrizTabla[self.filaPivot][i] = self.matrizTabla[self.filaPivot][i] / numeroPivot

    '''
    Funcion que efectua operaciones en las filas de manera que se logre obtener un 0 en la columna pivot
    '''
    def modificarFilas(self):
        for i in range(0,self.cantidadDeFilas):
            variableParaDivision = self.matrizTabla[i][self.columnaPivot]
            if( i != self.filaPivot ):
                for j in range(0,self.cantidadDeColumnas):
                    self.matrizTabla[i][j] = self.matrizTabla[i][j] - ( self.matrizTabla[self.filaPivot][j] * variableParaDivision)

