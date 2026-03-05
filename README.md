# Buscaminas - Introducción a la Programación (UBA)

Este repositorio contiene la implementación integral del motor lógico para el juego **Buscaminas**, desarrollada como Trabajo Práctico para la materia *Introducción a la Programación* en la Facultad de Ciencias Exactas y Naturales de la Universidad de Buenos Aires (UBA).

## 🎯 Descripción del Proyecto
El objetivo principal fue diseñar un sistema robusto capaz de gestionar el estado de una partida de Buscaminas, priorizando la eficiencia algorítmica y la integridad de los datos en los procesos de persistencia. 



## 🛠️ Características Técnicas (Backend)
El núcleo del desarrollo se encuentra en `buscaminas.py` y destaca por:

* **Gestión de Estado Centralizada**: Uso de un diccionario (`EstadoJuego`) para el control de dimensiones, minas, visibilidad y condiciones de fin de partida.
* **Algoritmo de Expansión Recursiva**: Implementación de un algoritmo tipo *Flood Fill* para el descubrimiento automático de celdas adyacentes vacías.
* **Persistencia y Validación**: Sistema de guardado y carga de partidas mediante archivos `.txt`. Incluye lógica de validación para garantizar que los tableros cargados sean coherentes y aptos para el juego.
* **Tipado Estático**: Incorporación de `Type Hints` para mejorar la legibilidad y facilitar el mantenimiento del código.

## 🧪 Testing y Calidad
Se incluyó una suite de pruebas unitarias en `test_propios.py` utilizando el framework `unittest`:
* **Casos Borde**: Validación de tableros de dimensiones mínimas ($1 \times n$) y tableros saturados de minas.
* **Integridad Lógica**: Pruebas sobre los algoritmos de cálculo de minas adyacentes y funciones de reinicio de partida.
* **Persistencia**: Verificación de los procesos de escritura y lectura de archivos de estado.

## 🖥️ Interfaz Gráfica (Frontend)
El archivo `interfaz_buscaminas.py` utiliza la librería **Tkinter** para la representación visual del juego.
> **Nota de autoría**: La estructura y diseño de la interfaz gráfica fueron provistos por el equipo docente de la cátedra como base para el trabajo. El desarrollo del grupo se enfocó exclusivamente en el motor lógico, la implementación de algoritmos y la suite de tests.

## 👥 Créditos
- **Dante Carletti**
- **Joaquín Callao**
- **German Altieri**

---
*Este proyecto fue realizado con fines académicos en el marco de la Licenciatura en Ciencia de Datos (UBA).*
