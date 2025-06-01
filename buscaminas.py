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



# -- FUNCION: COLOCAR_MINAS() ---------------------------------------------------------------------------------

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    
    lista_resultado = []
    lista_minas = elegir_bombas(filas,columnas,minas)
    
    for i in range(filas):
        
        lista_fila = []        
        for j in range(columnas):
                        
            if [i,j] in lista_minas: lista_fila.append(-1)
                
            else: lista_fila.append(0)
            
        lista_resultado.append(lista_fila)
        
    if es_matriz(lista_resultado): return  lista_resultado
        
    else: print("ERROR")   
    
    
def elegir_bombas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    
    i = 0
    lista_minas = []
    
    while i < minas:
        mina_fila = random.randint(0,filas-1)
        mina_col = random.randint(0, columnas-1)
        
        coordenada_mina = [mina_fila,mina_col]
        
        if coordenada_mina not in lista_minas:
            lista_minas.append(coordenada_mina)
            i += 1
            
    return lista_minas



# -- ES_MATRIZ() ----------------------------------------

def es_matriz(matriz: list[list[int]]) -> bool:
    
    largo = len(matriz[0])
    if largo == 0: return False
    
    for lista in matriz:
        if len(lista) != largo: return False
        
    return True
     
            


# -- FUNCION: CALCULAR_NUMEROS() ---------------------------------------------------------------------------------

def calcular_numeros(tablero: list[list[int]]) -> None:
    largo_fila = len(tablero[0])
    
    for fila in range(len(tablero)):
        for col in range(largo_fila):
            
            if tablero[fila][col] == 0:                         
                tablero[fila][col] = calcular_minas(tablero, [fila,col])
            
    return tablero


def calcular_minas(tablero: list[list[int]], coordenada: list[int]) -> int:
    res = 0
    cant_filas = len(tablero)
    cant_col = len(tablero[0])
        
    for i in range((coordenada[0])-1,(coordenada[0])+2):
        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            if i >= 0 and j >= 0 and i < cant_filas and j < cant_col:
                if [i,j] != coordenada and tablero[i][j] == -1 : 
                    res += 1   
                
    return res 
  

        

# -- FUNCION: CREAR_JUEGO() ---------------------------------------------------------------------------------

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:   
    estado: EstadoJuego = {
        "filas" : filas,
        "columnas" : columnas,
        "minas" : minas,
        "juego_terminado" : False,
        "tablero" : calcular_numeros((colocar_minas(filas,columnas,minas))),
        "tablero_visible": tablero_vacio(filas,columnas)       
    }
    
    if estado_valido(estado): return estado
    

# -- CREAR_TABLERO_VACIO() ----------------------------------------

def tablero_vacio(filas: int, columnas: int) -> list[list[int]]:
    tablero = []
    for i in range(filas):
        listas = []
        for j in range(columnas):
            listas.append(VACIO)
        
        tablero.append(listas) 
        
    return tablero



# -- ESTADOS_VALIDOS() ----------------------------------------

def estado_valido(estado: EstadoJuego) -> bool:
    if estructura_y_tipos_validos(estado):
        if contar_minas(estado) == estado["minas"]:
            if estado["tablero"] == calcular_numeros(estado["tablero"]):
                if ((todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) or hay_bomba_en_tablero(estado["tablero_visible"])) and estado["juego_terminado"] == True) or estado["juego_terminado"] == False:
                    if verificar_posicion_bombas(estado["tablero"], estado["tablero_visible"]):
                        if verificar_posicion_no_bombas(estado["tablero"], estado["tablero_visible"]): return True
                        
    return False





# -- ESTRUCTURAS_Y_TIPOS_VALIDOS() ----------------------------------------

def estructura_y_tipos_validos(estado: EstadoJuego) -> bool:
         
    if validar_filas(estado) and validar_columnas(estado) and validar_minas(estado) and validar_tablero(estado) and validar_tablero_visible(estado) and cantidad_keys(estado) and son_matriz_misma_dimension(estado["tablero"], estado["tablero_visible"]): return True          
    else: return False
    
    

# -- VALIRDA_ALGO() ----------------------------------------

def validar_filas(estado: EstadoJuego) -> bool:
    if estado["filas"] > 0: return True
    else: return False
    
    
def validar_columnas(estado: EstadoJuego) -> bool:
    if estado["columnas"] > 0: return True
    else: return False


def validar_minas(estado: EstadoJuego) -> bool:
    if estado["minas"] > 0 and estado["minas"] < (estado["filas"]*estado["columnas"]): return True
    else: return False
    
    
def validar_tablero(estado: EstadoJuego) -> bool:
    for lista in estado["tablero"]:
            for i in range(len(lista)):
                elemento = lista[i]
                if -1 > elemento > 8: return False
                
    return True


def validar_tablero_visible(estado: EstadoJuego) -> bool:
    valores = ["0","1","2","3","4","5","6","7","8"]
    for lista in estado["tablero_visible"]:
            for i in range(len(lista)):
                elemento = lista[i]
                if elemento != BOMBA and elemento != VACIO and elemento != BANDERA and elemento not in valores: 
                    return False
              
    return True


def cantidad_keys(estado: EstadoJuego) -> bool:
    if len(estado.keys()) == 6: return True
    else: 
        print(6)
        return False

                        
    

def contar_minas(estado: EstadoJuego) -> int:
    contador = 0
    for fila in estado["tablero"]:
        for elemento in fila:
            if elemento == -1: contador += 1
            
    return contador

                
                    
         
# -- MATRIZ_Y_MISMA_DIMENSION() ----------------------------------------
           
def son_matriz_misma_dimension(tablero: list[list[int]], tablero_visible: list[list[int]]) -> bool:
    
    if es_matriz(tablero) and es_matriz(tablero_visible):
        if len(tablero) == len(tablero_visible):
            if len(tablero[0]) == len(tablero_visible[0]): return True
            
    return False
                
                    
         
# -- TODAS_CELDAS_SEGURAS_DESCUBIERTAS() ----------------------------------------
           
def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[int]]) -> bool:
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero[i][j] == -1:
                if tablero_visible[i][j] != BANDERA and tablero_visible[i][j] != VACIO: return False
                
            elif 0 <= tablero[i][j] <= 8:
                if str(tablero_visible[i][j]) != str(tablero[i][j]):
                    return False
                
    return True
                    
         
# -- HAY_BOMBA_EN_TABLERO() ----------------------------------------
           
def hay_bomba_en_tablero(tablero_visible: list[list[int]]) -> bool:
    
    for lista in tablero_visible:
        for elemento in lista:
            if elemento == BOMBA: return True
    
    return False
                
                    
         
# -- VERIFICAR_POSICION_BOMBAS() ----------------------------------------
           
def verificar_posicion_bombas(tablero: list[list[int]], tablero_visible: list[list[int]]):
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero_visible[i][j] == BOMBA:
                if tablero[i][j] != -1: return False
                
    return True



# -- VERIFICAR_POSICION_NO_BOMBAS() ----------------------------------------
           
def verificar_posicion_no_bombas(tablero: list[list[int]], tablero_visible: list[list[int]]):
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            if tablero_visible[i][j] != BOMBA and tablero_visible[i][j] != BANDERA and tablero_visible[i][j] != VACIO:
                if str(tablero_visible[i][j]) != str(tablero[i][j]): return False
                
    return True



def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    res = estado["tablero_visible"]
    return res


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    
    if estado["juego_terminado"] == False:    
        for i in range(fila+1):
            for j in range(columna+1):
                if [i,j] == [fila,columna]:
                    if estado["tablero_visible"][i][j] == VACIO: 
                        estado["tablero_visible"][i][j] = BANDERA
                    
                    elif estado["tablero_visible"][i][j] == BANDERA: 
                        estado["tablero_visible"][i][j] = VACIO
                    
                    else: estado["tablero_visible"][i][j] = estado["tablero_visible"][i][j]
    
    if estado_valido(estado) == False: print("ERROR")
                





# -- DESCUBRIR_CELDA() -------------------------------------------------------------------------

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:        
    verificar_si_perdiste(estado,fila,columna)
    if estado["juego_terminado"] == False:      
        caminos = caminos_descubiertos(estado["tablero"], estado["tablero_visible"], fila,columna)
        for i in range(estado["filas"]):
            for j in range(estado["columnas"]):
                if (i,j) in caminos:
                    estado["tablero_visible"][i][j] = str(estado["tablero"][i][j])
                     
    if verificar_victoria(estado): estado["juego_terminado"] = True     
    if estado_valido(estado) == False: print("ERROR estado no valido")


# -- CAMINOS_DESCUBIERTOS() -------------------------------------------------------------------------

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    if tablero[fila][columna] > 0:
        return celda_es_numero(tablero, tablero_visible, fila, columna)
    
    else: return celda_es_cero(tablero, tablero_visible, fila, columna)
        


# -- CELDA_ES_NUMERO() ------------------------------------------

def celda_es_numero(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    return [(fila,columna)]
    


# -- CELDA_ES_CERO() ------------------------------------------

celdas_descubiertas = []
    
def celda_es_cero(tablero: list[list[int]], tablero_visible: list[list[int]], fila: int, columna: int) -> list[tuple[int,int]]:
    coordenada: list[int] = [fila,columna]   
    
    global celdas_descubiertas
    celdas_descubiertas.append((fila,columna))
            
    for i in range((coordenada[0])-1,(coordenada[0])+2):        
        for j in range((coordenada[1])-1,(coordenada[1])+2):
            
            if i >= 0 and j >= 0 and i < (len(tablero[0])) and j < (len(tablero)):
                if tablero[i][j] == 0 and (i,j) not in celdas_descubiertas:
                    celda_es_cero(tablero, tablero_visible, i, j)
                    
                else: celdas_descubiertas.append((i,j))
                        
    return celdas_descubiertas
   
    
def verificar_si_perdiste(estado: EstadoJuego, fila: int, columna: int):
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
    global celdas_descubiertas
    celdas_descubiertas = []
    estado["tablero"] = estado2["tablero"]
    estado["tablero_visible"] = estado2["tablero_visible"]
    estado["juego_terminado"] = estado2["juego_terminado"]
    
    if estado_valido(estado) == False: print("ERROR")



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

ruta_directorio = "trabajo"


def contar_numeros_fila(linea: list) -> int:
    contador = 0
    global caracteres_validos    
    for elemento in linea:
        if elemento in caracteres_validos: contador += 1    
    return contador
    
    
def archivo_como_lista(ruta_directorio, archivo) -> list[str]:
    archivo = open(f"{ruta_directorio}\\{archivo}", "r", encoding="UTF-8")
    lista_archivo = archivo.readlines()
    archivo.close()
    return lista_archivo



def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    
    largo_col = len(estado["tablero"])
    largo_fila = len(estado["tablero"][0])
    
    
    if existe_archivo(ruta_directorio, "tablero.txt") and existe_archivo(ruta_directorio, "tablero_visible.txt"):
        
        tablero = archivo_como_lista(ruta_directorio, "tablero.txt")
        tablero_visible = archivo_como_lista(ruta_directorio, "tablero.txt")
        
        for i in range(largo_col):            
                if contar_numeros_fila(tablero[i]) == largo_fila:
                    
                    for j in range(largo_fila):pass        
                

    return False

def numeros_correctos(tablero: list[list[int]]):
    
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            
            coordenada = [i,j]
            contador_bombas = 0
            if tablero[i][j] != -1:
                for k in range((coordenada[0])-1,(coordenada[0])+2):        
                    for l in range((coordenada[1])-1,(coordenada[1])+2):
                
                        if k >= 0 and l >= 0 and k < (len(tablero[0])) and l < (len(tablero)):
                            if tablero[k][l] == -1: contador_bombas += 1
            
                if contador_bombas != tablero[i][j]: return False
    
    return True
            
            
            
estado = {
        "filas" : 2,
        "columnas" : 2,
        "minas" : 1,
        "juego_terminado" : False,
        "tablero" : [
        [-1, 1],
        [1, 1]
    ],
        "tablero_visible": [
        [VACIO, VACIO],
        [VACIO, VACIO]
    ]
    }

print(numeros_correctos(estado["tablero"]))







