class ArchivoSalida:

    def __init__(self):
        pass

    def crearArchivoSalida(nombreArchivoEntrada):
        nombreArchivoSalida = nombreArchivoEntrada.replace(".txt", "") + "_sol.txt"
        print(nombreArchivoSalida)
        archivo = open (nombreArchivoSalida, "w+")
        return archivo

    def cerrarArchivoSalida(archivo):
        archivo.close()

class Imprimir:

    global esDegenerada #Variable tipo booleana que determina si la solucion es degenerada
    global nombresColumnas #Variable tipo lista de strings que va a contener los nombres de las columnas
    #Ejemplo: ['x1', 'x2', 'x3', 'x4', 'Sol', 'DIV']
    global nombresFilas #Variable tipo lista de strings que va a contener los nombres de las filas
    #Ejemplo: ['U', 'x2', 'x4']
    global tabla #Variable de tipo lista de listas de Float, que contiene la tabla de cada iteracion.
    #Ejemplo: [[c0, c1, c2, c3, c4, c5], [0.25, 1.0, 0.25, 0.0, 2.0, 2.0], [0.5, 0.0, -0.5, 1.0, 0.0, 2.0]]
    #Siendo ci clases de tipo Z_Aux, que contienen numeroM, numeroSinM, columna a la que pertenece.
    
    #Constructor
    def __init__(self):
        pass
    
    #Funcion imprimirColumnas. Esta se va a usar dentro de la funcion imprimirMatriz para imprimir los nombres de las columnas 
    #en el archivo para cada iteracion. 
    #Entradas:
    #   nombresColumnas: Variable global tipo lista de strings que va a contener los nombres de las columnas
    #Salidas:
    #   Imprime en el archivo los nombres de las columnas para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimirNombreColumnasGranM(archivo, nombresColumnas):
        lineaColumnas = "|\t|"
        lineaInferior = "********"
        lineaSuperior = "\n\n\n********"
        for indice in nombresColumnas:
            lineaSuperior = lineaSuperior + "*************"
            lineaColumnas = lineaColumnas + indice + "\t     |"
            lineaInferior = lineaInferior + "*************"
        lineaInferior = lineaInferior + "****************"
        lineaSuperior = lineaSuperior + "****************"
        print(lineaSuperior + "\n" + lineaColumnas + "\n" + lineaInferior)
        archivo.write("\n" + lineaSuperior + "\n" + lineaColumnas + "\n" + lineaInferior + "\n")


    #Funcion imprimirFuncionObjetivo. Esta funcion se encarga de imprimir la funcion objetivo en el archivo para cada iteracion.
    #Entradas:
    #   nombresFilas: Variable global tipo lista de strings que contiene los nombres de las filas.
    #   tabla: Variable de tipo lista de listas de Float, que contiene la tabla de cada iteracion.
    #Salidas:
    #   Imprime en el archivo la funcion objetivo para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimirFuncionObjetivoGranM(archivo, nombresFilas, tabla):
        lineaInferior = "********"
        lineaFuncionObjetivo = "|" + nombresFilas[0] + "\t|" #Imprime la letra U
        for valor in tabla[0]:
            lineaInferior = lineaInferior + "*************"
            valorM = round(valor.numeroM, 2) #Redondea a dos digitos el valor del numero que se suma / resta con M
            valorSinM = round(valor.numeroSinM, 2) #Redondea a dos digitos el valor del numero que esta multiplicado con M
            if valor.numeroM == 0: #Si la M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "\t     |" #Se imprime solo el valor sin M
            elif valor.numeroM != 0 and valor.numeroSinM == 0: #Si la M no es cero, pero el valor sin M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorM) + "M\t     |" #Se imprime el valor M
            else: #Si ambos tienen valores
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "+" + str(valorM) + "M\t     |" #Se imprimen ambos
        lineaInferior = lineaInferior + "****************"
        print(lineaFuncionObjetivo + "\n" + lineaInferior)
        archivo.write(lineaFuncionObjetivo + "\n" + lineaInferior + "\n")


    #Funcion imprimirMatriz. Esta funcion se encarga de imprimir la funcion objetivo en el archivo para cada iteracion.
    #Entradas:
    #   nombresFilas: Variable global tipo lista de strings que contiene los nombres de las filas.
    #   tabla: Variable de tipo lista de listas de Float, que contiene la tabla de cada iteracion.
    #Salidas:
    #   Imprime en el archivo la funcion objetivo para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimirMatrizGranM(archivo, nombresFilas, nombresColumnas, tabla):
        if(len(tabla) is not 0): #Si la tabla no esta vacia
            Imprimir.imprimirNombreColumnasGranM(archivo, nombresColumnas)
            Imprimir.imprimirFuncionObjetivoGranM(archivo, nombresFilas, tabla)
            for filaTabla in tabla[1:len(tabla)]: #Lineas que no tienen funcion objetivo
                lineaInferior = "********"
                filaFinal = "|" + nombresFilas[tabla.index(filaTabla)] + "\t|" #Agrega el nombre de la fila a la fila a imprimir
                for columnaTabla in filaTabla:
                    lineaInferior = lineaInferior + "*************"
                    valor = round(columnaTabla, 2) #Redondea el valor a dos digitos
                    filaFinal = filaFinal + str(valor) + "\t     |"
                lineaInferior = lineaInferior + "****************"
                archivo.write(filaFinal + "\n" + lineaInferior + "\n")
                print(filaFinal + "\n" + lineaInferior)
