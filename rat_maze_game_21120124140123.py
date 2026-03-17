import pygame
import random
import sys

# CONFIG 
SIZE = 12
CELL = 50
WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL + 120  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rat in Maze 🐭")
big_font = pygame.font.SysFont(None, 42)

# warna
WHITE = (240,240,240)
BLACK = (30,30,30)
BLUE = (100,150,255)
RED = (255,100,100)
GRAY = (200,200,200)
YELLOW = (255,220,0)

clock = pygame.time.Clock()

# MAZE
maze_success = [
[1,1,1,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,0,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0,1,1,1,0],
[0,0,0,0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,0,0,1,1],
[0,0,0,0,0,0,0,0,0,0,0,1],
]

maze_fail = [
[1,1,1,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,0,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,0,1,1,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1],
]

def generate_random():
    maze = [[1 if random.random()>0.3 else 0 for _ in range(SIZE)] for _ in range(SIZE)]
    maze[0][0]=1
    maze[SIZE-1][SIZE-1]=1
    return maze

maze = maze_success
path = [[0]*SIZE for _ in range(SIZE)]

# DRAW 
def draw(rat_pos, status):
    screen.fill(WHITE)

    for i in range(SIZE):
        for j in range(SIZE):
            rect = pygame.Rect(j*CELL, i*CELL, CELL, CELL)

            if maze[i][j] == 0:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)

            if path[i][j] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif path[i][j] == -1:
                pygame.draw.rect(screen, RED, rect)

            pygame.draw.rect(screen, WHITE, rect, 1)

    # CHEESE 
    cheese_x = (SIZE-1)*CELL
    cheese_y = (SIZE-1)*CELL
    pygame.draw.polygon(screen, YELLOW, [
        (cheese_x+5, cheese_y+CELL-5),
        (cheese_x+CELL-5, cheese_y+CELL-5),
        (cheese_x+CELL//2, cheese_y+5)
    ])

    # Rat
    if rat_pos:
        x,y = rat_pos
        cx = y*CELL+CELL//2
        cy = x*CELL+CELL//2

        pygame.draw.circle(screen, (120,70,15), (cx,cy), CELL//3)
        pygame.draw.circle(screen, (150,90,40), (cx-10,cy-10), 8)
        pygame.draw.circle(screen, (150,90,40), (cx+10,cy-10), 8)
        pygame.draw.circle(screen, (0,0,0), (cx+8,cy), 3)

    # BACKGROUND TEXT 
    pygame.draw.rect(screen, (220,220,220), (0, SIZE*CELL, WIDTH, 120))

    # TEXT
    text = big_font.render(status, True, (0,0,0))
    screen.blit(text, (10, SIZE*CELL + 40))

    pygame.display.update()

#  SOLVER 
def valid(x,y):
    return (0<=x<SIZE and 0<=y<SIZE and maze[x][y]==1 and path[x][y]==0)

def solve(mode=""):
    stack=[(0,0)]

    while stack:
        x,y=stack[-1]

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw((x,y), f"{mode} Searching...")

        if (x,y)==(SIZE-1,SIZE-1):
            path[x][y]=1
            draw((x,y), f"{mode} 🐭 Rat found the cheese!")
            pygame.time.delay(1500)
            return True

        if valid(x,y):
            path[x][y]=1

            for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
                nx,ny=x+dx,y+dy
                if valid(nx,ny):
                    stack.append((nx,ny))
                    break
            else:
                path[x][y]=-1
                stack.pop()
        else:
            stack.pop()

        pygame.time.delay(80)

    draw(None, f"{mode} 🐭 Rat cannot find the cheese!")
    pygame.time.delay(1500)
    return False

#  MAIN 
def main():
    global maze, path

    running=True
    status="Press 1:Success  2:Fail  3:Random"

    while running:
        draw(None,status)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    maze=maze_success
                    path=[[0]*SIZE for _ in range(SIZE)]
                    solve("Success Maze -")

                if event.key==pygame.K_2:
                    maze=maze_fail
                    path=[[0]*SIZE for _ in range(SIZE)]
                    solve("Fail Maze -")

                if event.key==pygame.K_3:
                    maze=generate_random()
                    path=[[0]*SIZE for _ in range(SIZE)]
                    solve("Random Maze -")

        clock.tick(60)

    pygame.quit()

if __name__=="__main__":
    main()