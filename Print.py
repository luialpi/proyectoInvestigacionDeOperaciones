 de la parte grafica
#-----------------------------------------------------------
#-----------------------------------------------------------

class Print:
    #Constructor
    def __init__(self):
        pass
        
    #Funcion imprime_Columnas. Esta se va a usar dentro de la funcion imprimirMatriz para imprimir los nombres de las columnas 
    #en el archivo para cada iteracion. 
    #Entradas:
    #   nombresColumnas: Variable global tipo lista de strings que va a contener los nombres de las columnas
    #Salidas:
    #   Imprime en el archivo los nombres de las columnas para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprime_Columnas(self, nombresColumnas, archivo):
        lineaColumnas = "|\t|"
        lineaInferior = "*********"
        lineaSuperior = "\n\n\n*********"
        for indice in nombresColumnas:
            lineaSuperior = lineaSuperior + "****************"
            lineaColumnas = lineaColumnas + indice + "\t\t|"
            lineaInferior = lineaInferior + "****************"
        archivo.write("\n" + lineaSuperior + "\n" + lineaColumnas + "\n" + lineaInferior + "\n")


    #Funcion imprimeFilaU. Esta funcion se encarga de imprimir la funcion objetivo en el archivo para cada iteracion.
    #Entradas:
    #   nombresFilas: Variable global tipo lista de strings que contiene los nombres de las filas.
    #   tabla: Variable de tipo lista de listas de Float, que contiene la tabla de cada iteracion.
    #Salidas:
    #   Imprime en el archivo la funcion objetivo para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimeFilaU(self, tabla, nombresFilas, archivo):
        lineaInferior = "*********"
        lineaFuncionObjetivo = "|" + nombresFilas[0] + "\t|" #Imprime la letra U
        for valor in tabla[0]:
            lineaInferior = lineaInferior + "****************"
            valorM = round(valor.numeroM, 2) #Redondea a dos digitos el valor del numero que se suma / resta con M
            valorSinM = round(valor.numeroSinM, 2) #Redondea a dos digitos el valor del numero que esta multiplicado con M
            if valor.numeroM == 0: #Si la M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "\t\t|" #Se imprime solo el valor sin M
            elif valor.numeroM != 0 and valor.numeroSinM == 0: #Si la M no es cero, pero el valor sin M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorM) + "M\t\t|" #Se imprime el valor M
            else: #Si ambos tienen valores
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "+" + str(valorM) + "M\t|" #Se imprimen ambos
        archivo.write(lineaFuncionObjetivo + "\n" + lineaInferior + "\n")
    
    #Funcion imprimirMatriz. Esta funcion se encarga de imprimir la funcion objetivo en el archivo para cada iteracion.
    #Entradas:
    #   nombresFilas: Variable global tipo lista de strings que contiene los nombres de las filas.
    #   tabla: Variable de tipo lista de listas de Float, que contiene la tabla de cada iteracion.
    #Salidas:
    #   Imprime en el archivo la funcion objetivo para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimirMatrizGranM(self, tabla, nombresFilas, nombresColumnas, archivo):
        if(len(tabla) is not 0): #Si la tabla no esta vacia
            Print.imprime_Columnas(nombresColumnas, archivo)
            Print.imprimeFilaU(tabla, nombresFilas, archivo)
            for filaTabla in tabla[1:len(tabla)]: #Lineas que no tienen funcion objetivo
                lineaInferior = "*********"
                filaFinal = "|" + nombresFilas[tabla.index(filaTabla)] + "\t|" #Agrega el nombre de la fila a la fila a imprimir
                for columnaTabla in filaTabla:
                    lineaInferior = lineaInferior + "****************"
                    valor = round(columnaTabla, 2) #Redondea el valor a dos digitos
                    filaFinal = filaFinal + str(valor) + "\t\t|"
                archivo.write(filaFinal + "\n" + lineaInferior + "\n")

#-----------------------------------------------------------
#-----------------------------------------------------------

class Solucion:
    '''Impresion del resultado final'''
    
    def __init__(self):
        
        self.lista=[]
        self.lista2=[]
        
    '''
    Funcion utilizada para verificar cuales variables
    son las basicas para luego mostrar la solucion
    de la forma U (x1 =0,...)
    '''
    def mostrarSolucion(self,tabla,arregloFilas,arregloCol,archivo):
        self.lista.append("U")
        self.agregarM(tabla)
        #self.lista2.append(str(round(tabla[0][len(tabla[0])-2].numeroM,2)) +"M + "+str(round(tabla[0][len(tabla[0])-2].numeroSinM,2)))
        for i in range(1, len(arregloFilas)):
            self.lista.append(arregloFilas[i])
            
            self.lista2.append(tabla[i][len(tabla[i])-2])
        
        self.colocar_Variables(arregloCol)
        self.imprimirVar(archivo)
        
    def colocar_Variables(self,arregloCol): # coloca las variables que no son las basicas en la lista para luego imprimirlas
        for i in range(0,len(arregloCol)-2):
            
            if arregloCol[i] in self.lista:
                continue
            else:
                self.lista.append(arregloCol[i])
                self.lista2.append(0)


    def agregarM(self,tabla): # agrega M debido a que es un objeto por lo tano se debe tratar como objeto.numero M y objeto.numeroSin M
        if round(tabla[0][len(tabla[0])-2].numeroM,2) ==0:
            self.lista2.append(str(round(tabla[0][len(tabla[0])-2].numeroSinM,2)))
        else:self.lista2.append(str(round(tabla[0][len(tabla[0])-2].numeroM,2)) +"M + "+str(round(tabla[0][len(tabla[0])-2].numeroSinM,2)))

    '''
    Funcion encargada de mostrar la respuesta final de
    la forma U = 332(x1:0,..)

    '''            
    def imprimirVar(self,archivo):
        print("\n\n-----------------------------------------------------------------\n  ")
        archivo.write("\n\n-----------------------------------------------------------------\n ")
        aux="->Respuesta Final: U= "+ str(self.lista2[0])+"("+ str(self.lista[1]) +": "+ str(round(self.lista2[1],2))
        for i in range(2,len(self.lista)):
            aux+=","+str(self.lista[i]) +": "+ str(round(self.lista2[i],2))
        print(aux+" )")
        archivo.write(aux+" )\n") # lo escribe al archivo 
            
                           
                
    #-----------------------------------------------------------
    #-----------------------------------------------------------

class Multiples_Solucion:
    '''
    Clase en la cual se verifica si el resultado final cuenta con 
    una solucion extra o no 
    '''
    
    def __init__(self):
        self.listaPosiciones=[]
        
    def localizar_VB(self, tabla,arregloFilas,arregloCol):
        for i in range(1,len(arregloFilas)):
            self.listaPosiciones.append(arregloCol.index(arregloFilas[i]))
        
        return self.verificar_Multiples_Soluciones(tabla)

    '''
    Funcion en la cual se verifica si en la fila U
    existe alguna variable no basica con valor de 0 
    ya que debido a esto se considera que tiene soluciones
    extra
    '''
        
    def verificar_Multiples_Soluciones(self,tabla):
        for i in range(len (tabla[0])-2):
            if not i in self.listaPosiciones:
                if tabla[0][i].numeroM == 0 and tabla[0][i].numeroSinM == 0:
                    return i
        return -1
#-----------------------------------------------------------
#-----------------------------------------------------------
              
class Archivo:
    '''Encagada de crear archivo donde se 
    almacenara las iteraciones'''
    
    def __init__(self,nombre):
        nombreArchivoSalida = nombre.replace(".txt", "") + "_sol.txt"
        archivo = open (nombreArchivoSalida, "w+")

    def getArchivo(self):
        return self.archivo

class ArchivoSalida:

    def __init__(self):
        pass

    def crearArchivoSalida(nombreArchivoEntrada):
        nombreArchivoSalida = nombreArchivoEntrada.replace(".txt", "") + "_sol.txt"
        archivo = open (nombreArchivoSalida, "w+")
        return archivo

    def cerrarArchivoSalida(archivo):
        archivo.close()
#-----------------------------------------------------------
#-----------------------------------------------------------

