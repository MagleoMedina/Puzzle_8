import pygame
import sys
import time
import heapq
import random

pygame.init()
WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle-8")

FONT_TITLE = pygame.font.SysFont(None, 48)
FONT_BUTTON = pygame.font.SysFont(None, 32)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# --- Agrega estas constantes ---
PUZZLE_SIZE = 3
TILE_SIZE = 80
PUZZLE_ORIGIN = (110, 60)  # x, y offset for puzzle drawing

GOAL_STATE = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
# --- Fin de las constantes ---

# Button data: (text, y position)
buttons = [
    ("Agente informado", 140),
    ("Agente no informado", 200),
    ("Cerrar", 260)
]

button_rects = []

def draw_interface():
    SCREEN.fill(WHITE)
    # Draw title
    title_surface = FONT_TITLE.render("Puzzle-8", True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH//2, 70))
    SCREEN.blit(title_surface, title_rect)
    # Draw buttons
    button_rects.clear()
    for idx, (text, y) in enumerate(buttons):
        btn_surface = FONT_BUTTON.render(text, True, BLACK)
        btn_rect = btn_surface.get_rect(center=(WIDTH//2, y))
        pygame.draw.rect(SCREEN, GRAY, btn_rect.inflate(40, 20), border_radius=8)
        SCREEN.blit(btn_surface, btn_rect)
        button_rects.append(btn_rect.inflate(40, 20))

def manhattan(state):
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

def find_zero(state):
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            if state[i][j] == 0:
                return i, j

def neighbors(state):
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
    return tuple(tuple(row) for row in state)

def a_star(start):
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

def get_solution_length(solution):
    if solution is None:
        return 0
    return len(solution) - 1  # Excluye el estado inicial

def is_solvable(state):
    flat = [num for row in state for num in row if num != 0]
    inv = 0
    for i in range(len(flat)):
        for j in range(i+1, len(flat)):
            if flat[i] > flat[j]:
                inv += 1
    return inv % 2 == 0

def random_puzzle():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i*3:(i+1)*3] for i in range(3)]
        if is_solvable(state) and state != GOAL_STATE:
            return state

def draw_puzzle(state):
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

def agente_informado():
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
        # --- Mostrar título encima del puzzle durante la animación ---
        titulo_surface = FONT_BUTTON.render("Busqueda Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        # --- Fin del título ---
        draw_puzzle(state)
        elapsed = time.time() - start_time  # Actualiza el tiempo en cada frame
        # Solo mostrar el tiempo durante la animación
        label_time = FONT_BUTTON.render("Tiempo:", True, BLACK)
        time_surface = FONT_BUTTON.render(f"{elapsed:.2f} s", True, BLACK)
        SCREEN.blit(label_time, (10, 80))
        SCREEN.blit(time_surface, (10, 110))
        pygame.display.flip()
        pygame.time.delay(500)  # 0.5s entre movimientos

    # Al terminar, muestra el tiempo final y los otros valores hasta que el usuario cierre o presione una tecla
    end_time = time.time()
    elapsed = end_time - start_time
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        SCREEN.fill(WHITE)
        # --- Mostrar título encima del puzzle también al finalizar ---
        titulo_surface = FONT_BUTTON.render("Busqueda Informada", True, BLACK)
        titulo_rect = titulo_surface.get_rect(center=(WIDTH // 2, PUZZLE_ORIGIN[1] - 30))
        SCREEN.blit(titulo_surface, titulo_rect)
        # --- Fin del título ---
        draw_puzzle(solution[-1])
        draw_stats(elapsed, expanded_nodes, solution_length)
        pygame.display.flip()

def bfs_count_expanded(start):
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

def agente_no_informado():
    puzzle = random_puzzle()
    start_time = time.time()
    expanded_nodes, solution = bfs_count_expanded(puzzle)
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

    end_time = time.time()
    elapsed = end_time - start_time
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

def main():
    while True:
        draw_interface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button_rects[0].collidepoint(mouse_pos):
                    # Acción para "Agente informado"
                    agente_informado()
                elif button_rects[1].collidepoint(mouse_pos):
                    # Acción para "Agente no informado"
                    agente_no_informado()
                elif button_rects[2].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    main()