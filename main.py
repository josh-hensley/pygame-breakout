import pygame
import random
pygame.init()

SCREEN = pygame.display.set_mode()
SCREEN_CENTER_X = SCREEN.get_width()//2
SCREEN_CENTER_Y = SCREEN.get_height()//2
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
FONT = pygame.font.SysFont('impact', 100)


class Paddle:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN.get_height() - 20
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.score = 0
    def updateRect(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Ball:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.dx = 5
        self.dy = 5
    def updateRect(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.color = color
def movePaddle(p1):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_move = pygame.mouse.get_rel()
            p1.x += mouse_move[0]
            p1.updateRect()

def moveBall(ball):
    pass

def createBricks():
    bricks = []
    for i in SCREEN.get_width()//70:
        for j in SCREEN.get_height()//2 + 20:
            brick = Brick( i, j, WHITE )
            bricks.append(brick)
    return bricks

def draw(p1, ball, bricks):
    SCREEN.fill(BLACK)
    pygame.draw.rect(p1, WHITE)
    drawBricks(bricks)
    pygame.display.update()

def drawBricks(bricks):
    for brick in bricks:
        pygame.draw.rect(SCREEN, brick.color, brick.rect)

def main():
    running = True
    menu = True
    newGame: True
    ball = Ball()
    p1 = Paddle()
    bricks = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and menu:
                menu = False
        if menu:
            menu_text = FONT.render('PRESS ANY BUTTON TO START', 1, WHITE)
            SCREEN.blit(menu_text, (SCREEN_CENTER_X, SCREEN_CENTER_Y))
            continue
        if newGame:
            bricks = createBricks()
            newGame = False
        movePaddle(p1)
        moveBall(ball)
        draw()
    pygame.quit()

if __name__ == '__main__':
    main()