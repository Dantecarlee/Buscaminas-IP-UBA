import unittest
import os
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible, es_matriz,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, estado_valido, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)


def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True



class colocar_minasTest(unittest.TestCase):
    def test_tablero_cuadrado(self):
        filas = 5
        columnas = 5
        minas = 5
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        
    def test_una_sola_fila(self):
        filas = 1
        columnas = 3
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
    def test_muchas_minas(self):
        filas = 4
        columnas = 1
        minas = 3
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        
        
        
class es_matrizTest(unittest.TestCase):
    def test_matriz_vacia(self):
        #Verifica que una lista vacía no es una matriz
        self.assertFalse(es_matriz([[]]))
        
    def test_matriz_irregular(self):
        #Verifica que un tablero con filas de diferente tamaño no es una matriz
        self.assertFalse(es_matriz([[1], [1,2]]))
        
    def test_matriz_valida(self):
        #Verifica que un tablero con filas de igual tamaño es una matriz
        self.assertTrue(es_matriz([[1,2], [3,4]]))
        
             
class calcular_numerosTest(unittest.TestCase):
    def test_dos_bombas(self):
        tablero = [[0,-1,-1],
                    [0,0,0],
                    [0,0,0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1,-1],
                                    [1,2,2],
                                    [0,0,0]])
        
    def test_numero_rodeado_bombas(self):
        tablero = [[-1,-1,-1,-1],
                    [-1,0,-1,-1]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[-1,-1,-1,-1],
                                    [-1,5,-1,-1]])
        
    def test_tablero_solo_bombas(self):
        tablero = [[-1,-1],
                   [-1,-1]]
        
        calcular_numeros(tablero)
        # Testeamos que el tablero no tenga cambios
        self.assertEqual(tablero, [[-1,-1],
                                 [-1,-1]])


class crear_juegoTest(unittest.TestCase):
    def test_tablero_chico(self):
        filas = 2
        columnas = 2
        minas = 2
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
        
    def test_tablero_grande(self):
        filas = 10
        columnas = 13
        minas = 43
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
        
        
    def test_tablero_lleno_de_bombas(self):
        filas = 3
        columnas = 3
        minas = 8
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
   
    
class estado_validoTest(unittest.TestCase):
    def test_estado_valido(self):
        
        #Definimos un estado válido
        estado: EstadoJuego = {
        "filas" : 3,
        "columnas" : 4,
        "minas" : 3,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1,0],
                     [2,2,2,1],
                     [0,0,1,-1]],
        "tablero_visible":[[BANDERA,BANDERA,"1","0"],
                           [VACIO,VACIO,"2","1"],
                           [VACIO,VACIO,VACIO,VACIO]]}     
    
        #Testeamos que el estado sea válido
        self.assertTrue(estado_valido(estado))
        
        
    def test_estado_con_filas_erroneas(self):
        
        #Definimos un estado inválido ya que la cantidad de filas que debe tener no corresponde al tablero
        estado: EstadoJuego = {
        "filas" : 4,
        "columnas" : 4,
        "minas" : 3,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1,0],
                     [2,2,2,1],
                     [0,0,1,-1]],
        "tablero_visible":[[BANDERA,BANDERA,"1","0"],
                           [VACIO,VACIO,"2","1"],
                           [VACIO,VACIO,VACIO,VACIO]]}     
    
        #Testeamos que el estado no sea válido
        self.assertFalse(estado_valido(estado))
        
        
    def test_estado_con_columnas_erroneas(self):
        
        #Definimos un estado inválido ya que la cantidad de columnas que debe tener no corresponde al tablero
        estado: EstadoJuego = {
        "filas" : 3,
        "columnas" : 5,
        "minas" : 3,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1,0],
                     [2,2,2,1],
                     [0,0,1,-1]],
        "tablero_visible":[[BANDERA,BANDERA,"1","0"],
                           [VACIO,VACIO,"2","1"],
                           [VACIO,VACIO,VACIO,VACIO]]}     
    
        #Testeamos que el estado no sea válido
        self.assertFalse(estado_valido(estado))
    
    def test_estado_error_en_estructura_y_tipos_de_datos(self):
        
        #Definimos un estado inválido ya que el tablero tiene dimensiones erróneas
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1],
                     [2,2,1,1]],
        "tablero_visible":[[BANDERA,BANDERA,"1"],
                           [VACIO,VACIO,"1", VACIO]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))
    
    
    def test_estado_error_en_cantidad_de_minas(self):
        
        #Definimos un estado inválido ya que posee más minas de las que declara
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,2],
                     [3,-1,2]],
        "tablero_visible":[[BANDERA,BANDERA,"2"],
                           [VACIO,VACIO,"2"]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))
            
               
    def test_estado_error_numero_incorrecto(self):
        
        #Definimos un estado inválido ya que el tablero tiene una celda cuyo número es erroneo
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1],
                     [2,3,1]],
        "tablero_visible":[[BANDERA,BANDERA,"1"],
                           [VACIO,VACIO,"1"]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))           
    
    
    def test_estado_con_bomba_y_juego_no_terminado(self):
        
        #Definimos un estado inválido ya que hay una bomba en el tablero, pero marca que el juego no está terminado
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1],
                     [2,2,1]],
        "tablero_visible":[[BANDERA,BOMBA,"1"],
                           [VACIO,VACIO,"1"]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))  
               
    
    def test_estado_con_bomba_en_celda_segura(self):
        
        #Definimos un estado inválido ya que hay una bomba en el tablero, donde debería haber una celda segura
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : True,
        "tablero" : [[-1,-1,1],
                     [2,2,1]],
        "tablero_visible":[[BANDERA,VACIO,"1"],
                           [VACIO,VACIO,BOMBA]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))    
        
        
    def test_estado_numero_en_lugar_de_bomba(self):
        
        #Definimos un estado inválido ya que hay un número en el lugar donde debería haber una bomba
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : True,
        "tablero" : [[-1,-1,1],
                     [2,2,1]],
        "tablero_visible":[[BANDERA,"1","1"],
                           [VACIO,VACIO,"1"]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))   
               

    def test_estado_tablero_visible_invalido(self):
        
        #Definimos un estado inválido ya que el tablero visible tiene un número de tipo "int"
        estado: EstadoJuego = {
        "filas" : 2,
        "columnas" : 3,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1],
                     [2,2,1]],
        "tablero_visible":[[BANDERA,BANDERA,"1"],
                           [VACIO,VACIO,1]]}     
    
        #Testeamos que el estado sea inválido
        self.assertFalse(estado_valido(estado))
        
    def test_estado_con_minas_negativas(self):
        estado: EstadoJuego = {
            "filas": 2,
            "columnas": 3,
            "minas": -1,
            "juego_terminado": False,
            "tablero": [[-1,1,0], [1,1,0]],
            "tablero_visible": [[VACIO,VACIO,VACIO], [VACIO,VACIO,VACIO]]
        }
        self.assertFalse(estado_valido(estado))
        

        
class marcar_celdaTest(unittest.TestCase):
    def test_marcar_celda(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_desmarcar_celda(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [-1, 1,0],
                [1, 1,0]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, BANDERA]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 1, 1)
        # Testeamos que la celda se desmarque y todo el resto se quede igual
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1, 0],
            [1, 1, 0]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        
    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BOMBA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True   
        }
        marcar_celda(estado, 1, 1)
        
        # Testeamos que no haya cambios en el tablero visible
        self.assertEqual(estado['tablero_visible'], [
            [BOMBA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertTrue(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        


class descubrir_celdaTest(unittest.TestCase):
    def test_descubrir_un_cero(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [1, 1, 0],
                [-1, 2, 0],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1", "0"],
            [VACIO, "2", "0"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertFalse(estado['juego_terminado'])
        
    def test_descubrir_bomba(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [1, 1, 0],
                [-1, 2, 0],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 1, 0)
        
        # Testeamos que la celda descubierta sea una bomba
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [BOMBA, VACIO, VACIO],
            [VACIO, VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        # Testeamos que el juego esté terminado
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertTrue(estado['juego_terminado'])
        
        
    def test_descubrir_celda_ganadora(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [1, 1, 0],
                [-1, 2, 0],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, "1", "0"],
                [BANDERA, "2", "0"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        
        # Testeamos que la celda descubierta tenga el valor que debe tener
        self.assertEqual(estado['tablero_visible'], [
            ["1", "1", "0"],
            [BANDERA, "2", "0"],
            [BANDERA, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        # Testeamos que el juego esté terminado
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertTrue(estado['juego_terminado'])
        
        
    def test_descubrir_celda_con_bandera(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [1, 1, 0],
                [-1, 2, 0],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, "1", "0"],
                [BANDERA, "2", "0"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 1, 0)
        
        # Testeamos que el tablero visible no se modifique
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1", "0"],
            [BANDERA, "2", "0"],
            [BANDERA, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        # Testeamos que el juego no esté terminado y que sigan existiendo dos bombas
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertFalse(estado['juego_terminado'])
        
    
    def test_descubrir_celda_ya_descubierta(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1,1],[1,1]],
            'tablero_visible': [["1",VACIO],[VACIO,VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        #Testeamos que no haya cambios en el tablero visible
        self.assertEqual(estado['tablero_visible'], [["1",VACIO],[VACIO,VACIO]])


class verificar_victoriaTest(unittest.TestCase):
    def test_juego_ganado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [-1, 1,0],
                [ 1, 1,0]
            ],
            'tablero_visible': [
                [VACIO, "1", "0"],
                ["1", "1", "0"]
            ],
            'juego_terminado': False
        }
        
        # Testeamos que el juego no esté terminado pero que haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1, 0],
            [ 1, 1, 0]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1", "0"],
            ["1", "1", "0"]
        ])
        self.assertFalse(estado['juego_terminado'])
        
        
    def test_juego_no_ganado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [-1, 1,0],
                [ 1, 1,0]
            ],
            'tablero_visible': [
                [VACIO, "1", "0"],
                [VACIO, "1", "0"]
            ],
            'juego_terminado': False
        }
        
        
        
    def test_juego_perdido(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [-1, 1,0],
                [ 1, 1,0]
            ],
            'tablero_visible': [
                [BOMBA, "1", "0"],
                ["1", "1", "0"]
            ],
            'juego_terminado': True
        }
        
        # Testeamos que el juego no esté terminado pero que no haya ganado
        self.assertFalse(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1, 0],
            [ 1, 1, 0]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [BOMBA, "1", "0"],
            ["1", "1", "0"]
        ])
        self.assertTrue(estado['juego_terminado'])
        

class obtener_estado_tableroTest(unittest.TestCase):
    def test_tablero_no_vacio(self):
        estado: EstadoJuego = {
        "filas" : 3,
        "columnas" : 4,
        "minas" : 3,
        "juego_terminado" : False,
        "tablero" : [[-1,-1,1,0],
                     [2,2,2,1],
                     [0,0,1,-1]],
        "tablero_visible":[[BANDERA,BANDERA,"1","0"],
                           [VACIO,VACIO,"2","1"],
                           [VACIO,VACIO,VACIO,VACIO]]}
        
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado),[
            [BANDERA,BANDERA,"1","0"],
            [VACIO,VACIO,"2","1"],
            [VACIO,VACIO,VACIO,VACIO]])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 4)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [-1,-1,1,0],
            [2,2,2,1],
            [0,0,1,-1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA,BANDERA,"1","0"],
            [VACIO,VACIO,"2","1"],
            [VACIO,VACIO,VACIO,VACIO]])
        self.assertFalse(estado['juego_terminado'])
        
    def test_tablero_vacio(self):
        estado: EstadoJuego = {
        "filas" : 3,
        "columnas" : 2,
        "minas" : 2,
        "juego_terminado" : False,
        "tablero" : [[-1,-1],
                     [2,2],
                     [0,0]],
        "tablero_visible":[[VACIO,VACIO],
                           [VACIO,VACIO],
                           [VACIO,VACIO]]}
        
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado),[
            [VACIO,VACIO],
            [VACIO,VACIO],
            [VACIO,VACIO]])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [-1,-1],
            [2,2],
            [0,0]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO,VACIO],
            [VACIO,VACIO],
            [VACIO,VACIO]])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_tablero_cuadrado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        
    def test_reiniciar_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1,1],[1,1]],
            'tablero_visible': [[BOMBA,"1"],["1","1"]],
            'juego_terminado': True
        }
        reiniciar_juego(estado)
        
        #Testeamos que el juego no esté terminado
        self.assertFalse(estado['juego_terminado'])
        #Testeamos que el tablero visible esté totalmente vacío
        self.assertEqual(estado['tablero_visible'], [[VACIO,VACIO],[VACIO,VACIO]])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        


class guardar_estadoTest(unittest.TestCase):
    def test_estado_iniciado(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [1, 1, 0],
                [-1, 2, 0],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, "1", "0"],
                [BANDERA, "2", "0"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': False
        }
        
        ruta_directorio = os.path.join("test_guardar_estado", "test_estado_iniciado")
        valores = ["0","1","2","3","4","5","6","7","8","-"] 
        
        #Guardamos el estado en el archivo
        guardar_estado(estado, ruta_directorio)
        
        # Para tablero.txt
        archivo = open(f"{ruta_directorio}\\tablero.txt", "r", encoding="UTF-8")
        lista_archivo = archivo.readlines()
        archivo.close()
                
        for i in range(len(estado['tablero'])):
            j = 0
            k = 0
            while j < len(lista_archivo[i]) and k < len(estado['tablero'][0]):
                while lista_archivo[i][j] not in valores:
                    j += 1
                
                if lista_archivo[i][j] == "-":
                    j += 1
                    #Testeamos que si en el archivo hay un "-", en el tablero debe haber un "-1"
                    self.assertEqual(estado['tablero'][i][k], -1)
                                        
                else: 
                    #Testeamos que el número que aparece en el, archivo coincida con el de el ablero en esa misma coordenada
                    self.assertEqual(int(lista_archivo[i][j]), estado['tablero'][i][k])
                
                j += 1
                k += 1
       
                
    def test_estado_no_iniciado(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero': [
                [1, 2, -1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        ruta_directorio = os.path.join("test_guardar_estado", "test_estado_no_iniciado")
        valores = ["0","1","2","3","4","5","6","7","8","-"] 
        
        #Guardamos el estado en el archivo
        guardar_estado(estado, ruta_directorio)
        
        # Para tablero.txt
        archivo = open(f"{ruta_directorio}\\tablero.txt", "r", encoding="UTF-8")
        lista_archivo = archivo.readlines()
        archivo.close()
                
        for i in range(len(estado['tablero'])):
            j = 0
            k = 0
            while j < len(lista_archivo[i]) and k < len(estado['tablero'][0]):
                while lista_archivo[i][j] not in valores:
                    j += 1
                
                if lista_archivo[i][j] == "-":
                    j += 1
                    #Testeamos que si en el archivo hay un "-", en el tablero debe haber un "-1"
                    self.assertEqual(estado['tablero'][i][k], -1)
                                        
                else: 
                    #Testeamos que el número que aparece en el, archivo coincida con el de el ablero en esa misma coordenada
                    self.assertEqual(int(lista_archivo[i][j]), estado['tablero'][i][k])
                
                j += 1
                k += 1
        
        
        # Para tablero_visible.txt
        
        archivo = open(f"{ruta_directorio}\\tablero_visible.txt", "r", encoding="UTF-8")
        lista_archivo = archivo.readlines()
        archivo.close()
                
        for i in range(len(estado['tablero_visible'])):
            j = 0
            k = 0
            while j < len(lista_archivo[i]) and k < len(estado['tablero_visible'][0]):
                while lista_archivo[i][j] == ",":
                    j += 1
                
                if lista_archivo[i][j] == "*":
                    #Testeamos que si hay un "*" en archivo, en la misma coordenada de tablero visible haya una BANDERA
                    self.assertEqual(estado['tablero_visible'][i][k], BANDERA)
                    
                elif lista_archivo[i][j] == "?":
                    #Testeamos que si hay un "?" en archivo, en la misma coordenada de tablero visible haya una BOMBA
                    self.assertEqual(estado['tablero_visible'][i][k], VACIO)
                                        
                else: 
                    #Testeamos que el número que aparece en el archivo coincida con el del tablero en esa misma coordenada
                    self.assertEqual((lista_archivo[i][j]), estado['tablero_visible'][i][k])
                
                j += 1
                k += 1
        

class cargar_estadoTest(unittest.TestCase):
    
    def test_cargar_juego_iniciado(self):
        
        #Definimos un estado trivial que será sobreescrito por el estado cargado
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_juego_iniciado")
        
        # Cargar el estado guardado en "test_estado_valido\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue correcta
        self.assertTrue(resultado)
        
        # Verificar que los datos se cargaron correctamente
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1", "0"],
            [BANDERA, "2", "0"],
            [BANDERA, "2", "0"]
        ])
        self.assertFalse(estado['juego_terminado'])
        
    
    def test_cargar_juego_no_iniciado(self):
        
        #Definimos un estado trivial que será sobreescrito por el estado cargado
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1],
                [0, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                ["1", "1"],
                ["0", "0"]
            ],
            'juego_terminado': False
        }
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_juego_no_iniciado")
        
        # Cargar el estado guardado en "test_estado_valido\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue correcta
        self.assertTrue(resultado)
        
        # Verificar que los datos se cargaron correctamente
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 5)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0, 1, 1],
            [-1, 2, 0, 1, -1],
            [-1, 2, 0, 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO, VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])
        
        
    def test_cargar_estado_archivos_no_existen(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        # Intentar cargar desde un directorio sin archivos
        ruta_invalida = "directorio_inexistente"
        resultado = cargar_estado(estado, ruta_invalida)
        
        # Verificar que la carga falló
        self.assertFalse(resultado)
        
        # Verificar que el estado no fue modificado
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])




"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

if __name__ == '__main__':
    unittest.main(verbosity=2)
