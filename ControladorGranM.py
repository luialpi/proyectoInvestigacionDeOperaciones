from GranM import*
tabla=[[]]
variablesDecision=0
arregloCol=[]#ubicar en tabla u
arregloFilas=["Z"]
arregloZ=[]
#-----------------------------------------------------------
class Z_Aux:
    #Constructor
    '''
    Clase en la cual se cuenta con un constructor encargado de 
    crear un objeto el cual tiene como atributo numero M
    numero sin m y letra la cual hace referencia a la columna en 
    que se ubique, en caso de no tener numero en M el numero que 
    se le asigne sera un 0
    '''
    def __init__(self,numeroM,numeroSinM,letra):
        self.numeroM= numeroM
        self.numeroSinM=numeroSinM
        self.letra=letra 
#-----------------------------------------------------------
#crear Z
class Z:
    #Constructor
    '''
    Clase la cual recibe como parametro si se trata de minimizar o 
    maximizar, ademas de una lista de lista en la cual se encuentran
    las restricciones en formato de [[3,2,1,"<="]] en donde los numeros
    corresponden a float o int y el simbolo es un string

    '''
    def __init__(self,arreglo,esMin,u):
        self.esMin= esMin
        self.restricciones=arreglo
        self.u= u


    '''
    Funcion en la cual se crean los objetos
    correspondientes a las variables basicas
    con sus respectivos atributos del numero M
    numero sin m y letra ya sea x1 x2 etc
    Ademas se agrega la solucion identificada mediante
    SOL
    '''    
    def crearZ(self):
        global tabla
        self.convertirNulo_ObjetosU()
        for i in range(len(self.u)):
            global arregloZ
            z=Z_Aux(0,self.u[i],"x"+str(i+1))
            arregloZ.append(z)
        sol=Z_Aux(0,0,"SOL")
        arregloZ.append(sol)


    ''' 
    Funcion en la cual se verifica si la variable
    se encuentra en el arreglo  para ello se utiliza 
    la letra que lo ubica en la columna

    '''
    def buscarArreglo(self,identificador):
        global arregloZ
        for x in range(len(arregloZ)):
            if arregloZ[x].letra == identificador:
                return x
        return -1

     
    ''' 
    Funcion para imprimimir los valores ya como objetos
    esto solamente es para la fila 0 es decir la fila z
    '''   
    
    #def imprimeArregloZ(self):
        #global arregloZ
        #for x in range(len(arregloZ)):
            #print("M:"+str(arregloZ[x].numeroM) +"\t Sin M:"+str(arregloZ[x].numeroSinM)+ "\t Letra:"+arregloZ[x].letra) 
    '''
    Funcion que verifica si se trata de minimizar o 
    maximizar , en caso de que sea minimizar cambiara de
    signo al numero debido al despeje que se debe hacer
    al colocar Z
    '''
    
    def verificarMinX(self,numero):
        if self.esMin is True:
            return numero*-1
        else: return numero
       
    '''
    Funcion la cual va agregando va recorriendo restriccion por restriccion
    para realizar la suma correspondiente de acuerdo al despeje
    de las variables artificiales con los valores de la funcion objetivo
    '''
    def agregarRestricciones(self):
        global arregloZ
        for i in range (len(self.restricciones)):
     
             if self.restricciones[i][len(self.restricciones[i])-1]!= "<=":
                 for j in range(len(self.restricciones[i])-2): ## por que los dos ultimos son solucion y simbolo
                     if self.buscarArreglo("x"+str(j+1)) != -1: # si lo encontro devuelve la pos donde esta si no -1
                         numero = self.verificarMinX(self.restricciones[i][j])# si es minimizar lo deja igual
                         arregloZ[self.buscarArreglo("x"+str(j+1))].numeroM+=numero

                 numero = self.verificarMinX(self.restricciones[i][len(self.restricciones[i])-2])# si es minimizar lo multiplica*-1
                 x=self.buscarArreglo("SOL")
                 arregloZ[x].numeroM+=numero
                 
        self.cambiarSignos()
        #self.imprimeArregloZ() # verifica si esta imprimiendo bien M


    '''
    Funcioon en la cual lo que se hace es cambiar
    el signo del numero M y numero que no tiene M
    en la fila Z
    '''
    def cambiarSignos(self):
        global arregloZ,tabla
        for x in range(len(arregloZ)):
            arregloZ[x].numeroM=arregloZ[x].numeroM*-1
            arregloZ[x].numeroSinM=arregloZ[x].numeroSinM*-1
            tabla[0][self.ubicar_En_Tabla(arregloZ[x])]=arregloZ[x]    

    '''
    Funcion la cual se utiliza para ubicar en la tabla
    el elemento de la fila U
    '''
    def ubicar_En_Tabla(self,elemento):
        global arregloCol
        for x in range(len(arregloCol)):
            if elemento.letra == arregloCol[x]:
                return x
        return -1         

    ''' 
    Funcion que se utliza para 
    la creacion de objetos pertenecientes a las 
    variables de holgura en donde el valor del numero M
    y numero sin M corresponde a 0 0
    '''
    def convertirNulo_ObjetosU(self):
        for x in range(len(arregloCol)):
            z=Z_Aux(0,0,arregloCol[x])
            tabla[0][x]=z
       

#-------------------------------------------------------
#Matriz      
class Matriz:
    #Constructor
    def __init__(self, arreglo):
        self.matriz = arreglo
       
   
    def set_Matriz(self, valor):  #set matriz  
        #print("Matriz cambiada")
        self.matriz = valor

    def get_Matriz(self): #get de la matriz 
        return self.matriz

    '''
    Funcion en la cual se crea la matriz a utilizar
    contando las variables artificiales, holgura y basicas
    en caso de tenerlas
    Ademas se agregan dos columnas extra para colocar
    la solucion y el resultado de la division para
    la seleccion del fila pivot

    '''
    def cantidad_filas(self):
        if(len(self.matriz) is not 0):
           global variablesDecision, tabla
           filas=variablesDecision+2 # col solucion y col division
           for i in range (len(self.matriz)):
               indica = self.matriz[i][len(self.matriz[i])-1]
               filas+=self.cantidad_filasAux(indica)
        tabla=[[0 for i in range(filas)] for i in range(len(self.matriz)+1)]

    def cantidad_filasAux(self,argument): # verifica si va necesitar el espacio para R y -S
        switcher = {">=": 2}
        return switcher.get(argument, 1)

    def variablesX(self):
        global variablesDecision
        for i in range (0,variablesDecision):
            arregloCol.append("x"+str(i+1))
        


#-----------------------------------------------------------
#Restricciones

class Restricciones:
    #Constructor
    def __init__(self, arreglo,esMin):
        self.matriz = arreglo
        self.varR=1
        self.varS=1
        self.esMin=esMin
    '''
    Funcion en la cual se colococan dentro de la tabla general a utilizar
    un 1 0 -1 a las variables correspondientes a las artificiales
    '''   
    def colocar_Restricciones(self):
        global variablesDecision
        posicion = variablesDecision-1  # aumenta en R y S
        
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])-2):
                tabla[i+1][j]=self.matriz[i][j]
            m = Matriz(self.matriz)
            self.verificar_Signo(self.matriz[i][len(self.matriz[i])-1])
            x= m.cantidad_filasAux(self.matriz[i][len(self.matriz[i])-1])
            posicion += x
            tabla[i+1][len(tabla[i])-2]=self.matriz[i][len(self.matriz[i])-2]
            if x is 2:
                tabla[i+1][posicion-1]=1
                tabla[i+1][posicion]=-1
            else: tabla[i+1][posicion]=1
        '''
        como se menciono anteriormente
        se agregan dos columnas extras
        que corresponden a la solucin y a una
        para la division
        '''    
        arregloCol.append("SOL")
        arregloCol.append("DIV")
    '''
    Funcion en la cual se agrega al arreglo que muestra las filas
    y las columnas una R representando variable artificial
    y una S en caso de ser una variable de holgura
    Se le adiciona el nuemero para poder diferenciarlas
    '''   
    def MayorIgual(self):
        arregloCol.append("R"+str(self.varR))
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("R"+str(self.varR))
        z=Z_Aux(self.verificar_Min(self.esMin),0,"S"+str(self.varS))
        global arregloZ
        arregloZ.append(z)
        self.varR+=1
        self.varS+=1
        
    def verificar_Min(self,argument):#verifica que se trate de minimizar o maximizar 
        switcher = {True: 1}
        return switcher.get(argument, -1)
            
    '''
    Funcion la cual agrega una S asemejando a una variable
    holgura tanto al arreglo de filas como el arreglo 
    de columnas , es cuando se recibe un signo <=
    '''
    def MenorIgual(self):
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("S"+str(self.varS))
        self.varS+=1

    '''
    Funcion en la que se agrega una R asimilando 
    una variable artificial, se agrega cuando 
    en la restriccion el signo es un =, se anade 
    al arreglo de filas y columnas
    '''
    def Igual(self):
        arregloCol.append("R"+str(self.varR))
        arregloFilas.append("R"+str(self.varR))
        self.varR+=1    
 
    def verificar_Signo(self,signo): # verifica cual signo corresponde a la restriccion
        switcher = {">=": self.MayorIgual,"<=": self.MenorIgual, "=": self.Igual }
        switcher [signo]()
        

#------------------------------------------------------------          
class Controlador:
    '''
    Metodo main en donde se llaman a las funciones para
    la implementacion metodo M """
      
    '''
    def __init__(self,minimo,U,restricciones,vars,file):
        global variablesDecision

        self.archivo=file
           
        variablesDecision=vars
        self.esMinimizar= minimo# se recibe
        self.arregloZ=U
        self.arregloEntrada=restricciones # lo que entra OJO CAMBIAR***************$$$$$
        #------------**------------------------**------------------
    '''
    Funcion en la cual se controla la creacion del areglo con objetos
    pertenecientes a la fila U, ademas se crea la tabla en la cual 
    de forma estandarizada
    '''
    def inicioControlador(self):    
        #print("-> Representacion de la impresion: \n ---------------------- \n |* R = Var Artificial   | \n |* S = Var Holgura      | \n |* X = Var Decision     | \n ----------------------\n\n")
        self.archivo.write("-> Representacion de la impresion: \n ---------------------- \n |* R = Var Artificial   | \n |* S = Var Holgura      | \n |* X = Var Decision     | \n ----------------------\n\n")


        matriz = Matriz(self.arregloEntrada) # crea objeto para la impresion
        #matriz.imprime_Matriz(matriz.get_Matriz())
        matriz.cantidad_filas() # crea la tabla
        matriz.variablesX()
        restricciones=Restricciones(self.arregloEntrada,self.esMinimizar)
        restricciones.colocar_Restricciones()
        #
        z=Z(self.arregloEntrada,self.esMinimizar,self.arregloZ)
        z.crearZ()
        z.agregarRestricciones()
      #-----
        global arregloFilas,arregloCol,tabla
        gM=GranM(tabla,arregloFilas,arregloCol,self.esMinimizar,self.archivo)
        gM.start_MetodoM_Max()
        
  
    #tabla de forma estandar OK
   
    #print(arregloEntrada)
#-------------------------------------------------------------
#-------------------------------------------------------------

