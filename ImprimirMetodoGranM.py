class ImprimirMetodoGranM:
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
        ImprimirMetodoGranM_Aux = ImprimirMetodoGranM()
        if(len(tabla) is not 0): #Si la tabla no esta vacia
            ImprimirMetodoGranM_Aux.imprime_Columnas(nombresColumnas, archivo)
            ImprimirMetodoGranM_Aux.imprimeFilaU(tabla, nombresFilas, archivo)
            for filaTabla in tabla[1:len(tabla)]: #Lineas que no tienen funcion objetivo
                lineaInferior = "*********"
                filaFinal = "|" + nombresFilas[tabla.index(filaTabla)] + "\t|" #Agrega el nombre de la fila a la fila a imprimir
                for columnaTabla in filaTabla:
                    lineaInferior = lineaInferior + "****************"
                    valor = round(columnaTabla, 2) #Redondea el valor a dos digitos
                    filaFinal = filaFinal + str(valor) + "\t\t|"
                archivo.write(filaFinal + "\n" + lineaInferior + "\n")



class Solucion:
    '''Impresion del resultado final'''
    
    def __init__(self,acotada):
        
        self.lista=[]
        self.lista2=[]
        self.bandera = False
        self.acotada = acotada
        self.variablesNegativas = False
        
    '''
    Funcion utilizada para verificar cuales variables
    son las basicas para luego mostrar la solucion
    de la forma U (x1 =0,...)
    '''
    def mostrarSolucion(self,tabla,arregloFilas,arregloCol,archivo,restricciones):
        self.lista.append("U")
        self.agregarM(tabla)
        for i in range(1, len(arregloFilas)):
            self.lista.append(arregloFilas[i])
            
            self.lista2.append(tabla[i][len(tabla[i])-2])
        
        self.colocar_Variables(arregloCol)
        self.imprimirVariables(archivo,restricciones)
        
    def colocar_Variables(self,arregloCol): 
        for i in range(0,len(arregloCol)-2):
            
            if arregloCol[i] in self.lista:
                continue
            else:
                self.lista.append(arregloCol[i])
                self.lista2.append(0)


    def agregarM(self,tabla): 
        if round(tabla[0][len(tabla[0])-2].numeroM,2) ==0:
            self.lista2.append(str(round(tabla[0][len(tabla[0])-2].numeroSinM,2)))
        else:self.lista2.append(str(round(tabla[0][len(tabla[0])-2].numeroM,2)) +"M + "+str(round(tabla[0][len(tabla[0])-2].numeroSinM,2)))

    '''
    Funcion encargada de mostrar la respuesta final de
    la forma U = 332(x1:0,..)

    '''            
    def imprimirVariables(self,archivo,restricciones):
        Solucion_Aux = Solucion(self.acotada)
        archivo.write("\n\n-----------------------------------------------------------------\n ")
        aux="-> U= "+ str(self.lista2[0])+"("+ str(self.lista[1]) +": "+ str(round(self.lista2[1],2))
        for i in range(2,len(self.lista)):
            aux+=","+str(self.lista[i]) +": "+ str(round(self.lista2[i],2))
        print("\n\n-----------------Metodo de la Gran M--------------------------\n  ")
        print(aux+" )")
        print("\n-----------------------------------------------------------------\n  ")
        archivo.write(aux+" )\n")
        Solucion_Aux.verificarVariablesBasicasMenor0(self.lista,self.lista2,archivo)
        Solucion_Aux.validarSolucionFactible(archivo,self.lista2,self.lista,restricciones)

    def validarSolucionFactible(self,archivo,lista2,lista,restricciones):
        Solucion_Aux = Solucion(self.acotada)
        resultado = 0
        cantidad_Restricciones = len(restricciones.matriz)
        for i in range(0,len(restricciones.matriz)):
            for j in range(0,len(restricciones.matriz[i])-2):
               indice = Solucion_Aux.encontrarCampoLista(lista,"x"+ str(j+1))
               resultado += restricciones.matriz[i][j]*lista2[indice]

            if (restricciones.matriz[i][len(restricciones.matriz[i])-1])== "=":
                if (resultado != (restricciones.matriz[i][len(restricciones.matriz[i])-2])):
                    print("La solucion al problema no es factible ya que incumple con la restriccion:"+str(i+1))
                    self.bandera = True
                    archivo.write("\n\nLa solucion al problema no es factible ya que incumple con la restriccion:"+str(i+1)+"\n")
                    
            if (restricciones.matriz[i][len(restricciones.matriz[i])-1])== "<=":
                if (resultado > (restricciones.matriz[i][len(restricciones.matriz[i])-2])):
                    print("La solucion al problema no es factible ya que incumple con la restriccion:"+str(i+1))
                    self.bandera = True
                    archivo.write("\n\nLa solucion al problema no es factible ya que incumple con la restriccion:"+str(i+1)+"\n")

            if ((restricciones.matriz[i][len(restricciones.matriz[i])-1])== ">="):
               if (resultado < (restricciones.matriz[i][len(restricciones.matriz[i])-2])):
                    print("La solucion al problema no es factible ya que incumple con la restriccion: "+str(i+1))
                    self.bandera = True
                    archivo.write("\n\nLa solucion al problema no es factible ya que incumple con la restriccion:"+str(i+1)+"\n")
                    
            resultado = 0
        
        if ((self.bandera) == False) and (self.acotada == False) and (self.variablesNegativas == False):
            print("La solucion al problema es factible ya que cumple con las restricciones iniciales")
            archivo.write("\n\nLa solucion al problema es factible ya que cumple con las restricciones iniciales\n")

        
    def encontrarCampoLista(self,lista,signo):
        for i in range(0,len(lista)):
            if (lista[i]) == signo:
                return i
            
    def verificarVariablesBasicasMenor0(self,lista,lista2,archivo):
        contadorBasico = 1
        variablesBasicas = []
        for i in range(0,len(lista)):
            signo = "x"+str(contadorBasico)
            if (lista[i] == signo):
                contadorBasico += 1
                variablesBasicas.append(i)
                
        for i in range(0,len(variablesBasicas)):
            if (lista2[variablesBasicas[i]] < 0):
                print("La solucion al problema no es factible ya que alguna variable basica es negativa")
                archivo.write("La solucion al problema no es factible ya que alguna variable basica es negativa")
                self.variablesNegativas = True
   
class Multiples_Solucion:
    '''
    Clase en la cual se verifica si el resultado final cuenta con 
    una solucion extra o no 
    '''
    
    def __init__(self):
        self.listaPosiciones=[]
        
    def localizar_Variable_Basica(self, tabla,arregloFilas,arregloCol):
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

              
class Archivo:
    '''Encagada de crear archivo donde se 
    almacenara las iteraciones'''
    
    def __init__(self,nombre):
        nombreArchivoSalida = nombre.replace(".txt", "") + "_sol.txt"
        self.archivo = open(nombreArchivoSalida,"w+")

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

