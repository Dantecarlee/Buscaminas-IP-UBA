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


# La ruta directorio es la carpeta en la que están guardados los archivos
ruta_directorio = "trabajo"

# Lista que contenga los valores de los números que puede tener cada celda pero con tipo "str"
valores = ["0","1","2","3","4","5","6","7","8"] # Luego se usa como global dentro de las funciones

# Lista vacia para ir completando con las cordenadas de las celdas que se van descubriendo
celdas_descubiertas = [] # Luego se usa como global dentro de las funciones


# -- ELIGIR_BOMBAS()

def elegir_bombas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    '''
    ELIJE DE MANERA ALEATORIA LA COORDENADA DE CADA UNA DE LAS MINAS QUE DEBE COLOCAR
    
Args:
    filas: Número mayor a cero que representa la cantidad de filas que tiene un tablero
    columnas: Número mayor a cero que representa la cantidad de columnas que tiene un tablero
    minas: Número mayor a cero que representa la cantidad de minas que tiene un tablero

Returns:
    Un lista con una cantidad de elementos igual a "minas", que contiene listas de dos elementos que representan las coordenadas donde se encuentra cada mina
       
    '''
    
    contador: int = 0
    lista_minas: list[list[int]] = []
    
    while contador < minas:
        mina_fila = random.randint(0,filas-1)
        mina_col = random.randint(0, columnas-1)
        
        coordenada_mina = [mina_fila,mina_col]
        
        if coordenada_mina not in lista_minas:
            lista_minas.append(coordenada_mina)
            contador += 1
            
    return lista_minas



# -- COLOCAR_MINAS( )

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
    lista_minas: list[list[int]] = elegir_bombas(filas,columnas,minas)
    
    for i in range(filas):
        
        lista_fila: list[int] = []
              
        for j in range(columnas):
                        
            if [i,j] in lista_minas: lista_fila.append(-1)
                
            else: lista_fila.append(0)
            
        lista_resultado.append(lista_fila)
        
    if es_matriz(lista_resultado): return  lista_resultado
        



# -- ES_MATRIZ()

def es_matriz(matriz: list[list[int]]) -> bool:
    '''
    VERIFICA QUE TODAS LAS FILAS TENGAN EL MISMO LARGO
    
Args:    
    matriz: Tablero cuyas dimensiones serán evaluadas

Returns:
    True si todas las filas de "matriz" tienen el mismo largo
    '''
    
    largo: int = len(matriz[0])
    if largo == 0: return False
    
    for lista in matriz:
        if len(lista) != largo: return False
        
    return True
     
            

# -- CALCULAR_NUMEROS()

def calcular_numeros(tablero: list[list[int]]) -> None:
    '''
    CALCULA EL NÚMERO QUE DEBE TENER CADA CELDA SEGÚN LO ESPECIFICA CALCULAR_MINAS()
    SOLO MODIFICA EL VALOR DE LA CELDA EN CASO DE QUE LA MISMA NO SEA UNA BOMBA (UN "-1")
    
Args:    
    tablero: Una matriz bidimensional que se irá recorriendo y cuyos valores internos van a ir cambiando según lo que devuelva la función calcular_minas
    '''
    largo_fila: int = len(tablero[0])
    
    for fila in range(len(tablero)):
        for col in range(largo_fila):
            
            if tablero[fila][col] == 0:                         
                tablero[fila][col] = calcular_minas(tablero, [fila,col])
            


# -- CALUCLAR_MINAS()

def calcular_minas(tablero: list[list[int]], coordenada: list[int]) -> int:
    '''
    CALCULA EL NÚMERO QUE DEBE TENER UNA CELDA DE ACUERDO A LA CANTIDAD DE MINAS QUE TIENE EN SUS CELDAS ADYACENTES
    
Args:    
    tablero: Una matriz bidimensional cuyos valores internos son "0" (si no es una bomba) o "-1" (si es una bomba )
    coordenada: Una lista de dos elementos, que demarcan una celda específica, teniendo en cuenta que el primer número corresponde a su fila y el segundo a su columna
    
Returns:
    El número de minas que tiene la coordenada elegida en sus celdas adyacentes
    '''
    res: int = 0
    cant_filas: int = len(tablero)
    cant_col: int = len(tablero[0])
        
    for i in range((coordenada[0])-1,(coordenada[0])+2):
        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            if i >= 0 and j >= 0 and i < cant_filas and j < cant_col:
                if [i,j] != coordenada and tablero[i][j] == -1 : 
                    res += 1   
                
    return res 
  
        

# -- CREAR_JUEGO()

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego: 
    '''
    CREA UN ESTADO CON EL QUE SE VA A JUGAR Y VERIFICA QUE EL MISMO CUMPLA ESTADO_VALIDO()
    
Args:    
    filas: Número mayor a cero que Representa la cantidad de filas que tiene un tablero
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
    
    if estado_valido(estado): return estado
    

    
# -- TABLERO_VACIO()

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



# -- ESTADO_VÁLIDO()

def estado_valido(estado: EstadoJuego) -> bool:
    '''
    VERIFICA QUE UN ESTADO SEA UN ESTADO VÁLIDO, ES DECIR, QUE SE CUMPLA:
        - LA ESTRUCTURA INTERNA Y LOS TIPOS DE DATOS USADOS EN EL ESTADO SON CORRECTOS
        - LA CANTIDAD DE MINAS EN EL TABLERO ES LA CANTIDAD DE MINAS ELEGIDAS PARA EL JUEGO
        - LOS NÚMEROS DEL TABLERO SE CORRESPONDEN A LA CANTIDAD DE MINAS QUE TIENE ESA CELDA A SU ALREDEDOR
        - EL JUEGO ESTÁ TERMINADO SI TODAS LAS CELDAS "NO BOMBA" YA FUERON DESCUBIERTAS
        - EL JUEGO ESTÁ TERMINADO SI EN EL TABLERO VISIBLE HAY UNA BOMBA EXPUESTA 
        - SI HAY UNA BOMBA EN EL TABLERO VISIBLE, ES PORQUE EN ESA COORDENADA EN EL TABLERO HAY UN "-1"
        - SI HAY UN NÚMERO EN EL TABLERO VISIBLE, ES PORQUE EN ESA COORDENADA EN EL TABLERO ESTÁ EL MISMO NÚMERO
    
Args:    
    estado: Diccionario que contiene toda información sobre la partida en juego

Returns:
    True si el estado a evaluar cumple con todas las condiciones mencionadas
    '''
    
    if estructura_y_tipos_validos(estado):
        if contar_minas(estado) == estado["minas"]:
            if numeros_correctos(estado["tablero"]): 
                if ((todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) and estado["juego_terminado"]) or 
                    (hay_bomba_en_tablero(estado["tablero_visible"]) and estado["juego_terminado"]) or 
                    (not (todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"])) and not (hay_bomba_en_tablero(estado["tablero_visible"]) and not (estado["juego_terminado"])))):
                    if verificar_posicion_bombas(estado["tablero"], estado["tablero_visible"]):
                        if verificar_posicion_no_bombas(estado["tablero"], estado["tablero_visible"]): return True
             
    return False


# -- NUMEROS_CORRECTOS()

def numeros_correctos(tablero: list[list[int]]) -> bool:
    '''
    VERIFICA QUE LOS NÚMEROS DE UN TABLERO SEAN LOS QUE CORRESPONDEN SEGÚN LA CANTIDAD DE MINAS A SU ALREDEDOR
    
Args:    
    tablero: Una matriz bidimensional cuyos valores internos son números enteros entre 0 y 8, o "-1" (si es una bomba )

Returns:
    True si cada celda contiene la cantidad exacta de minas que tiene en sus coordenadas adyacentes
    '''
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            coordenada: list[int] = [i,j]
            contador_bombas: int = 0
            
            if tablero[i][j] != -1:
                for k in range((coordenada[0])-1,(coordenada[0])+2):        
                    for l in range((coordenada[1])-1,(coordenada[1])+2):
                        
                        if k >= 0 and l >= 0 and k < (len(tablero)) and l < (len(tablero[0])):
                            if tablero[k][l] == -1: 
                                
                                contador_bombas += 1
            
                if contador_bombas != tablero[i][j]: return False
    
    return True



# -- CONTAR_MINAS()

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



# -- VERIFICA QUE LA ESTRUCTURA DE UN ESTADO SEA CORRECTA AL IGUAL QUE LOS TIPOS DE DATOS EN LOS TABLEROS

def estructura_y_tipos_validos(estado: EstadoJuego) -> bool:   
         
    if validar_filas(estado) and validar_columnas(estado) and validar_minas(estado) and validar_tablero(estado) and validar_tablero_visible(estado) and cantidad_keys(estado) and son_matriz_misma_dimension(estado["tablero"], estado["tablero_visible"]): return True          
    
    else: return False
    
    

# -- VERIFICA QUE LA CANTIDAD DE FILAS, COLUMNAS Y MINAS SEA MAYOR A CERO

def validar_filas(estado: EstadoJuego) -> bool:
    if estado["filas"] > 0:
        contador: int = 0
        for fila in estado["tablero"]:
            contador += 1
        
        if contador == estado["filas"]: return True
        
    return False
    
    
    
def validar_columnas(estado: EstadoJuego) -> bool:
    if estado["columnas"] > 0:
        contador: int = 0
        for columna in estado["tablero"][0]:
            contador += 1
        
        if contador == estado["columnas"]: return True
        
    return False


def validar_minas(estado: EstadoJuego) -> bool:
    if estado["minas"] > 0 and estado["minas"] < (estado["filas"]*estado["columnas"]): return True
    
    
    
# -- VERIFICA QUE LOS TIPOS DE DATOS EN LOS TABLEROS SEAN CORRECTOS    
    
def validar_tablero(estado: EstadoJuego) -> bool:
    for lista in estado["tablero"]:
            for i in range(len(lista)):
                elemento = lista[i]
                if elemento < -1 or elemento > 8: return False

                
    return True


def validar_tablero_visible(estado: EstadoJuego) -> bool:
    global valores
    for lista in estado["tablero_visible"]:
            for i in range(len(lista)):
                elemento = lista[i]
                if elemento != BOMBA and elemento != VACIO and elemento != BANDERA and elemento not in valores: 
                    return False
              
    return True



# -- VERIFICA QUE LA CANTIDAD DE KEYS DE UN ESTADO SEA SEIS

def cantidad_keys(estado: EstadoJuego) -> bool:
    if len(estado.keys()) == 6: return True


       
# -- VERIFICA QUE LA CANTIDAD DE ELEMENTOS POR FILA DE LOS TABLEROS SEAN LA MISMA, Y QUE LA DIMENSIÓN DE LOS TABLEROS TAMBIÉN SEAN IGUALES ENTRE SI
           
def son_matriz_misma_dimension(tablero: list[list[int]], tablero_visible: list[list[int]]) -> bool:
    
    if es_matriz(tablero) and es_matriz(tablero_visible):
        if len(tablero) == len(tablero_visible):
            if len(tablero[0]) == len(tablero_visible[0]): return True
                
                    
         
# -- VERIFICA SI TODAS LAS CELDAS QUE NO SON BOMBAS YA FUERON DESCUBIERTAS
           
def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[int]]) -> bool:
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero[i][j] == -1:
                if tablero_visible[i][j] != BANDERA and tablero_visible[i][j] != VACIO: return False
                
            elif 0 <= tablero[i][j] <= 8:
                if str(tablero_visible[i][j]) != str(tablero[i][j]):
                    return False
                
    return True
                    
         
# -- VERIFICA SI HAY ALGUNA BOMBA VISIBLE EN EL TABLERO
           
def hay_bomba_en_tablero(tablero_visible: list[list[int]]) -> bool:
    
    for lista in tablero_visible:
        for elemento in lista:
            if elemento == BOMBA: return True
    
    return False
                
                    
         
# -- VERIFICA QUE SI EN TABLERO VISIBLE HAY UNA BOMBA, EN LA MISMA COORDENADA EN TABLERO HAY UN "-1"
           
def verificar_posicion_bombas(tablero: list[list[int]], tablero_visible: list[list[int]]):
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero_visible[i][j] == BOMBA:
                if tablero[i][j] != -1: return False
                
    return True



# -- VERIFICA QUE EL VALOR MOSTRADO EN TABLERO VISIBLE DE UNA CELDA DESCUBIERTA ES EL MISMO VALOR QUE TIENE LA CELDA EN TABLERO
           
def verificar_posicion_no_bombas(tablero: list[list[int]], tablero_visible: list[list[int]]):
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero_visible[i][j] != BOMBA and tablero_visible[i][j] != BANDERA and tablero_visible[i][j] != VACIO:
                if str(tablero_visible[i][j]) != str(tablero[i][j]): return False
                
    return True



# -- DADO UN ESTADO, DEVUELVE EL TABLERO VISIBLE

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    res = estado["tablero_visible"]
    return res



# -- COLOCA UNA BANDERA EN EL TABLERO VISIBLE

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    
    if estado["juego_terminado"] == False:    
        for i in range(fila+1):
            for j in range(columna+1):
                if [i,j] == [fila,columna]:
                    if estado["tablero_visible"][i][j] == VACIO: 
                        estado["tablero_visible"][i][j] = BANDERA
                    
                    elif estado["tablero_visible"][i][j] == BANDERA: 
                        estado["tablero_visible"][i][j] = VACIO
    
                



# -- DESCUBRIR_CELDA() -------------------------------------------------------------------------

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if estado["tablero_visible"][fila][columna] == VACIO:
        verificar_si_perdiste(estado,fila,columna)
        if estado["juego_terminado"] == False:  
            global celdas_descubiertas
            celdas_descubiertas = []     
            caminos = caminos_descubiertos(estado["tablero"], estado["tablero_visible"], fila,columna)
            for i in range(estado["filas"]):
                for j in range(estado["columnas"]):
                    if (i,j) in caminos:
                        estado["tablero_visible"][i][j] = str(estado["tablero"][i][j])
                     
    if verificar_victoria(estado): estado["juego_terminado"] = True

# -- CAMINOS_DESCUBIERTOS() -------------------------------------------------------------------------

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    if tablero[fila][columna] > 0:
        return celda_es_numero(tablero, tablero_visible, fila, columna)
    
    else: return celda_es_cero(tablero, tablero_visible, fila, columna)
        


# -- CELDA_ES_NUMERO() ------------------------------------------

def celda_es_numero(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    return [(fila,columna)]
    


# -- CELDA_ES_CERO() ------------------------------------------
    
def celda_es_cero(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    coordenada: list[int] = [fila,columna]   
    
    global celdas_descubiertas
    celdas_descubiertas.append((fila,columna))
            
    for i in range((coordenada[0])-1,(coordenada[0])+2):        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            if i >= 0 and j >= 0 and i < len(tablero) and j < len(tablero[0]):

                if tablero[i][j] == 0 and (i,j) not in celdas_descubiertas:
                    celda_es_cero(tablero, tablero_visible, i, j)
                    
                else: celdas_descubiertas.append((i,j))
                        
    return celdas_descubiertas
   
    
def verificar_si_perdiste(estado: EstadoJuego, fila: int, columna: int) -> None:
    for i in range(fila+1):
            for j in range(columna+1):
                if [i,j] == [fila,columna]:
                    if estado["tablero"][i][j] == -1: 
                        estado["juego_terminado"] = True
                        estado["tablero_visible"][i][j] = BOMBA
                        
                    else: estado["juego_terminado"] = False



def verificar_victoria(estado: EstadoJuego) -> bool:
    if todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]): return True
    else: return False


def reiniciar_juego(estado: EstadoJuego) -> None:
    estado2 = crear_juego(estado["filas"], estado["columnas"], estado["minas"])
    
    while estado["tablero"] == estado2["tablero"]:
         estado2 = crear_juego(estado["filas"], estado["columnas"], estado["minas"])
        
    global celdas_descubiertas
    celdas_descubiertas = []
    print(celdas_descubiertas)
    estado["tablero"] = estado2["tablero"]
    estado["tablero_visible"] = estado2["tablero_visible"]
    estado["juego_terminado"] = estado2["juego_terminado"]
    



def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    
    # -- ESTO ES DE TABLERO.TXT --------------------------------------------------------------
    
    archivo = open(f"{ruta_directorio}\\tablero.txt", "w", encoding="UTF-8")
    
    for i in range(len(estado["tablero"])):
            for j in range(len(estado["tablero"][0])): 
                if j == (len(estado["tablero"][0]))-1: archivo.write(f"{estado["tablero"][i][j]}")                    
                else : archivo.write(f"{estado["tablero"][i][j]},")                
            archivo.write("\n")
    archivo.close()
    
    
    # -- ESTO ES DE TABLERO_VISIBLE.TXT --------------------------------------------------------------
    
    archivo = open(f"{ruta_directorio}\\tablero_visible.txt", "w", encoding="UTF-8")
    
    for i in range(len(estado["tablero_visible"])):
            for j in range(len(estado["tablero_visible"][0])):
                 
                if j == (len(estado["tablero_visible"][0]))-1:
                    archivo.write(f"{clasificar_celda(estado['tablero_visible'][i][j])}")
                                 
                else : 
                    archivo.write(f"{clasificar_celda(estado['tablero_visible'][i][j])},")

            archivo.write("\n")
    archivo.close()

def clasificar_celda(celda: Any):
    if celda == BANDERA: return "*"
    elif celda == VACIO: return "?"
    else: return celda

    
    
def archivo_como_lista(ruta_directorio, archivo) -> list[str]:
    archivo = open(f"{ruta_directorio}\\{archivo}", "r", encoding="UTF-8")
    lista_archivo = archivo.readlines()
    archivo.close()
    return lista_archivo



def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    
    
    if existe_archivo(ruta_directorio, "tablero.txt") and existe_archivo(ruta_directorio, "tablero_visible.txt"):
        tablero = archivo_como_lista(ruta_directorio, "tablero.txt")
        tablero_visible = archivo_como_lista(ruta_directorio, "tablero_visible.txt")
        
        estado_archivo = crear_estado_desde_archivo(tablero, tablero_visible)
        estado["filas"] = estado_archivo["filas"]
        estado["columnas"] = estado_archivo["columnas"]
        estado["minas"] = estado_archivo["minas"]
        estado["juego_terminado"] = estado_archivo["juego_terminado"]
        estado["tablero"] = estado_archivo["tablero"]
        estado["tablero_visible"] = estado_archivo["tablero_visible"]
        
        return True
        
    return False
        
                 
  
  
  
# -- CREAR UN TABLERO DESDE UN ARCHIVO -----------------------------------------------------
          
def crear_tablero(tablero: list[str]) -> list[list[int]]:
    lista_fila = []
    lista_tablero = []
    global valores
    
    for elemento in tablero:
        for i in range(len(elemento)):
            
            if i != 0 and elemento[i-1] == "-": continue
            
            if elemento[i] == "-": lista_fila.append(-1)
            elif elemento[i] in valores: lista_fila.append(int(elemento[i]))
                
        lista_tablero.append(lista_fila)
                
        lista_fila = []
        
    return lista_tablero
        
        
# -- CREAR UN TABLERO VISIBLE DESDE UN ARCHIVO -------------------------------------
def crear_tablero_visible(tablero_visible: list[str]) -> list[list[Any]]:
    lista_fila = []
    lista_tablero = []
    global valores
    
    for elemento in tablero_visible:
        for i in range(len(elemento)):
                        
            if elemento[i] in valores: lista_fila.append(elemento[i])
            elif elemento[i] == "?": lista_fila.append(VACIO)
            elif elemento[i] == "*" : lista_fila.append(BANDERA)
                
        lista_tablero.append(lista_fila)
                
        lista_fila = []
        
    return lista_tablero
        

def crear_estado_desde_archivo(tablero: list[str], tablero_visible: list[str]) -> EstadoJuego:
    
    estado: EstadoJuego = {
        "filas" : 0,
        "columnas" : 0,
        "minas" : 0,
        "juego_terminado" : False,
        "tablero" : crear_tablero(tablero),
        "tablero_visible": crear_tablero_visible(tablero_visible)      
    }
    
    estado["minas"] = contar_minas(estado)
    estado["columnas"] = len(estado["tablero"][0])
    estado["filas"] = len(estado["tablero"])
    
    if estado_valido(estado): return estado
    
    
    





