# Puzzle-8

Este proyecto implementa el clásico **Puzzle-8** (también conocido como 8-puzzle) con una interfaz gráfica interactiva desarrollada en Python utilizando la librería `pygame`. El objetivo del juego es ordenar los números del 1 al 8 en una cuadrícula de 3x3, dejando el espacio vacío (representado por 0) en la posición central, siguiendo el estado objetivo:

```
1 2 3
8 0 4
7 6 5
```

## Características

- **Interfaz gráfica amigable**: Permite interactuar con el puzzle y visualizar el proceso de resolución.
- **Generación de puzzles aleatorios y resolubles**: El sistema garantiza que cada puzzle generado pueda ser resuelto.
- **Dos modos de resolución automática**:
  - **Agente informado**: Utiliza el algoritmo A* con heurística de distancia Manhattan.
  - **Agente no informado**: Utiliza búsqueda en anchura (BFS).
- **Animación paso a paso**: Visualización de cada movimiento de la solución encontrada.
- **Estadísticas en tiempo real**: Muestra el tiempo de ejecución, nodos expandidos y longitud de la solución.
- **Manejo de hilos**: El agente no informado ejecuta la búsqueda en un hilo separado para mantener la interfaz responsiva.

## Requisitos

- Python 3.7 o superior
- [pygame](https://www.pygame.org/) (instalable vía pip)

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Instala las dependencias necesarias ejecutando:

   ```
   pip install pygame
   ```

## Ejecución

Ubícate en la carpeta del proyecto y ejecuta el archivo principal:

```
python main.py
```

### Ejecutable

Si no deseas ejecutar el código fuente, puedes encontrar el **ejecutable del juego** ya compilado en la carpeta [`dist`](./dist). Simplemente navega a esa carpeta y ejecuta el archivo (solo compatible con windows).

## Uso

Al iniciar el programa, verás una ventana con el título "Puzzle-8" y tres botones:

- **Agente informado**: Resuelve el puzzle usando A* (heurística Manhattan).
- **Agente no informado**: Resuelve el puzzle usando BFS.
- **Cerrar**: Sale de la aplicación.

Haz clic en cualquiera de los dos primeros botones para generar un puzzle aleatorio y observar cómo el agente lo resuelve paso a paso. Al finalizar, se mostrarán estadísticas relevantes.

## Estructura del Código

- `main.py`: Contiene toda la lógica del juego, la interfaz gráfica y la implementación de los algoritmos de búsqueda.
- **Funciones principales**:
  - `random_puzzle()`: Genera un puzzle aleatorio y resoluble.
  - `a_star()`, `count_expanded_nodes_a_star()`: Implementación del algoritmo A*.
  - `bfs_count_expanded()`: Implementación de BFS.
  - `agente_informado()`, `agente_no_informado()`: Controlan la ejecución y visualización de cada agente.
  - `draw_puzzle()`, `draw_stats()`, `draw_interface()`: Dibujo de la interfaz y estadísticas.

## Algoritmos Implementados

### Agente Informado (A*)

- Utiliza la heurística de **distancia Manhattan** para estimar el costo restante hasta el objetivo.
- Expande los nodos de menor costo estimado primero.
- Generalmente encuentra la solución óptima más rápidamente que BFS.

### Agente No Informado (BFS)

- Explora todos los nodos a una profundidad antes de pasar a la siguiente.
- Garantiza encontrar la solución más corta, pero puede ser menos eficiente en tiempo y memoria.

## Personalización

Puedes modificar el estado objetivo (`GOAL_STATE`) o experimentar con otras heurísticas en la función `manhattan()` para observar diferentes comportamientos de los algoritmos.

## Créditos

Desarrollado por [Magleo Medina].


---
