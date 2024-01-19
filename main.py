# Conway's Game of Life Source Code
# Press 'g' to populate grid randomly
# Press 'c' to clear grid

import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Use dynamic grid size based on the screen size
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

clock = pygame.time.Clock()


def gen(num):
    all_positions = [(row, col) for row in range(GRID_HEIGHT) for col in range(GRID_WIDTH)]
    random_positions = set()

    while len(random_positions) < min(num, GRID_WIDTH * GRID_HEIGHT):
        random_positions.add(random.choice(all_positions))

    return random_positions



def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors

def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                if event.key == pygame.K_g:
                    max_cells = GRID_WIDTH * GRID_HEIGHT
                    positions = gen(min(random.randrange(4, 10) * GRID_WIDTH, max_cells))

    
        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    main()
    pygame.quit()