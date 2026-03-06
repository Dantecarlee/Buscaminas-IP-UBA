# Buscaminas - Introducción a la Programación (FCEN, UBA)

Group project for the course Introducción a la Programación, Licenciatura en Ciencias de Datos, FCEN - UBA.

## What it is

A fully functional Minesweeper game in Python with a graphical interface, save/load support, and a unit test suite.

## How to run

**Requirements:** Python 3.x and tkinter

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows (via Chocolatey)
choco install python-tk
```

```bash
python interfaz_buscaminas.py
```

## Project structure

- `buscaminas.py` — core game logic: board generation, cell discovery (flood fill), win/loss detection, and save/load with file validation
- `interfaz_buscaminas.py` — graphical interface built with tkinter *(base structure provided by the course)*
- `test_propios.py` — unit tests using `unittest`, covering board generation, adjacent mine calculation, edge cases, and save/load integrity

## Features

- 8x8 board with 10 mines (default)
- Left click to reveal, right click to flag
- Save and load game state to/from `.txt` files
- Validates loaded files for consistency before accepting them

## Authors

- Dante Carletti
- Joaquín Callao
- German Altierifue realizado con fines académicos en el marco de la Licenciatura en Ciencia de Datos (UBA).*
