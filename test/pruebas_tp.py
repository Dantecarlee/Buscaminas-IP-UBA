'''
ruta_directorio = "trabajo\\test"

archivo = open(f"{ruta_directorio}\\tablero.txt", "w", encoding="UTF-8")

lineas = ["hola", "aguante", "el tendon de tatum"]

for linea in lineas:
    archivo.write(f"{linea} \n")

print(type(archivo))

archivo.close()'''



archivo = open(f"trabajo\\test\\pruebas.txt", "r", encoding="UTF-8")

leer = archivo.readlines()

print(leer)

caracteres_validos = ["0","1","2","3","4","5","6","7","8"]

def count_if(linea: list) -> int:
    contador = 0
    global caracteres_validos
    
    for elemento in linea:
        if elemento in caracteres_validos: contador += 1
    
    return contador
    
    
for linea in leer:
    print(count_if(linea))
    

archivo.close()