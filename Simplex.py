
import sys
from VerificarArchivoEntrada import *
from Imprimir import *
from metodoSimplex import *

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
            #print(sys.argv[indice])
            resultado = VerificarArchivoEntrada.leerArchivo(sys.argv[indice])
            if resultado == False:
                configuracion = VerificarArchivoEntrada.getListaConfiguraciones()
                #print(str(configuracion))

                archivo = ArchivoSalida.crearArchivoSalida(sys.argv[indice])
                #elegirMetodo = {0:}
                #elegirMetodo.get(configuracion[0])
                
                #Ejemplo diccionario
                #diccionario = {1:VerificarArchivoEntrada.getListaConfiguraciones()}
                #print(diccionario.get(configuracion[0]))

main()
