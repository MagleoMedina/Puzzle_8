import pygame # Para la interfaz gráfica
import sys # Para manejar la interfaz gráfica
import time # Para medir el tiempo de ejecución
import heapq # Para la cola de prioridad
import random # Para generar el puzzle aleatorio
import threading  # Para manejo de hilos

# Inicializa Pygame y la pantalla
pygame.init()
WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle-8")

# Fuentes para los textos
FONT_TITLE = pygame.font.SysFont(None, 48)
FONT_BUTTON = pygame.font.SysFont(None, 32)

# Definición de colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Constantes para el puzzle
PUZZLE_SIZE = 3
TILE_SIZE = 80
PUZZLE_ORIGIN = (110, 60)  # Offset para dibujar el puzzle


GOAL_STATE = [
    [1,2,3],
    [8,0,4],
    [7,6,5]
]
# Datos de los botones: (texto, posición y)
buttons = [
    ("Agente informado", 140),
    ("Agente no informado", 200),
    ("Cerrar", 260)
]

# Lista para almacenar los rectángulos de los botones
button_rects = []

def draw_interface():
    """Dibuja la interfaz principal con el título y los botones."""
    SCREEN.fill(WHITE)
    # Dibuja el título
    title_surface = FONT_TITLE.render("Puzzle-8", True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH//2, 70))
    SCREEN.blit(title_surface, title_rect)
    # Dibuja los botones
    button_rects.clear()
    for idx, (text, y) in enumerate(buttons):
        btn_surface = FONT_BUTTON.render(text, True, BLACK)
        btn_rect = btn_surface.get_rect(center=(WIDTH//2, y))
        pygame.draw.rect(SCREEN, GRAY, btn_rect.inflate(40, 20), border_radius=8)
        SCREEN.blit(btn_surface, btn_rect)
        button_rects.append(btn_rect.inflate(40, 20))

#Inicio

#---Logica del puzzle---
def find_zero(state):
    """Encuentra la posición (i, j) del espacio vacío (0) en el estado."""
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            if state[i][j] == 0:
                return i, j

def neighbors(state):
    """Genera los estados vecinos moviendo el espacio vacío en las 4 direcciones posibles."""
    x, y = find_zero(state)
    moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < PUZZLE_SIZE and 0 <= ny < PUZZLE_SIZE:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves

def state_to_tuple(state):
    """Convierte una matriz de estado a una tupla inmutable para usar en sets."""
    return tuple(tuple(row) for row in state)

def get_solution_length(solution):
    """Devuelve la longitud de la solución (cantidad de movimientos)."""
    if solution is None:
        return 0
    return len(solution) - 1  # Excluye el estado inicial

def is_solvable(state):
    """Verifica si un estado del puzzle es resoluble respecto al GOAL_STATE actual."""
    # Convierte ambos estados a listas planas (ignorando el 0)
    flat_start = [num for row in state for num in row if num != 0]
    flat_goal = [num for row in GOAL_STATE for num in row if num != 0]
    # Crea un mapa de valor -> índice en el estado objetivo
    goal_pos = {val: idx for idx, val in enumerate(flat_goal)}
    # Transforma flat_start a la permutación respecto a flat_goal
    perm = [goal_pos[val] for val in flat_start]
    # Cuenta las inversiones en la permutación
    inv = 0
    for i in range(len(perm)):
        for j in range(i+1, len(perm)):
            if perm[i] > perm[j]:
                inv += 1
    return inv % 2 == 0

def random_puzzle():
    """Genera un puzzle aleatorio y resoluble diferente al objetivo.
    Si el puzzle generado no es resoluble, muestra un mensaje por consola y por la interfaz.
    """
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i*3:(i+1)*3] for i in range(3)]
        if not is_solvable(state):
            print("Puzzle no resoluble: Generando otro...")
            # Mostrar mensaje en la interfaz
            SCREEN.fill(WHITE)
            msg_surface = FONT_BUTTON.render("Puzzle no resoluble: Generando otro...", True, (200, 0, 0))
            msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            SCREEN.blit(msg_surface, msg_rect)
            pygame.display.flip()
            pygame.time.delay(1200)
            print(state)
            continue
        if state != GOAL_STATE:
            print("Puzzle resoluble generado:", state)
            return state
        
def draw_puzzle(state):
    """Dibuja el estado actual del puzzle en pantalla."""
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            val = state[i][j]
            rect = pygame.Rect(PUZZLE_ORIGIN[0]+j*TILE_SIZE, PUZZLE_ORIGIN[1]+i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, GRAY if val != 0 else WHITE, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 2)
            if val != 0:
                num_surface = FONT_BUTTON.render(str(val), True, BLACK)
                num_rect = num_surface.get_rect(center=rect.center)
                SCREEN.blit(num_surface, num_rect)

def draw_stats(elapsed, expanded_nodes, solution_length):
    """Dibuja las estadísticas de la búsqueda en pantalla."""
    label_time = FONT_BUTTON.render("Tiempo", True, BLACK)
    time_surface = FONT_BUTTON.render(f"{elapsed:.2f} s", True, BLACK)
    label_nodes = FONT_BUTTON.render("Nodos", True, BLACK)
    nodes_surface = FONT_BUTTON.render(str(expanded_nodes), True, BLACK)
    label_length = FONT_BUTTON.render("Longitud", True, BLACK)
    length_surface = FONT_BUTTON.render(str(solution_length), True, BLACK)
    SCREEN.blit(label_time, (10, 80))
    SCREEN.blit(time_surface, (10, 110))
    SCREEN.blit(label_nodes, (10, 150))
    SCREEN.blit(nodes_surface, (10, 180))
    SCREEN.blit(label_length, (10, 220))
    SCREEN.blit(length_surface, (10, 250))

#Fin

#Inicio
#---Funciones de búsqueda Informada---
def manhattan(state):
    """Calcula la distancia Manhattan total de un estado al estado objetivo."""
    distance = 0
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            val = state[i][j]
            if val == 0:
                continue
            goal_x = (val - 1) // PUZZLE_SIZE
            goal_y = (val - 1) % PUZZLE_SIZE
            distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def a_star(start):
    """Algoritmo A* para resolver el puzzle usando la heurística de Manhattan."""
    heap = []
    heapq.heappush(heap, (manhattan(start), 0, start, []))
    visited = set()
    while heap:
        f, g, current, path = heapq.heappop(heap)
        if current == GOAL_STATE:
            return path + [current]
        st = state_to_tuple(current)
        if st in visited:
            continue
        visited.add(st)
        for neighbor in neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                heapq.heappush(heap, (g+1+manhattan(neighbor), g+1, neighbor, path + [current]))
    return None

def count_expanded_nodes_a_star(start):
    """Versión de A* que también cuenta los nodos expandidos."""
    heap = []
    heapq.heappush(heap, (manhattan(start), 0, start, []))
    visited = set()
    expanded = 0
    while heap:
        f, g, current, path = heapq.heappop(heap)
        if current == GOAL_STATE:
            return expanded, path + [current]
        st = state_to_tuple(current)
        if st in visited:
            continue
        visited.add(st)
        expanded += 1
        for neighbor in neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                heapq.heappush(heap, (g+1+manhattan(neighbor), g+1, neighbor, path + [current]))
    return expanded, None

#Fin

#Inicio
#---Funciones de búsqueda No Informada---

def bfs_count_expanded(start):
    """Búsqueda en anchura (BFS) que cuenta los nodos expandidos."""
    from collections import deque
    queue = deque()
    queue.append((start, []))
    visited = set()
    expanded = 0
    while queue:
        current, path = queue.popleft()
        if current == GOAL_STATE:
            return expanded, path + [current]
        st = state_to_tuple(current)
        if st in visited:
            continue
        visited.add(st)
        expanded += 1
        for neighbor in neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                queue.append((neighbor, path + [current]))
    return expanded, None

#Fin

#Inicio
#Creacion de los agentes 

def agente_no_informado():
    """Ejecuta la búsqueda no informada (BFS) en un hilo y muestra la animación y estadísticas."""
    puzzle = random_puzzle()
    result = {"expanded_nodes": None, "solution": None}
    finished = threading.Event()

    def worker():
        # Ejecuta la búsqueda BFS y guarda los resultados
        expanded_nodes, solution = bfs_count_expanded(puzzle)
        result["expanded_nodes"] = expanded_nodes
        result["solution"] = solution
        finished.set()

    # Inicia el hilo para la búsqueda BFS
    thread = threading.Thread(target=worker)
    thread.start()
    start_time = time.time()

    # Mostrar pantalla de "calculando..." mientras el hilo trabaja
    while not finished.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill(WHITE)
        titulo_surface = FONT_BUTTON.render("Busqueda No Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        calc_surface = FONT_BUTTON.render("Calculando...", True, DARK_GRAY)
        calc_rect = calc_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(calc_surface, calc_rect)
        pygame.display.flip()
        pygame.time.delay(500)

    expanded_nodes = result["expanded_nodes"]
    solution = result["solution"]
    solution_length = get_solution_length(solution)

    for idx, state in enumerate(solution):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill(WHITE)
        # Título para búsqueda no informada
        titulo_surface = FONT_BUTTON.render("Busqueda No Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        draw_puzzle(state)
        elapsed = time.time() - start_time
        label_time = FONT_BUTTON.render("Tiempo:", True, BLACK)
        time_surface = FONT_BUTTON.render(f"{elapsed:.2f} s", True, BLACK)
        SCREEN.blit(label_time, (10, 80))
        SCREEN.blit(time_surface, (10, 110))
        pygame.display.flip()
        pygame.time.delay(500)
        #pygame.time.delay(0)  # Descomentar para ver el tiempo real de ejecución

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Tiempo de ejecución (no informado): {elapsed:.2f} s")  # Imprime tiempo por consola
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        SCREEN.fill(WHITE)
        titulo_surface = FONT_BUTTON.render("Busqueda No Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        draw_puzzle(solution[-1])
        draw_stats(elapsed, expanded_nodes, solution_length)
        pygame.display.flip()

def agente_informado():
    """Ejecuta la búsqueda informada (A*) y muestra la animación y estadísticas."""
    puzzle = random_puzzle()
    start_time = time.time()
    expanded_nodes, solution = count_expanded_nodes_a_star(puzzle)
    solution_length = get_solution_length(solution)

    for idx, state in enumerate(solution):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill(WHITE)
        # Mostrar título encima del puzzle durante la animación
        titulo_surface = FONT_BUTTON.render("Busqueda Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        draw_puzzle(state)
        elapsed = time.time() - start_time  # Actualiza el tiempo en cada frame
        # Solo mostrar el tiempo durante la animación
        label_time = FONT_BUTTON.render("Tiempo:", True, BLACK)
        time_surface = FONT_BUTTON.render(f"{elapsed:.2f} s", True, BLACK)
        SCREEN.blit(label_time, (10, 80))
        SCREEN.blit(time_surface, (10, 110))
        pygame.display.flip()
        pygame.time.delay(500)  # 0.5s entre movimientos
        #pygame.time.delay(0)  # Descomentar para ver el tiempo real de ejecución

    # Al terminar, muestra el tiempo final y los otros valores hasta que el usuario cierre o presione una tecla
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Tiempo de ejecución (informado): {elapsed:.2f} s")  # Imprime tiempo por consola
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        SCREEN.fill(WHITE)
        # Mostrar título encima del puzzle también al finalizar
        titulo_surface = FONT_BUTTON.render("Busqueda Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        draw_puzzle(solution[-1])
        draw_stats(elapsed, expanded_nodes, solution_length)
        pygame.display.flip()

#Fin

def main():
    """Bucle principal del programa, maneja la interfaz y los eventos."""
    while True:
        draw_interface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button_rects[0].collidepoint(mouse_pos):
                    # LLama a la función para "Agente informado"
                    agente_informado()
                elif button_rects[1].collidepoint(mouse_pos):
                    # LLama a la función para "Agente no informado"
                    agente_no_informado()
                elif button_rects[2].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    main()