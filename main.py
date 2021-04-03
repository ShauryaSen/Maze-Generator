import pygame
import math
import random

### CONSTANTS
FPS = 5
w = 50

# COLORS
WHITE = (255, 255, 255)
LIGHT_GREEN = (186, 208, 114)
DARK_GREEN = (110, 154, 68)

# WINDOW
WIN_WIDTH = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
pygame.display.set_caption("Snake Game")
COLS = math.floor(WIN_WIDTH / w)
ROWS = math.floor(WIN_WIDTH / w)


## functions
def index(x, y):
    if x < 0 or y < 0 or x * w >= WIN_WIDTH or y * w >= WIN_WIDTH:
        return 0
    
    return x + y * COLS


def draw_frame(current):
    # Draw a rectangle where the current cell is
    x = current.x * w
    y = current.y * w
    pygame.draw.rect(WIN, DARK_GREEN, pygame.Rect(x + 1, y + 1, w - 2, w - 2))
    pygame.display.update()
    pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(x + 1, y + 1, w - 2, w - 2))


def remove_line(last_cell, current, direction):
    cur_x = current.x * w
    cur_y = current.y * w
    last_x = last_cell.x * w
    last_y = last_cell.y * w

    print(cur_x, cur_y, last_x, last_y)

    if direction == "top":
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(cur_x + 1, cur_y + 1, w - 2, (w - 2) * 2))
    elif direction == "right":
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(last_x + 1, last_y + 1, (w - 2) * 2, w - 2))
    elif direction == "bottom":
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(last_x + 1, last_y + 1, w - 2, (w  - 2) * 2))
    elif direction == "left":
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(cur_x + 1, cur_y + 1, (w - 2) * 2, w - 2))



# Cell class
class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        x = self.x * w
        y = self.y * w

        # Draw the cell's lines
        pygame.draw.line(WIN, WHITE, (x, y), (x + w, y))
        pygame.draw.line(WIN, WHITE, (x + w - 1, y - 1), (x + w - 1, y + w - 1))
        pygame.draw.line(WIN, WHITE, (x - 1, y + w - 1), (x + w - 1, y + w - 1))
        pygame.draw.line(WIN, WHITE, (x, y), (x, y + w ))
            
    def pick_next(self, current, grid, visited):
        neighbors = []
        direction = []
        x = self.x
        y = self.y

        top = grid[index(x, y - 1)]
        right = grid[index(x + 1, y)]
        bottom = grid[index(x, y + 1)]
        left = grid[index(x - 1, y)]

        if top not in visited and top != 0:
            neighbors.append(top)
            direction.append("top")
        if right not in visited and right != 0:
            neighbors.append(right)
            direction.append("right")
        if bottom not in visited and bottom != 0:
            neighbors.append(bottom)
            direction.append("bottom")
        if left not in visited and left != 0:
            neighbors.append(left)
            direction.append("left")

        # now pick a random one from the neihbors
        if len(neighbors) == 0:
            return -1, "none"
        else:
            random_num = random.randint(0, len(neighbors) - 1)
            return neighbors[random_num], direction[random_num]

        

## Main
def main():
    # create the grid of cell objects
    grid = []
    for y in range(ROWS):
        for x in range(COLS):
            grid.append(cell(x, y))
    
    for box in grid:
        box.show()

    visited = []
    current = grid[0]
    remove_wall = False

    # Main loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # what happens each frame
        visited.append(current)
        draw_frame(current)

        next_cell, direction = current.pick_next(current, grid, visited)
        last_cell = current

        if  next_cell == -1:
            print("we done now?")
        else:
            current = next_cell
            remove_line(last_cell, current, direction)
        
    

if __name__ == "__main__":
    main()