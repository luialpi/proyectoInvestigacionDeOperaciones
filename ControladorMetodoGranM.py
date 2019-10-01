from MetodoGranM import*
from ImprimirMetodoGranM import*

tabla=[[]]
variablesDecision=0
arregloColumnas=[]
arregloFilas=["Z"]
arregloZ=[]

class ArregloZ_Aumentado_Aux:
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

class ArregloZ_Aumentado:
   
    '''
    Clase la cual recibe como parametro si se trata de minimizar o 
    maximizar, ademas de una lista de lista en la cual se encuentran
    las restricciones en formato de [[3,2,1,"<="]] en donde los numeros
    corresponden a float o int y el simbolo es un string

    '''
    def __init__(self,restricciones,esMin,u):
        self.esMin= esMin
        self.restricciones=restricciones
        self.u= u


    '''
    Funcion en la cual se crean los objetos
    correspondientes a las variables basicas
    con sus respectivos atributos del numero M
    numero sin m y letra ya sea x1 x2 etc
    Ademas se agrega la solucion identificada mediante
    SOL
    '''    
    def crearZ_Aumentada(self):
        global tabla
        self.convertirNulo_ObjetosU()
        for i in range(len(self.u)):
            global arregloZ
            z=ArregloZ_Aumentado_Aux(0,self.u[i],"x"+str(i+1))
            arregloZ.append(z)
        sol=ArregloZ_Aumentado_Aux(0,0,"SOL")
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
                 for j in range(len(self.restricciones[i])-2): 
                     if self.buscarArreglo("x"+str(j+1)) != -1:
                         numero = self.verificarMinX(self.restricciones[i][j])
                         arregloZ[self.buscarArreglo("x"+str(j+1))].numeroM+=numero

                 numero = self.verificarMinX(self.restricciones[i][len(self.restricciones[i])-2])
                 x=self.buscarArreglo("SOL")
                 arregloZ[x].numeroM+=numero
                 
        self.cambiarSignos()

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
        global arregloColumnas
        for x in range(len(arregloColumnas)):
            if elemento.letra == arregloColumnas[x]:
                return x
        return -1         

    ''' 
    Funcion que se utliza para 
    la creacion de objetos pertenecientes a las 
    variables de holgura en donde el valor del numero M
    y numero sin M corresponde a 0 0
    '''
    def convertirNulo_ObjetosU(self):
        for x in range(len(arregloColumnas)):
            z=ArregloZ_Aumentado_Aux(0,0,arregloColumnas[x])
            tabla[0][x]=z
       
    
class Matriz:
    def __init__(self, arreglo):
        self.matriz = arreglo
       
   
    def set_Matriz(self, valor): 
        print("Matriz cambiada")
        self.matriz = valor

    def get_Matriz(self): 
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
           filas=variablesDecision+2 
           for i in range (len(self.matriz)):
               indica = self.matriz[i][len(self.matriz[i])-1]
               filas+=self.cantidad_filasAux(indica)
        tabla=[[0 for i in range(filas)] for i in range(len(self.matriz)+1)]

    def cantidad_filasAux(self,argument): 
        switcher = {">=": 2}
        return switcher.get(argument, 1)

    def variablesX(self):
        global variablesDecision
        for i in range (0,variablesDecision):
            arregloColumnas.append("x"+str(i+1))
        
class Restricciones:
    def __init__(self,arreglo,esMin):
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
        posicion = variablesDecision-1 
        
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
        arregloColumnas.append("SOL")
        arregloColumnas.append("DIV")
    '''
    Funcion en la cual se agrega al arreglo que muestra las filas
    y las columnas una R representando variable artificial
    y una S en caso de ser una variable de holgura
    Se le adiciona el nuemero para poder diferenciarlas
    '''   
    def MayorIgual(self):
        arregloColumnas.append("R"+str(self.varR))
        arregloColumnas.append("S"+str(self.varS))
        arregloFilas.append("R"+str(self.varR))
        z=ArregloZ_Aumentado_Aux(self.verificar_Min(self.esMin),0,"S"+str(self.varS))
        global arregloZ
        arregloZ.append(z)
        self.varR+=1
        self.varS+=1
        
    def verificar_Min(self,argument):
        switcher = {True: 1}
        return switcher.get(argument, -1)
            
    '''
    Funcion la cual agrega una S asemejando a una variable
    holgura tanto al arreglo de filas como el arreglo 
    de columnas , es cuando se recibe un signo <=
    '''
    def MenorIgual(self):
        arregloColumnas.append("S"+str(self.varS))
        arregloFilas.append("S"+str(self.varS))
        self.varS+=1

    '''
    Funcion en la que se agrega una R asimilando 
    una variable artificial, se agrega cuando 
    en la restriccion el signo es un =, se anade 
    al arreglo de filas y columnas
    '''
    def Igual(self):
        arregloColumnas.append("R"+str(self.varR))
        arregloFilas.append("R"+str(self.varR))
        self.varR+=1    
 
    def verificar_Signo(self,signo): 
        switcher = {">=": self.MayorIgual,"<=": self.MenorIgual, "=": self.Igual }
        switcher [signo]()
        
         
class Controlador:
    '''
    Metodo main en donde se llaman a las funciones para
    la implementacion metodo M """
      
    '''
    def __init__(self,minimo,U,restricciones,vars,archivo):
        global variablesDecision

        self.archivo=archivo           
        variablesDecision=vars
        self.esMinimizar= minimo
        self.arregloZ=U
        self.arregloEntrada=restricciones
        
    '''
    Funcion en la cual se controla la creacion del areglo con objetos
    pertenecientes a la fila U, ademas se crea la tabla en la cual 
    de forma estandarizada
    '''
    def inicioControlador(self):
        
        matriz = Matriz(self.arregloEntrada)
        matriz.cantidad_filas()
        matriz.variablesX()
        
        restricciones=Restricciones(self.arregloEntrada,self.esMinimizar)
        restricciones.colocar_Restricciones()
        
        z=ArregloZ_Aumentado(self.arregloEntrada,self.esMinimizar,self.arregloZ)
        z.crearZ_Aumentada()
        z.agregarRestricciones()
  
        global arregloFilas,arregloColumnas,tabla
        granM=GranM(tabla,arregloFilas,arregloColumnas,self.esMinimizar,self.archivo,restricciones)
        granM.Inicio_Metodo_GranM()
