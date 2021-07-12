# I was originally going to add search algorithims to solve the maze after it is generated but it wouldn't be that good because the mazes that are generated have long hallways and not a lot of turns so it isn't really a good visualization for search algorithims you can see the remnants me starting this here but i was too lazy to really change it back so the code is really bad


import pygame
import math
import random
pygame.init()

### CONSTANTS
FPS = 100
w = 25

# COLORS
WHITE = (255, 255, 255)
LIGHT_GREEN = (186, 208, 114)
DARK_GREEN = (110, 154, 68)
GRAY = (250, 250, 250)
BLACK = (0, 0, 0)
MAD_LIGHT_GREEN = (80, 220, 100)
BLUE = (102, 191, 191)
DARKER_BLUE = (80, 169, 169)
RED = (238, 41, 57)
GREENY = (243,244,237)

# WINDOW
PADDING = 150
WIN_WIDTH = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH + PADDING))
WIN.fill(GRAY)
pygame.display.set_caption("Maze Generator")
COLS = math.floor(WIN_WIDTH / w)
ROWS = math.floor(WIN_WIDTH / w)


## functions
def index(x, y):
    if x < 0 or y < 0 or x * w >= WIN_WIDTH or (y * w) + PADDING >= WIN_WIDTH + PADDING:
        return 0
    
    return x + y * COLS


def draw_frame(current):
    # Draw a rectangle where the current cell is
    x = current.x * w
    y = (current.y * w) + PADDING
    pygame.draw.rect(WIN, DARK_GREEN, pygame.Rect(x + 1, y + 1, w - 2, w - 2))
    pygame.display.update()
    pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(x + 1, y + 1, w - 2, w - 2))


def remove_line(last_cell, current, direction):
    
    cur_x = current.x * w
    cur_y = (current.y * w) + PADDING
    last_x = last_cell.x * w
    last_y = (last_cell.y * w) + PADDING

    #print(cur_x, cur_y, last_x, last_y)

    if direction == "top":
        current.walls[2] = False
        last_cell.walls[0] = False
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(cur_x + 1, cur_y + 1, w - 2, (w - 2) * 2))
    elif direction == "right":
        current.walls[3] = False
        last_cell.walls[1] = False
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(last_x + 1, last_y + 1, (w - 2) * 2, w - 2))
    elif direction == "bottom":
        current.walls[0] = False
        last_cell.walls[2] = False
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(last_x + 1, last_y + 1, w - 2, (w  - 2) * 2))
    elif direction == "left":
        current.walls[1] = False
        last_cell.walls[3] = False
        pygame.draw.rect(WIN, LIGHT_GREEN, pygame.Rect(cur_x + 1, cur_y + 1, (w - 2) * 2, w - 2))
    

# Cell class
class cell:

    # define what walls the cell has
    #       top   right bottom left
    walls = [True, True, True, True]

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        x = self.x * w
        y = (self.y * w) + PADDING

        # Draw the cell's lines
        
        # top
        pygame.draw.line(WIN, BLACK, (x, y), (x + w, y))
        # right
        pygame.draw.line(WIN, BLACK, (x + w - 1, y - 1), (x + w - 1, y + w - 1))
        # bottom
        pygame.draw.line(WIN, BLACK, (x - 1, y + w - 1), (x + w - 1, y + w - 1))
        # left
        pygame.draw.line(WIN, BLACK, (x, y), (x, y + w ))
            
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

# Button Class
class start_button:
    def __init__(self, color, x, y, width, height, font, font_size, text=""):
       self.color = color
       self.x = x
       self.y = y
       self.width = width
       self.height = height
       self.font = font
       self.font_size = font_size
       self.text = text

    def draw(self, WIN, outline_color=None):
        if outline_color:
            pygame.draw.rect(WIN, outline_color, (self.x - 2, self.y - 2, self.width + 4, self.hieght + 4), 0)
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            WIN.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, coords):
        if coords[0] > self.x and coords[0] < self.x + self.width:
            if coords[1] > self.y and coords[1] < self.y + self.height:
                return True 

    def __str__(self):
        return self.text
# Stuff related to finding the solution

        

## Main
def main():
    # create the grid of cell objects
    grid = []
    for y in range(ROWS):
        for x in range(COLS):
            grid.append(cell(x, y))
    #make the grid
    for box in grid:
        box.show()
    #color in the padding
    pygame.draw.rect(WIN, GREENY, pygame.Rect(0,0, WIN_WIDTH, PADDING))

    # PHASE 1 (choosing algorithim) #
    # color, x, y, width, height, font, font_size, text=""
    start = start_button(BLUE, (WIN_WIDTH / 3 * 2) - (WIN_WIDTH / 3 / 2) - 120, PADDING / 2 - 40, 240, 80, "comicsans", 60, "START")

    
    clock = pygame.time.Clock()
    phase_1 = True

    # PHASE ONE LOOPS
    while phase_1:
        start.draw(WIN)
        pygame.display.update()

        # events    
        for event in pygame.event.get():
            coords = pygame.mouse.get_pos()
        
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if start.isOver(coords):
                        print("clicked the button")
                        start.color = MAD_LIGHT_GREEN
                        # Make it green
                        start.draw(WIN)
                        pygame.display.update()

                        phase_1 = False

            if phase_1 != False:
                if event.type == pygame.MOUSEMOTION:
                        if start.isOver(coords):
                            start.color = DARKER_BLUE
                        else:
                            start.color = BLUE

    # PHASE 2 (maze generation) #

    visited = []
    stack = []
    current = grid[0]
    remove_wall = False

    # PHASE TWO LOOP
    phase_2 = True
    while phase_2:
        clock.tick(FPS)

        # events    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # what happens each frame
        visited.append(current)
        draw_frame(current)
        stack.append(current)

        next_cell, direction = current.pick_next(current, grid, visited)
        last_cell = current

        while next_cell == -1:    
            clock.tick(FPS)
            stack.pop()
            if len(stack) < 1:
                break
            current = stack[len(stack) - 1]
            last_cell = current
            next_cell, direction = current.pick_next(current, grid, visited)
            draw_frame(current)
            #current = last_cell
            
        
        if next_cell != -1:
            current = next_cell
            remove_line(last_cell, current, direction)
        if len(stack) < 1:
            phase_2 = False

    # PHASE 3 (algorithim visualization) # (nvm this didn't end up happening)       



    game_pause = True
    while game_pause == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_pause = False
        
    

if __name__ == "__main__":
    main()