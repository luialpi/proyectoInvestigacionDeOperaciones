#Impresion de la parte grafica
#-----------------------------------------------------------
#-----------------------------------------------------------

class Print:
    #Constructor
    def __init__(self):
        pass
        
    '''
    Funcion en la cual se imprimen el nombre
    correspondiente a cada una de las filas ya sea
    var de holgura artificial o basica
    '''
    def imprime_Columnas(self,arregloCol,archivo):
        
        aux="\t"
        aux2="\t"
        for i in arregloCol:
            aux+=i+"\t"
            aux2+="------"
        aux2+="------------"
        print (aux+"\n"+aux2)
        archivo.write(aux+"\n"+aux2+"\n")

    '''
    Como m corresponde a objetos se encarga de imprimir esta fila
    por aparte imprimiendo numero M y numero Sin M
    '''
    def imprimeFilaU(self,tabla,arregloFilas,archivo):

        aux=arregloFilas[0]+"\t"
        for x in range (len(tabla[0])):
            if tabla[0][x].numeroM == 0: aux+=str(tabla[0][x].numeroSinM)+"\t"
            elif tabla[0][x].numeroM != 0 and tabla[0][x].numeroSinM == 0:
                aux+=str(tabla[0][x].numeroM)+"M\t"
            else: aux+=str(tabla[0][x].numeroSinM)+"+"+str(tabla[0][x].numeroM)+"M\t"
        print (aux)
        archivo.write(aux+"\n")
    
    '''
    Funcion encargada de imprimir la primer matriz
    una vez se encuentre estandarizada
    '''
    def imprime_Matriz(self,tabla,arregloFilas,arregloCol,archivo):

       if(len(tabla) is not 0):
          aux=""
          self.imprime_Columnas(arregloCol,archivo)
          self.imprimeFilaU(tabla,arregloFilas,archivo)
          for i in range (1,len(tabla)):
              aux=arregloFilas[i]+"\t"
              for j in range (len(tabla[i])):
                  aux+=str(tabla[i][j])+"\t"
              archivo.write(aux+"\n")
              print(aux)

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
        self.archivo=open(nombre,"w+")
        print(nombre)

    def getArchivo(self):
        return self.archivo
#-----------------------------------------------------------
#-----------------------------------------------------------
              



