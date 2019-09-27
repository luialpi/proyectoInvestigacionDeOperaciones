class VerificarArchivoEntrada:

    global nombreArchivoEntrada
    global metodo #Variable tipo float. 0=Simplex, 1=GranM, 2=DosFases, 3=Dual
    global tipoOptimizacion #Variable tipo booleana. True=max, False=min
    global cantidadVariablesDecision #Variable tipo float. Cantidad de variables de decision
    global cantidadRestricciones #Variable tipo float. Cantidad de restricciones
    global coeficientesFuncionObjetivo #Variable tipo Lista de floats. Los coeficientes de las variables de la funcion objetivo
    #Ejemplo: [3.0, 5.0]
    global coeficientesRestricciones #Variable tipo Matriz de floats. Los coeficientes de las restricciones y su signo
    #Ejemplo: [[2.0, 1.0, '<=', 6.0], [-1.0, 3.0, '=', 9.0], [0.0, 1.0, '>=', 4.0]]
    
    global esArchivoConError #Variable booleana que se activa si el archivo de entrada genero un error. 

    #Constructor
    def __init__(self):
        pass

    #Funcion getListaConfiguraciones. Regresa las configuraciones necesarias para correr cada metodo.
    #Dependiendo del metodo, se devuelve una lista de configuraciones diferente.
    def getListaConfiguraciones():
        global metodo
        elegirMetodo = {0:VerificarArchivoEntrada.generarVariablesSimplex(), 1:VerificarArchivoEntrada.generarVariablesGranM(), 2:2, 3:3}
        return [metodo, elegirMetodo.get(metodo)]

    def generarVariablesSimplex():
        global cantidadVariablesDecision
        global cantidadRestricciones
        global coeficientesFuncionObjetivo
        global coeficientesRestricciones
        global tipoOptimizacion
        #nombresColumnas = []
        #nombresFilas = ["U"]

        #hacer un for para que la funcion objetivo quede del mismo tamano.
        matrizInicial = []
        matrizInicial.append(coeficientesFuncionObjetivo) #Formato [[3,5], [2, 1, 6, <=], [-1, 3, 9, =], [0, 1, 4, >=,]]
        #for valor in range(cantidadVariablesDecision):
        #    nombresColumnas.append("x" + str(valor + 1))

        #for valor in range(cantidadRestricciones):
        #    nombresColumnas.append("S" + str(valor + 1))
        #    nombresFilas.append("S" + str(valor + 1))

        for fila in coeficientesRestricciones:
            filaNueva = []
            for valor in fila:
                if valor not in ["=", ">=", "<="]:
                    filaNueva.append(valor)
            filaNueva.append(fila[-2])
            matrizInicial.append(filaNueva)

        #print([matrizInicial, nombresColumnas, nombresFilas, tipoOptimizacion])
        #return [matrizInicial, nombresColumnas, nombresFilas, tipoOptimizacion]
        return [matrizInicial, tipoOptimizacion]
        
    def generarVariablesGranM():
        global cantidadVariablesDecision
        global cantidadRestricciones
        global coeficientesFuncionObjetivo
        global coeficientesRestricciones
        global tipoOptimizacion
        #Entrada: [nombreArchivoEntrada,
        #False=max, True=min, [coeficientesFuncionObjetivo],
        #[[restriccion1, al final desigualdad, final-1 resultado]], numero variables]

        coeficientesNuevosRestricciones = []
        for fila in coeficientesRestricciones:
            filaNueva = []
            for valor in fila:
                if valor not in ["=", ">=", "<="]:
                    filaNueva.append(valor)
            filaNueva.append(fila[-2])
            coeficientesNuevosRestricciones.append(filaNueva)
        
        return [cantidadVariablesDecision, coeficientesNuevosRestricciones, coeficientesFuncionObjetivo, not tipoOptimizacion]

    def generarVariablesDosFases():
        return "variablesDosFases"

    def generarVariablesDual():
        return "variablesDual"
        
    
    #Funcion leerArchivo. Lee el archivo de configuracion para convertirlo en una lista.
    #Entradas:
    #   Archivo de configuracion.
    #Salidas:
    #   Lista con las configuraciones.
    #Restricciones:
    #   Que el archivo exista.
    def leerArchivo(nombreArchivoEntrada):
        global esArchivoConError
        esArchivoConError = False
        listaEntrada = []
        try:
            archivoInicial = open(nombreArchivoEntrada, "r")
        except(FileNotFoundError):
            print("Error. Archivo de entrada: \"" + nombreArchivoEntrada + "\" no presente.\n")
            esArchivoConError = True
            return esArchivoConError
        except(OSError):
            print("Error de OS: El argumento: \"" + nombreArchivoEntrada + "\" es invalido.\n")
            esArchivoConError = True
            return esArchivoConError
            
        listaArchivo = archivoInicial.readlines()
        archivoInicial.close()
        for indice in listaArchivo:
            entrada = indice.split(",")
            entrada[len(entrada)-1] = entrada[len(entrada)-1].strip('\n')
            listaEntrada.append(entrada)
        
        VerificarArchivoEntrada.verificarArchivoConfiguracion(listaEntrada)
        return esArchivoConError

    #Funcion verificarArchivoConfiguracion. Esta funcion verifica que todos los datos introducidos
    #en el archivo de configuracion esten bien.
    #Entradas:
    #   La listaEntrada generada por leerArchivo.
    #Salidas:
    #   Ninguna.
    #Restricciones:
    #   Ninguna.
    def verificarArchivoConfiguracion(listaEntrada):
        VerificarArchivoEntrada.verificarTipoMetodo(listaEntrada[0][0])
        VerificarArchivoEntrada.verificarTipoOptimizacion(listaEntrada[0][1])
        VerificarArchivoEntrada.verificarCantidadArgumentos(listaEntrada[0])
        VerificarArchivoEntrada.verificarCoeficientesFuncionObjetivo(listaEntrada[1])
        VerificarArchivoEntrada.verificarRestricciones(listaEntrada)

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
        global esArchivoConError
        metodo = ""
        if tipoMetodo in ["0", "1", "2", "3"]:
            metodo = int(tipoMetodo)
        else:
            print("Error. El tipo de metodo ingresado es incorrecto.")
            print("Favor ingresar 0=Simplex, 1=GranM, 2=DosFases, 3=Dual")
            esArchivoConError = True

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
        global esArchivoConError
        tipoOptimizacion = ""
        if optimizacion == "max" or optimizacion == "min":
            if optimizacion == "max":
                tipoOptimizacion = True
                return
            else:
                tipoOptimizacion = False
        else:
            print("Error. El tipo de optimizacion ingresado es incorrecto.")
            print("Favor ingrese \"min\" o \"max\"")
            esArchivoConError = True

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
        global esArchivoConError
        if len(primeraLineaEntradas) == 4:
            try:
                cantidadVariablesDecision = int(primeraLineaEntradas[2])
                cantidadRestricciones = int(primeraLineaEntradas[3])
            except ValueError:
                print("Error. Los valores ingresados para el numero de variables de decision")
                print("y numero de restricciones no son numeros enteros.")
                print("Favor ingresar numeros validos.")
                esArchivoConError = True
        else:
            print("Error. La cantidad de argumentos en la primera linea del archivo no esta correcta.")
            print("Favor ingresar en este orden, separado por comas y sin espacios:")
            print("Metodo, optimizacion, numero de variables de decision, numero de restricciones.")
            esArchivoConError = True

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
        global esArchivoConError
        coeficientesFuncionObjetivo = []
        if cantidadVariablesDecision == len(funcionObjetivo):
            for indice in funcionObjetivo:
                try:
                    coeficientesFuncionObjetivo.append(float(indice))
                except ValueError:
                    print("Error. Uno de los coeficientes de la funcion objetivo no es un numero entero.")
                    print("Favor ingresar numeros validos.")
                    esArchivoConError = True
            return
        else:
            print("Error. La cantidad de coeficientes de la funcion objetivo es distinta")
            print("a la cantidad de variables de decision.")
            esArchivoConError = True

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
        global esArchivoConError
        coeficientesRestricciones = []
        if (len(listaEntrada)-2) == int(cantidadRestricciones):
            for fila in range (2, len(listaEntrada)):
                listaTemporal = []
                if (len(listaEntrada[fila])-2) != cantidadVariablesDecision:
                    print("Error. La restriccion numero " + str(fila-1) + " contiene un numero")
                    print("de variables incorrecto. Favor revisar e intentar de nuevo.")
                    esArchivoConError = True
                else:
                    for columna in listaEntrada[fila]:
                        if columna in ["<=", "=", ">="]:
                            if columna in ["=", ">="] and metodo == 0:
                                print("Error. La restriccion numero " + str(fila-1) + " contiene un")
                                print("\"" + columna + "\" pero el problema es un metodo simplex, por lo que")
                                print("no se puede resolver. Favor revisar e intentar de nuevo")
                                esArchivoConError = True
                            else:
                                listaTemporal.append(columna)
                        else:
                            try:
                                listaTemporal.append(float(columna))
                            except ValueError:
                                print("Error. Alguno de los coeficientes de la restriccion " + str(fila-1))
                                print("No es un valor entero. Favor revisar e intentar de nuevo.")
                                esArchivoConError = True
                if (listaEntrada[fila][-2]) not in ["<=", "=", ">="]:
                    print("Error. La restriccion " + str(fila-1) + " no posee un formato valido.")
                    print("Favor revisar e intentar de nuevo.")
                    esArchivoConError = True
                coeficientesRestricciones.append(listaTemporal)
        else:
            print("Error. La cantidad de restricciones no concuerda.")
            print("Favor revisar e intentar de nuevo.")
            esArchivoConError = True
