import unittest
import os
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, cambio_de_una_posicion, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)


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
        
        # Testeamos que la cantidad de minas en el tablero sea la correcta
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        
        
    def test_una_sola_fila(self):
        filas = 1
        columnas = 3
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        
        # Testeamos que la cantidad de minas en el tablero sea la correcta
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
    def test_muchas_minas(self):
        filas = 4
        columnas = 1
        minas = 3
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        
        # Testeamos que el tablero tenga solo bombas o ceros        
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        
        # Testeamos que la cantidad de minas en el tablero sea la correcta
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        
    def test_matriz_valida(self):
        filas = 5
        columnas = 4
        minas = 5
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        
        # Testeamos que el tablero tenga la cantidad de filas correcta
        self.assertEqual(len(tablero), filas)
        
        # Testeamos que todas las filas del tablero tengan la misma cantidad de elementos
        for i in range(len(tablero)):
            self.assertEqual(len(tablero[i]), columnas)
            
        # Testeamos que la cantidad de minas en el tablero sea la correcta
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        
        
             
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

        

class obtener_estado_tablero_visibleTest(unittest.TestCase):
    def test_tablero_no_vacio_con_cambio(self):
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
        
        copia_tablero_visible = obtener_estado_tablero_visible(estado)
        copia_tablero_visible[0][0] = "Cambio"
        
        # Testeamos que la copia del estado del tablero sea el esperado
        self.assertEqual(copia_tablero_visible,[
            ["Cambio",BANDERA,"1","0"],
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
        
        
        
        
    def test_tablero_vacio_sin_cambio(self):
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



class marcar_celdaTest(unittest.TestCase):
    
    
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
    
    
    def test_marcar_celda_descubierta(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, 1],
                [VACIO, 1]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 1)
        
        # Testeamos que no se modificó el tablero visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, 1],
            [VACIO, 1]
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
            [BOMBA, VACIO, VACIO]
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

    def test_descubrir_con_juego_terminado(self):
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
                ["1", "1", "0"],
                [VACIO, "2", "0"],
                [BANDERA, "2", "0"]
            ],
            'juego_terminado': True
        }
        descubrir_celda(estado, 1, 0)
        
        # Testeamos que no se modificó nada
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [
            [1, 1, 0],
            [-1, 2, 0],
            [-1, 2, 0]
        ])
        self.assertEqual(estado['tablero_visible'], [
                ["1", "1", "0"],
                [VACIO, "2", "0"],
                [BANDERA, "2", "0"]
            ])
        
        # Testeamos que el juego esté terminado
        self.assertTrue(estado['juego_terminado'])
        
        

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
            'juego_terminado': True
        }
        
        # Testeamos que haya ganado
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
        self.assertTrue(estado['juego_terminado'])
        
        
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
        
        # Testeamos que no haya ganado
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
            [VACIO, "1", "0"],
            [VACIO, "1", "0"]
        ])
        self.assertFalse(estado['juego_terminado'])
        
        
        
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
            [ 1, 1]])
        
    def test_reiniciar_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1,1],
                        [1,1]],
            'tablero_visible': [[BOMBA,"1"],
                                ["1","1"]],
            'juego_terminado': True
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
            [ 1, 1]])    

# Hacemos test particulares para esta función porque al ejecutar la funcion que la llama
# (reiniciar_juego), existe la posibilidad de que cambio_de_una_posición no se utilice.
class cambio_de_una_posicionTest(unittest.TestCase):
    def test_cambio_posicion(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        nuevo_estado = cambio_de_una_posicion(estado)
        
        # Testeamos que la posicion (0,0) haya sido intercambiada por la (0,1)
        self.assertEqual(nuevo_estado["tablero"], [
                [1, -1],
                [ 1, 1]
            ])
        
        # Testeamos que el resto no se modifica
        self.assertEqual(nuevo_estado["filas"], 2)
        self.assertEqual(nuevo_estado["columnas"], 2)
        self.assertEqual(nuevo_estado["minas"], 1)
        
        # Testeamos que el tablero visible no cambie (de eso se encarga la funcion Reiniciar Juego)
        self.assertEqual(nuevo_estado["tablero_visible"], [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ])
        
        
    def test_bombas_juntas(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 4,
            'minas': 3,
            'tablero': [
                [-1, -1,-1,1],
                [ 2, 3, 2, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        nuevo_estado = cambio_de_una_posicion(estado)
        
        # Testeamos que la posicion (0,0) haya sido intercambiada por la (0,3)
        # Testeamos que el resto del tablero tenga los numeros correspondientes
        self.assertEqual(nuevo_estado["tablero"], [
                [1, -1,-1,-1],
                [ 1, 2, 3, 2]
            ])
        
        # Testeamos que el resto no se modifica
        self.assertEqual(nuevo_estado["filas"], 2)
        self.assertEqual(nuevo_estado["columnas"], 4)
        self.assertEqual(nuevo_estado["minas"], 3)
        
        # Testeamos que el tablero visible no cambie (de eso se encarga la funcion Reiniciar Juego)
        self.assertEqual(nuevo_estado["tablero_visible"], [
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO]
            ])
        
        
    
    def test_fila_de_bombas(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 4,
            'minas': 4,
            'tablero': [
                [-1, -1,-1,-1],
                [ 2, 3, 3, 2]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        nuevo_estado = cambio_de_una_posicion(estado)
        
        # Testeamos que la posicion (0,0) haya sido intercambiada por la (0,3)
        # Testeamos que el resto del tablero tenga los numeros correspondientes
        self.assertEqual(nuevo_estado["tablero"], [
                [2, -1,-1,-1],
                [ -1, 3, 3, 2]
            ])
        
        # Testeamos que el resto no se modifica
        self.assertEqual(nuevo_estado["filas"], 2)
        self.assertEqual(nuevo_estado["columnas"], 4)
        self.assertEqual(nuevo_estado["minas"], 4)
        
        # Testeamos que el tablero visible no cambie (de eso se encarga la funcion Reiniciar Juego)
        self.assertEqual(nuevo_estado["tablero_visible"], [
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO]
            ])
        
        
        
    def test_bomba_ultima_posicion(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, 1],
                [ 1, -1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        
        nuevo_estado = cambio_de_una_posicion(estado)
        
        # Testeamos que la posicion (0,0) haya sido intercambiada por la (0,1)
        self.assertEqual(nuevo_estado["tablero"], [
                [-1, 1],
                [ 1, 1]
            ])
        
        # Testeamos que el resto no se modifica
        self.assertEqual(nuevo_estado["filas"], 2)
        self.assertEqual(nuevo_estado["columnas"], 2)
        self.assertEqual(nuevo_estado["minas"], 1)
        
        # Testeamos que el tablero visible no cambie (de eso se encarga la funcion Reiniciar Juego)
        self.assertEqual(nuevo_estado["tablero_visible"], [
                [VACIO, VACIO],
                [VACIO, VACIO]
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
        ruta_tablero = os.path.join("test_guardar_estado", "test_estado_iniciado", "tablero.txt")
        ruta_tablero_visible = os.path.join("test_guardar_estado", "test_estado_iniciado", "tablero_visible.txt")
        
        valores = ["0","1","2","3","4","5","6","7","8","-"] 
        
        #Guardamos el estado en el archivo
        guardar_estado(estado, ruta_directorio)
        
        # Para tablero.txt
        
        archivo = open(ruta_tablero, "r", encoding="UTF-8")
        lista_archivo = archivo.readlines()
        archivo.close()
                
        for i in range(len(estado['tablero'])):
            j = 0
            k = 0
            
        # Recorremos el tablero y el contenido del archivo a la vez, para ir comparando los valores
            while j < len(lista_archivo[i]) and k < len(estado['tablero'][0]): 
                
                while lista_archivo[i][j] not in valores:   #Para verificar que no es una coma
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
        
        archivo = open(ruta_tablero_visible, "r", encoding="UTF-8")
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
                
                
        # Testeamos que el resto del estado no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'],2)
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
       
                
    def test_estado_no_iniciado(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
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
        ruta_tablero = os.path.join("test_guardar_estado", "test_estado_no_iniciado", "tablero.txt")
        ruta_tablero_visible = os.path.join("test_guardar_estado", "test_estado_no_iniciado", "tablero_visible.txt")
        
        valores = ["0","1","2","3","4","5","6","7","8","-"] 
        
        #Guardamos el estado en el archivo
        guardar_estado(estado, ruta_directorio)
        
        # Para tablero.txt
        archivo = open(ruta_tablero, "r", encoding="UTF-8")
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
        
        archivo = open(ruta_tablero_visible, "r", encoding="UTF-8")
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
        
        
        # Testeamos que el resto del estado no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'],3)
        self.assertEqual(estado['tablero'], [
                [1, 2, -1],
                [-1, 3, 1],
                [-1, 2, 0]
            ])
        self.assertEqual(estado['tablero_visible'], [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ])
        self.assertFalse(estado['juego_terminado'])



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
        
        # Cargar el estado guardado en "test_juego_iniciado\\tablero.txt y tablero_visible.txt"
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
        
    
    def test_tablero_comas_de_mas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_comas_de_mas")
        
        # Cargar el estado guardado en "test_comas_de_mas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
        
    
    def test_visible_comas_de_mas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_comas_de_mas")
        
        # Cargar el estado guardado en "test_comas_de_mas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
        
        
    def test_tablero_dimensiones_distintas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_dimensiones_distintas")
        
        # Cargar el estado guardado en "test_dimensiones_distintas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
            
    def test_tablero_dimensiones_erroneas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_dimensiones_erroneas")
        
        # Cargar el estado guardado en "test_tablero_dimensiones_erroneas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
        
    def test_visible_dimensiones_erroneas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_dimensiones_erroneas")
        
        # Cargar el estado guardado en "test_visible_dimensiones_erroneas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
      
    def test_solo_bombas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_solo_bombas")
        
        # Cargar el estado guardado en "test_solo_bombas\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    

    def test_archivos_vacios(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_archivos_vacios")
        
        # Cargar el estado guardado en "test_archivos_vacios\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
    
    def test_tablero_elemento_incorrecto(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_elemento_incorrecto")
        
        # Cargar el estado guardado en "test_elementos_incorrectos\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)   
       
    
    def test_visible_elemento_incorrecto(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_elemento_incorrecto")
        
        # Cargar el estado guardado en "test_elementos_incorrectos\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)   
        
        
    def test_tablero_numero_erroneo(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_numero_erroneo")
        
        # Cargar el estado guardado en "test_numeros_erroneos\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
           
    def test_visible_numero_erroneo(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_numero_erroneo")
        
        # Cargar el estado guardado en "test_visible_numero_erroneo\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado)
    
    
    def test_tablero_coma_al_final(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_coma_al_final")
        
        # Cargar el estado guardado en "test_comas_al_final\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado) 
        
    
    def test_visible_coma_al_final(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_coma_al_final")
        
        # Cargar el estado guardado en "test_comas_al_final\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado) 
        
    
    def test_tablero_coma_al_principio(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_tablero_coma_al_principio")
        
        # Cargar el estado guardado en "test_comas_al_final\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado) 
      
    
    def test_visible_coma_al_principio(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_visible_coma_al_principio")
        
        # Cargar el estado guardado en "test_comas_al_final\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado) 
       
    
    def test_archivos_sin_bombas(self):
        
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
        
            
        ruta_directorio = os.path.join("test_cargar_estado", "test_archivos_sin_bomba")
        
        # Cargar el estado guardado en "test_archivos_sin_bomba\\tablero.txt y tablero_visible.txt"
        resultado = cargar_estado(estado, ruta_directorio)
        
        # Verificar que la carga fue incorrecta
        self.assertFalse(resultado) 
        
     
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
