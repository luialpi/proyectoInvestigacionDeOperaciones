class ManejoArchivos:

    global listaEntrada #Variable tipo Lista que se genera al leer el archivo
    global metodo #Variable tipo float. 0=Simplex, 1=GranM, 2=DosFases, 3=Dual
    global tipoOptimizacion #Variable tipo booleana. True=min, False=max
    global cantidadVariablesDecision #Variable tipo float. Cantidad de variables de decision
    global cantidadRestricciones #Variable tipo float. Cantidad de restricciones
    global coeficientesFuncionObjetivo #Variable tipo Lista de floats. Los coeficientes de las variables de la funcion objetivo
    #Ejemplo: [3.0, 5.0]
    global coeficientesRestricciones #Variable tipo Matriz de floats. Los coeficientes de las restricciones y su signo
    #Ejemplo: [[2.0, 1.0, '<=', 6.0], [-1.0, 3.0, '=', 9.0], [0.0, 1.0, '>=', 4.0]]


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

    #Funcion leerArchivo. Lee el archivo de configuracion para convertirlo en una lista.
    #Entradas:
    #   Archivo de configuracion.
    #Salidas:
    #   Lista con las configuraciones.
    #Restricciones:
    #   Que el archivo exista.
    def leerArchivo(nombreArchivoEntrada):
        global listaEntrada
        listaEntrada = []
        try:
            archivoInicial = open(nombreArchivoEntrada, "r")
        except(FileNotFoundError):
            print("Error. Archivo de entrada no presente")
            exit(0)
        listaArchivo = archivoInicial.readlines()
        archivoInicial.close()
        for indice in listaArchivo:
            entrada = indice.split(",")
            entrada[len(entrada)-1] = entrada[len(entrada)-1].strip('\n')
            listaEntrada.append(entrada)
        return listaEntrada

    #Funcion verificarArchivoConfiguracion. Esta funcion verifica que todos los datos introducidos
    #en el archivo de configuracion esten bien.
    #Entradas:
    #   La listaEntrada generada por leerArchivo.
    #Salidas:
    #   Ninguna.
    #Restricciones:
    #   Ninguna.
    def verificarArchivoConfiguracion():
        global listaEntrada
        ManejoArchivos.verificarTipoMetodo(listaEntrada[0][0])
        ManejoArchivos.verificarTipoOptimizacion(listaEntrada[0][1])
        ManejoArchivos.verificarCantidadArgumentos(listaEntrada[0])
        ManejoArchivos.verificarCoeficientesFuncionObjetivo(listaEntrada[1])
        ManejoArchivos.verificarRestricciones(listaEntrada)

    #Funcion verificarTipoMetodo. Verifica que el metodo introducido sea correcto y este dentro de la lista
    #de valores correctos.
    #Entradas:
    #   El tipo de metodo. Si fuera correcto, seria 0=Simplex, 1=GranM, 2=DosFases, 3=Dual
    #Salidas:
    #   Si el tipo de metodo esta dentro del rango correcto, se agrega a la variable global metodo.
    #   Si no lo es, se despliega un mensaje de error en consola.
    #Restricciones:
    #   Que el tipo de metodo sea alguno de estos: 0=Simplex, 1=GranM, 2=DosFases, 3=Dual
    def verificarTipoMetodo(tipoMetodo):
        global metodo
        metodo = ""
        if tipoMetodo in ["0", "1", "2", "3"]:
            metodo = int(tipoMetodo)
        else:
            print("Error. El tipo de metodo ingresado es incorrecto.")
            print("Favor ingresar 0=Simplex, 1=GranM, 2=DosFases, 3=Dual")
            exit(0)

    #Funcion verificarTipoOptimizacion. Verifica que el tipo de optimizacion sea correcta (min o max).
    #Entradas:
    #   El tipo de optimizacion (min o max).
    #Salidas:
    #   Si el tipo de optimizacion es correcto, se agrega a la variable global tipoOptimizacion True para min y False para max.
    #   Si no lo es, se despliega un mensaje de error en consola.
    #Restricciones:
    #   Que el tipo de metodo sea alguno de estos: min o max.
    def verificarTipoOptimizacion(optimizacion):
        global tipoOptimizacion
        tipoOptimizacion = False
        if optimizacion == "max" or optimizacion == "min":
            if optimizacion == "max":
                tipoOptimizacion = False
                return
            else:
                tipoOptimizacion = True
        else:
            print("Error. El tipo de optimizacion ingresado es incorrecto.")
            print("Favor ingrese \"min\" o \"max\"")
            exit(0)

    #Funcion verificarCantidadArgumentos. Verifica que la cantidad de argumentos de la primera linea del archivo
    #sea el correcto (cuatro). Tambien verifica que la cantidad de variables de decision y la cantidad de
    #restricciones sean un numero entero.
    #Entradas:
    #   La primera linea del archivo en formato de lista.
    #Salidas:
    #   Si la cantidad de parametros de la primera linea son 4 y los ultimos dos son numeros enteros, entonces
    #   estos ultimos dos se agregan a las variables globales cantidadVariablesDecision y cantidadRestricciones
    #   respectivamente.
    #   Si alguno falla, se despliega un mensaje de error en consola con lo que fallo.
    #Restricciones:
    #   Que la cantidad de argumentos de la lista sean 4.
    #   Que las ultimas dos variables sean enteros.
    def verificarCantidadArgumentos(primeraLineaEntradas):
        global cantidadVariablesDecision
        global cantidadRestricciones
        if len(primeraLineaEntradas) == 4:
            try:
                cantidadVariablesDecision = int(primeraLineaEntradas[2])
                cantidadRestricciones = int(primeraLineaEntradas[3])
            except ValueError:
                print("Error. Los valores ingresados para el numero de variables de decision")
                print("y numero de restricciones no son numeros enteros.")
                print("Favor ingresar numeros validos.")
                exit(0)
        else:
            print("Error. La cantidad de argumentos en la primera linea del archivo no esta correcta.")
            print("Favor ingresar en este orden, separado por comas y sin espacios:")
            print("Metodo, optimizacion, numero de variables de decision, numero de restricciones.")
            exit(0)

    #Funcion verificarCoeficientesFuncionObjetivo. Verifica que la cantidad de coeficientes de la funcion 
    #objetivo concuerde con la cantidad de variables de decision. Tambien verifica que los coeficientes
    #sean un numero entero.
    #Entradas:
    #   Los coeficientes de la funcion objetivo en una lista.
    #Salidas:
    #   Si la cantidad de parametros de la funcion objetivo concuerda con la cantidad de variables de
    #   decision, y cada coeficiente es un valor entero, entonces se agregan los coeficientes a la lista
    #   coeficientesFuncionObjetivo.
    #   Si alguno falla, se despliega un mensaje de error en consola con lo que fallo.
    #Restricciones:
    #   Que la cantidad de argumentos de la funcion objetivo concuerde con la cantidad de variables de decision.
    #   Que los coeficientes sean valores enteros.
    def verificarCoeficientesFuncionObjetivo(funcionObjetivo):
        global cantidadVariablesDecision
        global coeficientesFuncionObjetivo
        coeficientesFuncionObjetivo = []
        if cantidadVariablesDecision == len(funcionObjetivo):
            for indice in funcionObjetivo:
                try:
                    coeficientesFuncionObjetivo.append(float(indice))
                except ValueError:
                    print("Error. Uno de los coeficientes de la funcion objetivo no es un numero entero.")
                    print("Favor ingresar numeros validos.")
                    exit(0)
            return
        else:
            print("Error. La cantidad de coeficientes de la funcion objetivo es distinta")
            print("a la cantidad de variables de decision.")
            exit(0)

    #Funcion verificarRestricciones. Verifica que
    #   - La cantidad de restricciones sea igual a la cantidad de restricciones ingresadas en la primera linea del archivo.
    #   - Cada restriccion tenga valores enteros
    #   - Que la restriccion tenga un formato valido (n coeficientes + mayor, menor o igual + resultado)
    #   - Que si se usa metodo simplex, que las restricciones solo contengan <=.
    #Entradas:
    #   La listaEntrada generada por leerArchivo.
    #Salidas:
    #   Si las tres restricciones se cumplen, se agrega la lista de restricciones a coeficientesRestricciones.
    #   Si alguno falla, se despliega un mensaje de error en consola con lo que fallo.
    #Restricciones:
    #   - La cantidad de restricciones sea igual a la cantidad de restricciones ingresadas en la primera linea del archivo.
    #   - Cada restriccion debe tener valores enteros
    #   - Cada restriccion debe tener un formato valido (n coeficientes + mayor, menor o igual + resultado)
    #   - Si se usa metodo simplex, las restricciones solo deben contener <=.
    def verificarRestricciones(listaEntrada):
        global cantidadRestricciones
        global cantidadVariablesDecision
        global coeficientesRestricciones
        global metodo
        coeficientesRestricciones = []
        if (len(listaEntrada)-2) == int(cantidadRestricciones):
            for fila in range (2, len(listaEntrada)):
                listaTemporal = []
                if (len(listaEntrada[fila])-2) != cantidadVariablesDecision:
                    print("Error. La restriccion numero " + str(fila-1) + " contiene un numero")
                    print("de variables incorrecto. Favor revisar e intentar de nuevo.")
                    exit(0)
                else:
                    for columna in listaEntrada[fila]:
                        if columna in ["<=", "=", ">="]:
                            if columna in ["=", ">="] and metodo == 0:
                                print("Error. La restriccion numero " + str(fila-1) + " contiene un")
                                print("\"" + columna + "\" pero el problema es un metodo simplex, por lo que")
                                print("no se puede resolver. Favor revisar e intentar de nuevo")
                                exit(0)
                            else:
                                listaTemporal.append(columna)
                        else:
                            try:
                                listaTemporal.append(float(columna))
                            except ValueError:
                                print("Error. Alguno de los coeficientes de la restriccion " + str(fila-1))
                                print("No es un valor entero. Favor revisar e intentar de nuevo.")
                                exit(0)
                if (listaEntrada[fila][-2]) not in ["<=", "=", ">="]:
                    print("Error. La restriccion " + str(fila-1) + " no posee un formato valido.")
                    print("Favor revisar e intentar de nuevo.")
                    exit(0)
                coeficientesRestricciones.append(listaTemporal)
        else:
            print("Error. La cantidad de restricciones no concuerda.")
            print("Favor revisar e intentar de nuevo.")
            exit(0)


    #Funcion verificarDegenerada. Si una solucion tiene degenerada, se llama a esta funcion, para incluirlo en el archivo de solucion.
    #Entradas:
    #   estadoDegenerada: Es un int que nos dice en que numero de estado se encontro la degenerada.
    #   esDegenerada: Variable tipo booleana que determina si la solucion es degenerada.
    #Salidas:
    #   Si existe degenerada, imprime en el archivo que hubo una solucion degenerada.
    #Restricciones:
    #   Ninguna.
    def verificarDegenerada(estadoDegenerada):
        global esDegenerada
        if esDegenerada == True:
            #print("\n\n Aviso: En el estado " + str(estadoDegenerada) + " se encontro una solucion degenerada. \n")
            archivo.write("\n\n Aviso: En el estado " + str(estadoDegenerada) + " se encontro una solucion degenerada. \n")


#---------------------------Impresion gran M---------------------------#
            
    #Funcion imprimirColumnas. Esta se va a usar dentro de la funcion imprimirMatriz para imprimir los nombres de las columnas 
    #en el archivo para cada iteracion. 
    #Entradas:
    #   nombresColumnas: Variable global tipo lista de strings que va a contener los nombres de las columnas
    #Salidas:
    #   Imprime en el archivo los nombres de las columnas para cada iteracion.
    #Restricciones:
    #   Ninguna.
    def imprimirNombreColumnas():
        global nombresColumnas
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
    def imprimirFuncionObjetivo():
        global nombresFilas
        global tabla
        lineaInferior = "********"
        lineaFuncionObjetivo = "|" + nombresFilas[0] + "\t|" #Imprime la letra U
        for valor in tabla[0]:
            lineaInferior = lineaInferior + "*************"
            valorM = round(valor.numeroM, 2) #Redondea a dos digitos el valor del numero que se suma / resta con M
            valorSinM = round(valor.numeroSinM, 2) #Redondea a dos digitos el valor del numero que esta multiplicado con M
            if valor.numeroM == 0: #Si la M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "\t     |" #Se imprime solo el valor sin M
            elif valor.numeroM != 0 and valor.numeroSinM == 0: #Si la M no es cero, pero el valor sin M es cero
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorM) + "M\t    |" #Se imprime el valor M
            else: #Si ambos tienen valores
                lineaFuncionObjetivo = lineaFuncionObjetivo + str(valorSinM) + "+" + str(valorM) + "M\t    |" #Se imprimen ambos
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
    def imprimirMatriz():
        global nombresFilas
        global tabla
        if(len(tabla) is not 0): #Si la tabla no esta vacia
            ManejoArchivos.imprimirNombreColumnas()
            ManejoArchivos.imprimirFuncionObjetivo()
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
