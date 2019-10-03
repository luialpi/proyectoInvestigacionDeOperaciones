import argparse
import sys
from VerificarArchivoEntrada import *
from Imprimir import *
from metodoSimplex import *
from DosFases import *
from metodoDual import*
from ControladorMetodoGranM import *

def main():
    #Aqui leemos los argumentos de entrada de la funcion.
    for indice in range (1, len(sys.argv)):
        if sys.argv[indice] in ["-h", "[-h]"]:
            print("Menu de ayuda, Programa Metodo Simplex \n")
            print("Este programa fue construido en Python, por lo que debe instalarlo en su computadora \n")
            print("para hacerlo funcionar.\n\n")
            print("Instrucciones de instalacion: https://tutorial.djangogirls.org/es/python_installation/ \n\n")
            print("Para correr el programa, ingrese este comando: \n")
            print("python simplex.py [-h] [archivo1.txt archivo2.txt archivo3.txt...] \n")
            print("Los que tienen nombre archivoX.txt son los archivos de configuracion de entrada.\n")
            print("Puede agregar todos los que requiera.\n\n")
            print("El formato de cada archivo de entrada debe ser asi, cada valor separado por comas sin espacios:\n")
            print("metodo,tipoOptimizacion,cantidadVariablesDecision,cantidadRestricciones\n")
            print("coeficientesFuncionObjetivo\n")
            print("coeficientesRestricciones\n\n")
            print("Ejemplo:\n")
            print("1,min,2,3\n")
            print("3,5\n")
            print("2,1,<=,6\n")
            print("-1,3,=,9\n")
            print("0,1,>=,4\n")
        else:
            #Se lee el archivo de entrada, y se verifica para que venga con buen formato.
            #Genera un booleano si el archivo esta bien o no.
            esArchivoConError = VerificarArchivoEntrada.leerArchivo(sys.argv[indice])
            
            #Si el archivo no tiene error, entonces se trabaja sobre el mismo.
            #Si el archivo tiene error, no se hace nada, y se pasa al siguiente archivo.
            #Esto para que no se caiga el programa. 
            if esArchivoConError == False:
                #configuracion es una lista con configuraciones, generada a partir del metodo de entrada. 
                configuracion = VerificarArchivoEntrada.getListaConfiguraciones()

                #Se genera el archivo de salida con el nombre que se pide en la especificacion.
                archivo = ArchivoSalida.crearArchivoSalida(sys.argv[indice])

                #Se corre el tipo de metodo dependiendo de la entrada.
                if configuracion[0] == 0:
                    simplex = MetodoSimplex()
                    simplex.inicializarSimplex(True, configuracion[1][0], configuracion[1][1], archivo)
                    solucionSimplex = simplex.mainSimplex()

                    #Imprimir.imprimirMatrizSimplex(archivo, solucionSimplex[2], solucionSimplex[1], solucionSimplex[0])

                elif configuracion[0] == 1:
                    arregloU = configuracion[1][2]
                    funcionObjetivo = []
                    for i in range(0,len(arregloU)-2):
                        funcionObjetivo.append(arregloU[i])
                  
                    granM = Controlador(configuracion[1][3],funcionObjetivo,configuracion[1][1],int(configuracion[1][0]),archivo)
                    granM.inicioControlador()
                    
                elif configuracion[0] == 2:
                    dosFases = metodoDosFases()
                    solucionDosFases = dosFases.mainDosFases(configuracion[1][0],configuracion[1][1],archivo)

                elif configuracion[0] == 3:
                    metodoDualSalida = MetodoDual()
                    metodoDualSalida.mainDual(configuracion[1][0], configuracion[1][1], archivo)

main()

