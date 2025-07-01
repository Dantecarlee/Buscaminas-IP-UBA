import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))



# Lista que contenga los valores de los números que puede tener cada celda pero con tipo "str"
valores: list[str] = ["0","1","2","3","4","5","6","7","8"] # Luego se usa como global dentro de las funciones



def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    '''
    ARMA UN TABLERO QUE SOLO CUENTA CON CEROS Y BOMBAS EN LOS LUGARES ELEGIDOS POR ELEGIR_BOMBAS()
    
Args:    
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    minas: Número mayor a cero que representa la cantidad de minas que tiene un tablero

Returns:
    Un tablero en el que las casillas son "0" (donde no hay bomba) o "-1" (donde se eligió que haya una bomba)
    '''
    
    lista_resultado: list[list[int]]  = []
    lista_minas: list[tuple[int,int]] = elegir_bombas(filas,columnas,minas)
    
    for i in range(filas):
        
        lista_fila: list[int] = []
              
        for j in range(columnas):
            
            # "-1" Si fue elegida por elegir_bombas            
            if (i,j) in lista_minas: lista_fila.append(-1)
                
            else: lista_fila.append(0)
            
        lista_resultado.append(lista_fila)
        
    return lista_resultado

def elegir_bombas(filas:int, columnas: int, minas:int) -> list[tuple[int,int]]:
    '''
    ELIJE DE MANERA ALEATORIA LA COORDENADA DE CADA UNA DE LAS MINAS QUE DEBE COLOCAR
    
Args:
    filas: Número mayor a cero que representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    minas: Número mayor a cero que representa la cantidad de minas que tiene un tablero

Returns:
    Un lista con una cantidad de elementos igual a "minas", que contiene tuplas de dos elementos que representan las coordenadas donde se encuentra cada mina
       
    '''
    
    lista_posiciones: list[tuple[int, int]] = []
    
    # Cargamos las posiciones del tablero
    for i in range(filas):
        for j in range(columnas):
            lista_posiciones.append((i,j))
    
    # ELegimos una cantidad de esas posiciones     
    return random.sample(lista_posiciones, minas)



def calcular_numeros(tablero: list[list[int]]) -> None:
    '''
    CALCULA EL NÚMERO QUE DEBE TENER CADA CELDA SEGÚN LA CANTIDAD DE MINAS QUE TIENE EN SUS CELDAS ADYACENTES
    SOLO MODIFICA EL VALOR DE LA CELDA EN CASO DE QUE LA MISMA NO SEA UNA BOMBA (UN "-1")
    
Args:    
    tablero: Una matriz bidimensional que se irá recorriendo y cuyos valores internos van a ir cambiando según lo que devuelva la función calcular_minas
    '''
    largo_fila: int = len(tablero[0])
    
    for fila in range(len(tablero)):
        for col in range(largo_fila):
            
            if tablero[fila][col] != -1:                         
                tablero[fila][col] = calcular_cantidad_minas_adyacentes(tablero, (fila,col))
            
def calcular_cantidad_minas_adyacentes(tablero: list[list[int]], coordenada: tuple[int,int]) -> int:
    '''
    CALCULA EL NÚMERO QUE DEBE TENER UNA CELDA DE ACUERDO A LA CANTIDAD DE MINAS QUE TIENE EN SUS CELDAS ADYACENTES
    
Args:    
    tablero: Una matriz bidimensional cuyos valores internos son "0" (si no es una bomba) o "-1" (si es una bomba )
    coordenada: Una tupla de dos elementos, que demarcan una celda específica, teniendo en cuenta que el primer número corresponde a su fila y el segundo a su columna
    
Returns:
    El número de minas que tiene la coordenada elegida en sus celdas adyacentes
    '''
    
    res: int = 0
    cant_filas: int = len(tablero)
    cant_col: int = len(tablero[0])
    
# Buscamos recorrer las filas y columnas adyacentes a la posicón a la que accedemos, el "-1" para la anterior, y el "+2" para la posterior (teniendo en cuenta que el range() es excluyente) 
    for i in range((coordenada[0])-1,(coordenada[0])+2):
        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            # Verifica que la coordenada a revisar esté dentro del tablero
            if i >= 0 and j >= 0 and i < cant_filas and j < cant_col:
                
                if (i,j) != coordenada and tablero[i][j] == -1 : 
                    res += 1   
                
    return res 
  


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego: 
    '''
    CREA UN ESTADO VÁLIDO CON EL QUE SE VA A JUGAR 
    
Args:    
    filas: Número mayor a cero que representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    minas: Número mayor a cero que representa la cantidad de minas que tiene un tablero

Returns:
    Un diccionario que contiene la cantidad de filas, de columnas y de minas que hay en el tablero, un booleano que determina
    que el juego no está terminado, el tablero con la información interna de cada celda, y el tablero visible lleno de celdas "VACÍO"
    '''  
    estado: EstadoJuego = {
        "filas" : filas,
        "columnas" : columnas,
        "minas" : minas,
        "juego_terminado" : False,
        "tablero" : colocar_minas(filas,columnas,minas),
        "tablero_visible": tablero_vacio(filas,columnas)       
    }
    
    calcular_numeros(estado["tablero"])
    
    return estado
    
def tablero_vacio(filas: int, columnas: int) -> list[list[str]]:
    '''
    CREA UN TABLERO VISIBLE LLENO DE "VACÍO" PARA PONER EN EL ESTADO DE CREAR_JUEGO()
    
Args:    
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero

Returns:
    Un tablero con las dimensiones requeridas en las que todas las celdas contienen el valor "VACÍO" (" ")
    '''
    
    tablero: list[list[str]] = []
    
    for i in range(filas):
        listas: list[str] = []
        
        for j in range(columnas):
            listas.append(VACIO)
        
        tablero.append(listas) 
        
    return tablero

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[int]]) -> bool:
    '''
    VERIFICA SI TODAS LAS CELDAS QUE NO SON BOMBAS YA FUERON DESCUBIERTAS

Args:
    tablero: Una matriz bidimensional cuyos valores internos son números enteros entre 0 (cero) y 8 (ocho), o "-1" (si es una bomba )
    tablero_visible: Una matriz bidimensional cuyos valores internos pueden ser números enteros 
                     entre 0 y 8 (con tipo de dato "str"), o una BOMBA, o una BANDERA, o VACIO.

Returns:
    True si todas las celdas de tablero visible que no son bombas fueron descubiertas
    '''

    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero[i][j] == -1:
                if tablero_visible[i][j] == BOMBA: return False
                
            else:
                if str(tablero_visible[i][j]) != str(tablero[i][j]):
                    return False
                
    return True
                    


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    '''
    DADO UN ESTADO, DEVUELVE UNA COPIA DEL TABLERO VISIBLE DEL MISMO

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    El tablero visible del estado del juego cuyos valores internos pueden ser números enteros 
    entre 0 y 8 (con tipo de dato "str"), o una BOMBA, o una BANDERA, o VACIO.
    '''

    res: list[list[Any]] = []
    
    for fila in estado["tablero_visible"]:
        copia_fila = fila.copy()
        res.append(copia_fila)
        
    return res
        


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    '''
    COLOCA UNA BANDERA EN EL TABLERO VISIBLE O LA QUITA, EN CASO DE INTENTAR
    COLOCARLA EN UN CASILLERO EN EL QUE YA HAY UNA DE ELLAS.

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    '''
    
    if estado["juego_terminado"] == False:
        
        celda = estado["tablero_visible"][fila][columna]
        
        if celda == VACIO:
            estado["tablero_visible"][fila][columna] = BANDERA
            
        elif celda == BANDERA:
            estado["tablero_visible"][fila][columna] = VACIO



def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    '''
    CAMBIA EL VALOR DEL TABLERO VISIBLE EN UNA (O MÁS) CELDAS DESDE VACÍO AL NÚMERO QUE LA CELDA
    POSEE EN EL TABLERO, O UNA BOMBA, EN CASO DE QUE EN TABLERO HAYA UN "-1"

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    
Modify:
    Modifica el tablero visible. Descube todas las celdas que marque caminos_descubiertos() 
    '''

    # No modifica nada si el juego está terminado
    if estado["juego_terminado"] == False:
        
        
        if verificacion_y_accionamiento_si_perdiste(estado,fila,columna) == False:
            
            celdas_descubiertas = []     
            
            posiciones_descubiertas(estado["tablero"], estado["tablero_visible"], fila,columna, celdas_descubiertas)
            
            for i in range(estado["filas"]):
                for j in range(estado["columnas"]):
                    
                    if (i,j) in celdas_descubiertas:
                        # Descubre las posiciones en celdas_descubiertas
                        estado["tablero_visible"][i][j] = str(estado["tablero"][i][j])

        
        estado["juego_terminado"] = (verificar_victoria(estado) or verificacion_y_accionamiento_si_perdiste(estado,fila,columna))

def posiciones_descubiertas(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int, celdas_descubiertas:list[tuple[int,int]]) -> None:
    '''
     AGREGA LAS POSICIONES QUE SE DEBERÁN DESCUBIRI A UNA VARIABLE LLAMADA CLEDAS_DESCUBIERTAS.
     AGREGARÁ UNA SOLA EN CASO DE QUE LA CELDA MARCADA SEA UN NÚMERO MAYOR A 0, Y VARIAS SI LA MISMA ES UN 0

Args:
    tablero: Una matriz bidimensional cuyos valores internos son números enteros entre 0 (cero) y 8 (ocho), o "-1" (si es una bomba)
    tablero_visible: Una matriz bidimensional cuyos valores internos pueden ser números enteros 
                     entre 0 y 8 (con tipo de dato "str"), o una BOMBA, o una BANDERA, o VACIO.
    filas: Número mayor a cero que representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero

    '''

    if tablero[fila][columna] > 0:
        celdas_descubiertas.append((fila,columna))

    
    else: celda_es_cero(tablero, tablero_visible, fila, columna, celdas_descubiertas)
        
def celda_es_cero(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int, celdas_descubiertas:list[tuple[int,int]]) -> None:
    '''
    SI EL VALOR DE LA CELDA DESCUBIERTA ES 0 (CERO), MUESTRA EL VALOR DE LAS CELDAS ADYACENTES QUE NO SON BOMBAS.
    SI ALGUNA DE LAS CELDAS ADYACENTES ES 0, SE APLICA LA FUNCIÓN EN FORMA RECURSIVA PARA DESCUBRIR AÚN MÁS CELDAS

Args:
    tablero: Una matriz bidimensional cuyos valores internos son números enteros entre 0 (cero) y 8 (ocho), o "-1" (si es una bomba)
    tablero_visible: Una matriz bidimensional cuyos valores internos pueden ser números enteros 
                     entre 0 y 8 (con tipo de dato "str"), o una BOMBA, o una BANDERA, o VACIO.    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero

Returns:
    Una lista de las coordenadas de las celdas descubiertas, es decir, la celda que se quiere descubrir
    y sus adyacentes no bombas
    '''

    coordenada: list[int] = [fila,columna]
    celdas_descubiertas.append((fila,columna)) 
         
    # Buscamos recorrer las filas y columnas adyacentes a la posicón a la que accedemos, el "-1" para la anterior, y el "+2" para la posterior (teniendo en cuenta que el range() es excluyente) 
      
    for i in range((coordenada[0])-1,(coordenada[0])+2):        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            # Verifica que la coordenada a revisar esté dentro del tablero
            if i >= 0 and j >= 0 and i < len(tablero) and j < len(tablero[0]):

                # Si la celda descubierta es un 0 que no está ya en celdas_descubiertas (para que no se genere una recursividad infinita):
                if tablero[i][j] == 0 and (i,j) not in celdas_descubiertas:
                    celda_es_cero(tablero, tablero_visible, i, j, celdas_descubiertas)
                    
                else: celdas_descubiertas.append((i,j)) 

def verificacion_y_accionamiento_si_perdiste(estado: EstadoJuego, fila: int, columna: int) -> bool:
    '''
    VERIFICA SI PERDISTE EL JUEGO, ES DECIR, SI LA CELDA DESCUBIERTA CORRESPONDE
    A UNA BOMBA. DE HABER PERDIDO, CAMBIA EL ESTADO DE JUEGO_TERMINADO, Y DESCUBRE TODAS LAS BOMBAS DEL TABLERO.

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    
Returns:
    True si la celda seleccionada corresponde a una bomba. False si no lo hace.
    
Modify:
    Juego_terminado será True y tablero_visible tendrá todas las bombas a la vista en caso de haber perdido
    '''
    
    if estado["tablero"][fila][columna] == -1:    
        estado["juego_terminado"] = True
        mostrar_bombas(estado)
        return True
                        
    return False

def mostrar_bombas(estado: EstadoJuego) -> None:
    '''
    MUESTRA TODAS LAS BOMBAS DEL TABLERO VISIBLE

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego
    '''
    
    for i in range(len(estado["tablero"])):
        for j in range(len(estado["tablero"][0])):
            
            if estado["tablero"][i][j] == -1:
                estado["tablero_visible"][i][j] = BOMBA
        
    
    
def verificar_victoria(estado: EstadoJuego) -> bool:
    '''
    VERIFICA SI GANASTE EL JUEGO, ES DECIR, SI TODAS LAS CELDAS SEGURAS FUERON DESCUBIERTAS

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    True si todas las celdas que no son bombas ya fueron descubiertas
    '''

    return todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"])



def reiniciar_juego(estado: EstadoJuego) -> None:
    '''
    CREA OTRO ESTADO DE JUEGO NUEVO SOBRE EL EXISTENTE, DESDE CERO, ESTANDO EL TABLERO VISIBLE TOTALMENTE VACÍO.
    EL MISMO TENDRÁ LAS MISMAS DIMENSIONES QUE EL ESTADO DE JUEGO ANTERIOR, PERO SU TABLERO SERÁ DISTINTO.

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego. Es el estado anterior que poseía el juego.
    '''

    estado2: EstadoJuego = crear_juego(estado["filas"], estado["columnas"], estado["minas"])
    
    # Si el tablero del estado nuevo es igual al tablero del estado anterior:
    if estado2["tablero"] == estado["tablero"]: 
        
        # Modifica levemente el tablero del estado nuevo
        estado2 = cambio_de_una_posicion(estado2)
        
        
    estado["tablero"] = estado2["tablero"]
    estado["tablero_visible"] = estado2["tablero_visible"]
    estado["juego_terminado"] = estado2["juego_terminado"]
    
def cambio_de_una_posicion(estado: EstadoJuego) -> EstadoJuego:
    '''
    RECORREMOS EL TABLERO HASTA ENCONTTRAR UNA BOMBA, Y LUEGO LO RECORREMOS NUEVAMENTE PARA ENCONTRAR UNA POSICION NO-BOMBA CON LA QUE
    INTERCAMBIAR POSICIONES. LUEGO SE CALCULAN LOS NUMEROS QUE DEBE TENER EL NUEVO TABLERO.

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego. Es el estado anterior que poseía el juego.
    
Returns:
    Un estado de juego con una posición cambiada en el tablero
    '''
    
    # Recorre las posiciones del tablero en busca de una bomba
    for i in range(len(estado["tablero"])):
        for j in range(len(estado["tablero"][0])):
            
            if estado["tablero"][i][j] == -1:
                
                # Recorre nuevamente las posiciones del tablero desde (0,0) para encontrar un elemento NO-bomba
                for k in range(len(estado["tablero"])):
                    for l in range(len(estado["tablero"][0])):
                         
                        if estado["tablero"][k][l] != -1:
                            
                            # Intercambia los lugares entre ambos elementos encontrados
                            estado["tablero"][i][j] = 1
                            estado["tablero"][k][l] = -1
                            
                            # Calcula los números que tendrá cada celda con los cambios hechos
                            
                            calcular_numeros(estado["tablero"])
                            
                            return estado
                                    
       
        
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    '''
    GUARDA EL EL TABLERO Y EL TABLERO VISIBLE DEL ESTADO DE JUEGO ACTUAL EN DOS ARCHIVOS DE TEXTO

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego
    ruta_directorio: La dirección o la ruta de acceso hacia la carpeta donde se almacenan los archivos de texto
    
Modify: En tablero.txt escribe los elementos del tablero, separados por comas, utilizando una linea por fila
        En el tablero_visible.txt escribe los elementos del tablero reemplazando a la BANDERA por "*", al VACIO por "?". Los elementos
        numéricos los escribe igual que lo hizo con tablero.txt
    '''
    
    # -- ESTO ES DE TABLERO.TXT --------------------------------------------------------------
    
    # Crea la ruta de acceso para tablero.txt    
    ruta_tablero = os.path.join(ruta_directorio, "tablero.txt")
    
    archivo = open(ruta_tablero, "w", encoding="UTF-8")
    
    # Traslada el tablero del estado a texto separado por comas
    for i in range(len(estado["tablero"])):
            for j in range(len(estado["tablero"][0])): 
                if j == (len(estado["tablero"][0]))-1: archivo.write(str(estado["tablero"][i][j]))                    
                else : archivo.write(str(estado['tablero'][i][j]) + ",")  
                
            # Mientras no se encuentre en la última fila, genera un cambio de linea luego de escribir la linea
            if i != len(estado["tablero"])-1:        
                archivo.write("\n")
                
    archivo.close()
    
    
    # -- ESTO ES DE TABLERO_VISIBLE.TXT --------------------------------------------------------------
    
    # Crea la ruta de acceso para tablero_visible.txt 
    ruta_tablero_visible = os.path.join(ruta_directorio, "tablero_visible.txt")
    
    archivo = open(ruta_tablero_visible, "w", encoding="UTF-8")
    
    # Traslada el tablero visible del estado a texto separado por comas
    for i in range(len(estado["tablero_visible"])):
            for j in range(len(estado["tablero_visible"][0])):
                 
                if j == (len(estado["tablero_visible"][0]))-1:
                    archivo.write(clasificar_celda(estado['tablero_visible'][i][j]))
                                 
                else : 
                    archivo.write(clasificar_celda(estado['tablero_visible'][i][j]) + ",")

            # Mientras no se encuentre en la última fila, genera un cambio de linea luego de escribir la linea
            if i != len(estado["tablero"])-1:        
                archivo.write("\n")
                
    archivo.close()

def clasificar_celda(celda: Any) -> str:
    '''
    REALIZA EL REEMPLAZO DE LAS CELDAS QUE SON BANDERA Y VACÍO PARA PODER UTILIZARLAS EN GUARDAR_ESTADO()

Args:
    celda: Casillero específico dentro del tablero visible cuyos valores internos pueden ser números enteros 
            entre 0 y 8 (con tipo de dato "str"), o una BOMBA, o una BANDERA, o VACIO.
    
Return:
    El reemplazante de cada valor, excepto que el mismo sea numérico
    '''

    if celda == BANDERA: return "*"
    elif celda == VACIO: return "?"
    else: return celda



def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    '''
    REEMPLAZA TODAS LAS CARACTERÍSTICAS DEL ESTADO DE JUEGO ACTUAL POR LAS CARACTERÍSTICAS QUE TIENE 
    UN NUEVO ESTADO, DETERMINADO POR SU TABLERO Y SU TABLERO_VISIBLE, QUE SE ENCUENTRAN ALMACENADOS EN ARCHIVOS TXT

Args:
    estado: Diccionario que contiene toda información sobre la partida en juego. Es el estado de juego actual
    ruta_directorio: La dirección o la ruta de acceso hacia la carpeta donde se almacenan los archivos de texto

Returns:
    True si existen los archivos tablero.txt y tablero_visible.txt en la rua_directorio mecncionada y si los mismos son válidos para jugar.
    En este caso, el estado de juego actual se actualizará tomando los valores de el estado que se consiga con los archivos
    '''
    
    # Verifica si los archivos existen en la ruta mencionada
    if existe_archivo(ruta_directorio, "tablero.txt") and existe_archivo(ruta_directorio, "tablero_visible.txt"):
        
            # Lee el contenido de los archivos y los almacena en variables
            tablero_archivo: list[str] = archivo_como_lista(ruta_directorio, "tablero.txt")
            tablero_visible_archivo: list[str] = archivo_como_lista(ruta_directorio, "tablero_visible.txt")
                
            # Crea un estado de juego según las variables obtendidas desde los archivos
            estado_archivo: EstadoJuego = crear_estado_desde_archivo(tablero_archivo, tablero_visible_archivo)
                
            # Elimina tableros vacíos o con elementos inválidos
            if len(estado_archivo["tablero"]) > 0 and len(estado_archivo["tablero_visible"]) > 0:
                
                # Verifica que los tableros sean aptos para jugar
                
                if tablero_visible_correcto(tablero_visible_archivo,estado_archivo)[0] and tablero_correcto(tablero_archivo,estado_archivo)[0] and tablero_visible_correcto(tablero_visible_archivo,estado_archivo)[1] == tablero_correcto(tablero_archivo,estado_archivo)[1] and tablero_visible_correcto(tablero_visible_archivo,estado_archivo)[2] == tablero_correcto(tablero_archivo,estado_archivo)[2]:
                    
                    # Modifica el estado de juego previo por el estado de juego creado mediante los archivos
                    estado["filas"] = estado_archivo["filas"]
                    estado["columnas"] = estado_archivo["columnas"]
                    estado["minas"] = estado_archivo["minas"]
                    estado["juego_terminado"] = estado_archivo["juego_terminado"]
                    estado["tablero"] = estado_archivo["tablero"]
                    estado["tablero_visible"] = estado_archivo["tablero_visible"]
            
                    return True
      
    return False
    
def archivo_como_lista(ruta_directorio, archivo) -> list[str]:
    '''
    LEE UN ARCHIVO ESPECÍFICO Y DEVUELVE SU CONTENIDO EN UNA LISTA

Args:
    
    ruta_directorio: La dirección o la ruta de acceso hacia la carpeta donde se almacenan los archivos de texto
    archivo: archivo dentro del sistema de archivos del sistema operativo donde se encuentra o un tablero o un tablero visible

Returns:
    Una lista donde cada elemento es un string. Cada string es la lectura de una línea del archivo
    '''
    
    # Crea la ruta de acceso para entrar a leer tablero.txt 
    
    ruta_archivo = os.path.join(ruta_directorio, archivo)
    
    
    archivo = open(ruta_archivo, "r", encoding="UTF-8")
    
    # Lee el archivo y lo almacena
    lista_archivo: list[str] = archivo.readlines()
    
    archivo.close()
    
    return lista_archivo

def tablero_correcto(tablero_archivo: list[str], estado: EstadoJuego) -> tuple[bool,int,int]:
    '''
    VERIFICA QUE UN TABLERO QUE SE QUIERE CARGAR EN EL JUEGO CUMPLA LOS SIGUIENTES REQUISITOS:
        - TODAS LAS LINEAS TIENEN LA MISMA CANTIDAD DE ELEMENTOS VÁLIDOS
        - HAY AL MENOS UNA BOMBA EN EL TABLERO, y AL MENOS UN VALOR NO-BOMBA
        - NO HAY DOS COMAS SEGUIDAS EN EL TABLERO
        - LOS NÚMEROS QUE TIENE EL TABLERO SE CORRESPONDEN A LA CANTIDAD DE "-1" QUE TIENEN EN SUS CELDAS ADYACENTES
        
    EN LOS CASOS EN LOS QUE SE DEVUELVE UN VALOR FALSO, EL RETURN DARÁ UNA TUPLA CON ESTE BOOLEANO SEGUIDO DE DOS CEROS. ESTO
    SIMPLEMENTE PARA CUMPLIR CON EL TIPO DE DATO QUE DEVUELVE LA FUNCIÓN 
    
Args:    
    tablero_archivo: Una lista de strings que posee el contenido de un archivo en el que cada linea es un string diferente
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    Una tupla cuyo primer valor será True si el estado a evaluar cumple con todas las condiciones mencionadas, el segundo valor será
    la cantidad de filas que tiene el archivo, y el tercer valor, la cantidad de comas totales que tiene el archivo
    '''
    
    tablero: list[list[int]] = estado["tablero"]
    
    # Formatea el tablero_archivo para trabajar de manera más cómoda
    tablero_archivo: list[str] = formatear_lista_archivo(tablero_archivo)
    
    comas_totales: int = 0
    cantidad_filas_total:int= 0
    
    for fila in tablero_archivo:
        
        # False si las filas tienen dimensiones distintas        
        if cantidad_elementos_validos_fila_tablero(fila) != cantidad_elementos_validos_fila_tablero(tablero_archivo[0]): return (False,0,0)
                
    # False si no hay ninguna bomba en el tablero
    if hay_bomba(tablero_archivo) == False: return (False,0,0)
    
    
    # False si solo hay bombas en el tablero
    if todas_bombas(tablero_archivo) == True: return (False,0,0)
    
    for i in range(len(estado['tablero'])):
        j: int = 0
        k: int = 0
        comas_fila: int = 0
        
        
        # Falso si el tablero comienza en una ","
        if tablero_archivo[i][0] not in valores and tablero_archivo[i][0] != "-": return (False,0,0)
        
        
        # Falso si el tablero termina en una ","
        if tablero_archivo[i][len(tablero_archivo[i])-1] not in valores: return(False,0,0)       
        
        
        
        # Recorremos el tablero del archivo y el tablero del estado a la vez
        while j < len(tablero_archivo[i]) and k < len(estado['tablero'][i]):
            
            # Si la posición actual corresponde a una coma
            if tablero_archivo[i][j] == ",":
                comas_fila += 1
                            
                # False si hay dos comas seguidas                
                if tablero_archivo[i][j+1] == ",": return (False,0,0)
                j += 1
            
            # Si hay un "-" saltea el "1" siguiente
            if tablero_archivo[i][j] == "-":
                j +=1
                 
            # Si no hay un "-", debe figurar el número correspondiente a la cantidad de minas a su alrededor  
            elif tablero_archivo[i][j] != str(calcular_cantidad_minas_adyacentes(tablero, (i,k))): return (False,0,0)
            
            j += 1
            k += 1
               
        comas_totales += comas_fila
        cantidad_filas_total += 1    
        
    return (True,cantidad_filas_total,comas_totales)

def hay_bomba(tablero: list[str]) -> bool:
    '''
    VERIFICA SI HAY ALGUNA BOMBA (UN "-1") EN EL TABLERO
    
Args:    
    tablero: Una lista de strings que contiene el contenido de un archivo en el que cada linea es un string diferente

Returns:
    True si el tablero tiene un valor igual a "-1"
    '''
    
    for fila in tablero:
        if "-1" in fila:
            return True
        
    return False

def todas_bombas(tablero: list[str]) -> bool:
    '''
    VERIFICA SI HAY SOLO BOMBAS (TODOS "-1") EN EL TABLERO
    NO VERIFICAMOS QUE HAYA UN "-" SEGUIDO DE OTRO NÚMERO YA QUE ESTO NO PUEDE PASAR EN ESTE PUNTO.
    ESOS CASOS FUERON FILTRADOS ANTERIORMENTE
    
Args:    
    tablero: Una lista de strings que contiene el contenido de un archivo en el que cada linea es un string diferente

Returns:
    True si el tablero tiene solo valores iguales a "-1"
    '''
    for fila in tablero:
        
        i = 0
        while i < len(fila):
            
            if fila[i] == "-":
                i += 2  # saltamos "-1"

            elif fila[i] == ",":
                        i += 1  # ignoramos la coma
                        
            else: return False  # si no empieza con "-", no es válido
            
    return True

def cantidad_elementos_validos_fila_tablero(fila: str) -> int:
    '''
    CUENTA LA CANTIDAD ELEMENTOS VÁLIDOS QUE POSEE UNA FILA DE UN ARCHIVO PARA UN TABLERO.
    ELEMENTOS VÁLIDOS: NÚMERO ENTRE 0 Y 8 O UN "-1"
    
Args:    
    fila: Una cadena str que posee el contenido de una línea determinada de un archivo
    
Returns:
    La cantidad de elementos válidos que posee una línea de un archivo, o "-1" si hay un valor inválido en la misma
    '''
    contador: int = 0
    i: int = 0
    
    while i < len(fila):
        
        # Si es un número (0-8)
        if fila[i] in valores:  
            contador += 1
            i += 1
            
        elif fila[i] == "-" and i+1 < len(fila) and fila[i+1] == "1":  # Si es "-1"
            contador += 1
            i += 2  # Saltamos el "-1" completo
            
        # Si es una coma un espacio o un salto de línea lo ignora
        elif fila[i] == "," or fila[i] == " " or fila[i] == "\n":  
            i += 1
            
        # Si es un carácter inválido
        else: return -1  # Devuelve -1 asi falla la condicion 
    
    return contador
    
def formatear_lista_archivo(lineas_archivo: list[str]) -> list[str]:
    '''
    FORMATEA UNA LISTA DE STRINGS PROVENIENTE DE UN ARCHIVO: A CADA STRING LE QUITA EL SALTO DE LÍNEA
    Y TAMBIÉN LE QUITA LOS ESPACIO Y LAS LÍNEAS VACÍAS QUE TENGA 
    
Args:    
    tablero_archivo: Una lista de strings que posee el contenido de un archivo en el que cada linea es un string diferente

Returns:
    La misma lista sin  contener elementos vacíos ni espacios o saltos de línea en sus elementos.
    '''
    lineas_nuevas: list[str] = []
    
    for linea in lineas_archivo:
        linea_nueva: str = ""
        
        for elemento in linea:
            # Elimina saltos de línea y espacios
            if elemento not in ["\n"] and elemento != " ":  
                    linea_nueva += elemento
        
        if linea_nueva:  # Equivalente a len(linea_nueva) > 0
            lineas_nuevas.append(linea_nueva)
            
    return lineas_nuevas

def tablero_visible_correcto(tablero_visible_archivo: list[str], estado: EstadoJuego) -> tuple[bool,int,int]:
    '''
    VERIFICA QUE UN TABLERO VISIBLE QUE SE QUIERE CARGAR EN EL JUEGO CUMPLA LOS SIGUIENTES REQUISITOS:
        - TODAS LAS LINEAS TIENEN LA MISMA CANTIDAD DE ELEMENTOS VÁLIDOS
        - NO HAY DOS COMAS SEGUIDAS EN EL TABLERO VISIBLE
        - LOS NÚMEROS QUE TIENE EL TABLERO VISIBLE SE CORRESPONDEN A LOS NÚMEROS QUE TIENE LA MSIMA POSICION EN EL TABLERO ASOCIADO
    
    EN LOS CASOS EN LOS QUE SE DEVUELVE UN VALOR FALSO, EL RETURN DARÁ UNA TUPLA CON ESTE BOOLEANO SEGUIDO DE DOS CEROS. ESTO
    SIMPLEMENTE PARA CUMPLIR CON EL TIPO DE DATO QUE DEVUELVE LA FUNCIÓN 
    
Args:    
    tablero_archivo: Una lista de strings que posee el contenido de un archivo en el que cada linea es un string diferente
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    Una tupla cuyo primer valor será True si el estado a evaluar cumple con todas las condiciones mencionadas, el segundo valor será
    la cantidad de filas que tiene el archivo, y el tercer valor, la cantidad de comas totales que tiene el archivo
    '''
    
    tablero_visible_archivo: list[str] = formatear_lista_archivo(tablero_visible_archivo)
    
    comas_totales: int = 0
    cantidad_filas_total:int= 0
    
    for fila in tablero_visible_archivo:
        # False si las filas tienen dimensiones distintas
        if cantidad_elementos_validos_fila_visible(fila) != cantidad_elementos_validos_fila_visible(tablero_visible_archivo[0]): return (False,0,0)
    
    for i in range(len(estado['tablero_visible'])):
        
        j: int = 0
        k: int = 0
        comas_fila: int = 0
        
        # Falso si el tablero comienza en una ","
        if tablero_visible_archivo[i][0] not in valores and tablero_visible_archivo[i][0] not in ["?", "*"]: return (False,0,0)
        
        # Falso si el tablero termina en una ","
        if tablero_visible_archivo[i][len(tablero_visible_archivo[i])-1] not in valores and tablero_visible_archivo[i][len(tablero_visible_archivo[i])-1] not in["?","*"]: return (False,0,0)
        
        
        while j < len(tablero_visible_archivo[i]) and k < len(estado['tablero_visible'][i]):
            
            # Si la posicion actual corresponde a una coma:
            if tablero_visible_archivo[i][j] == ",":
                comas_fila += 1
                
                # False si hay dos comas seguidas
                if tablero_visible_archivo[i][j+1] == ",": return (False,0,0)
                j += 1
              
            if (len(estado["tablero"]) == len(estado["tablero_visible"])) and (len(estado["tablero"][0]) == len(estado["tablero_visible"][0])):
                
                # Debe figurar el número correspondiente a la cantidad de minas a su alrededor
                if tablero_visible_archivo[i][j] in valores and tablero_visible_archivo[i][j] != str(calcular_cantidad_minas_adyacentes(estado["tablero"], (i,k))): return (False,0,0)
            
            j += 1
            k += 1
                   
        comas_totales += comas_fila
        cantidad_filas_total += 1
        
    return (True,cantidad_filas_total,comas_totales)

def cantidad_elementos_validos_fila_visible(fila: str) -> int:
    '''
    CUENTA LA CANTIDAD ELEMENTOS VÁLIDOS QUE POSEE UNA FILA DE UN ARCHIVO PARA UN TABLERO VISIBLE.
    ELEMENTOS VÁLIDOS: NÚMERO ENTRE 0 Y 8, UN VACÍO ("?") O UNA BANDERA ("*")
    
Args:    
    fila: Una cadena str que posee el contenido de una línea determinada de un archivo
    
Returns:
    La cantidad de elementos válidos que posee una línea de un archivo, o "-1" si hay un valor inválido en la misma
    '''
    
    contador: int = 0
    i: int = 0
    
    while i < len(fila):
        if fila[i] in ["*","?"] or fila[i] in valores:  # Si es un número (0-8) o vacio/bandera
            contador += 1
            i += 1
            
        # Si es una coma un espacio o un salto de línea lo ignora
        elif fila[i] == "," or fila[i] == " " or fila[i] == "\n": i+=1
        
        # Si es un carácter inválido
        else: return -1  # Devuelve -1 asi falla la condicion 
        
    return contador                     
              
def crear_tablero(tablero: list[str]) -> list[list[int]]:
    '''
    CREAR UN TABLERO DESDE UNA LISTA PROVENIENTE DE UN ARCHIVO 

Args:
    tablero: Una lista de strings, que sale de archivo_como_lista(), en la que cada string representa los valores
    que debe tener una fila del tablero que se desea armar

Returns:
    Un tablero donde muestra las minas y los valores de las casillas tal cual estaban guardadas en el archivo, pero
    respetando el formato de estado["tablero"]
    '''
    
    lista_fila: list[int] = []
    lista_tablero: list[list[int]] = []
    global valores
    
    for linea in tablero:
        
        # En caso de haber algún elemento inválido, devuelve una lista vacía que luego dará error
        if cantidad_elementos_validos_fila_tablero(linea) == -1: return []
        
        for i in range(len(linea)):
            
            # Ignora los "1" después de un "-"
            if i != 0 and linea[i-1] == "-" and linea[i] == "1": continue
            
            # Coloca un "-1" si en el archivo aparece un "-"
            if linea[i] == "-": lista_fila.append(-1)
            
            # Coloca el elemento actual en la lista
            elif linea[i] in valores: lista_fila.append(int(linea[i]))
            
                
        if lista_fila != []: lista_tablero.append(lista_fila)
                
        lista_fila = []
        
        
    return lista_tablero    

def crear_tablero_visible(tablero_visible: list[str]) -> list[list[Any]]:
    '''
    CREAR UN TABLERO VISIBLE DESDE UNA LISTA PROVENIENTE DE UN ARCHIVO

Args:
    tablero_visible: Una lista de strings, que sale de archivo_como_lista(), en la que cada string representa los valores
        que debe tener una fila del tablero visible que se desea armar

Returns:
    Un tablero visible donde muestra las banderas y los vacios guardados en el archivo, teniendo en cuenta
    que "*" se reemplazará por BANDERA, y "?" por VACIO
    '''

    lista_fila: list[int] = []
    lista_tablero: list[list[int]] = []
    global valores
    
    for linea in tablero_visible:
        
        # En caso de haber algún elemento inválido, devuelve una lista vacía que luego dará error
        if cantidad_elementos_validos_fila_visible(linea) == -1: return []
        
        for i in range(len(linea)):
                        
            if linea[i] in valores: lista_fila.append(linea[i])
            elif linea[i] == "?": lista_fila.append(VACIO)
            elif linea[i] == "*" : lista_fila.append(BANDERA)
                
        if lista_fila != []: lista_tablero.append(lista_fila)
                
        lista_fila = []
        
    return lista_tablero

def crear_estado_desde_archivo(tablero: list[str], tablero_visible: list[str]) -> EstadoJuego:
    '''
    CREA UN NUEVO ESTADO CON EL TABLERO DE CREAR_TABLERO() Y EL TABLERO VISIBLE DE CREAR_TABLERO_VISIBLE()

Args:
    tablero: Una lista de strings, que sale de archivo_como_lista(), en la que cada string representa los valores
            que debe tener una fila del tablero que se desea armar
    tablero_visible: Una lista de strings, que sale de archivo_como_lista(), en la que cada string representa los valores
                    que debe tener una fila del tablero visible que se desea armar
        
Returns:
    Un diccionario que contiene la cantidad de filas, de columnas y de minas que hay en el tablero, un booleano que determina
    que el juego no está terminado, y el tablero y el tablero visible tal como lo rearmaron las funciones crear_tablero()
    y crear_tablero_visible()   . 
    '''   
    
    estado: EstadoJuego = {
            "filas" : 0,
            "columnas" : 0,
            "minas" : 0,
            "juego_terminado" : False,
            "tablero" : crear_tablero(tablero),
            "tablero_visible": crear_tablero_visible(tablero_visible)    
        }
        
    estado["filas"] = len(estado["tablero"])
    
    # Si el tablero y el tablero visible tienen al menos una fila:
    if len(estado["tablero"]) > 0 and len(estado["tablero_visible"]) > 0: estado["columnas"] = len(estado["tablero"][0])
    
    estado["minas"] = contar_minas(estado)
    
    return estado
    
def contar_minas(estado: EstadoJuego) -> int:
    '''
    CUENTA LA CANTIDAD DE MINAS QUE TIENE UN TABLERO
    
Args:    
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    La cantidad de bombas que hay en el tablero
    '''
    contador: int = 0
    
    for fila in estado["tablero"]:
        for elemento in fila:
            if elemento == -1: contador += 1
            
    return contador




