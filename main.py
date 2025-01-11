import pygame
import random
pygame.init()

SCREEN = pygame.display.set_mode((720, 640))
SCREEN_CENTER_X = SCREEN.get_width()//2
SCREEN_CENTER_Y = SCREEN.get_height()//2
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
FONT = pygame.font.SysFont('impact', 100)
VEL = 10
MAX_SPEED = 15


class Paddle:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN.get_height() - 20
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.dx = VEL
        self.score = 0
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Ball:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.dx = random.randrange(-100, 100) * .001
        self.dy = random.randrange(0, 100) * .001
        self.center = self.rect.width//2 + self.x, self.rect.height//2 + self.y
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.center = self.rect.width//2 + self.x, self.rect.height//2 + self.y        

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.color = color

def movePaddle(p1):
    mouse_move = pygame.mouse.get_rel()
    if mouse_move[0] > 0:
        p1.x += p1.dx
        p1.update()
    if mouse_move[0] < 0:
        p1.x -= p1.dx
        p1.update()

def moveBall(ball):
    if ball.x > SCREEN.get_width() - ball.rect.width or ball.x < 0:
        ball.dx *= -1
        if abs(ball.dx) > MAX_SPEED and ball.dx < 0:
            ball.dx = -MAX_SPEED
        elif abs(ball.dx) > MAX_SPEED:
            ball.dx = MAX_SPEED
        ball.x += ball.dx
        ball.update()
    if ball.y < 0 or ball.y > SCREEN.get_height() - ball.rect.height:
        ball.dy *= -1
        if abs(ball.dy) > MAX_SPEED and ball.dy < 0:
            ball.dy = -MAX_SPEED
        elif abs(ball.dy) > MAX_SPEED:
            ball.dy = MAX_SPEED
        ball.y += ball.dy
        ball.update()
    else:
        ball.x += ball.dx
        ball.y += ball.dy
        ball.update()

def createBricks():
    bricks = []
    for i in range(10):
        for j in range(3):
            brick = Brick( i * 70 + 20, j * 30 + 150, WHITE )
            bricks.append(brick)
    return bricks

def draw(p1, ball, bricks):
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, p1)
    drawBricks(bricks)
    pygame.draw.rect(SCREEN, WHITE, ball.rect)
    pygame.display.flip()

def drawBricks(bricks):
    for brick in bricks:
        pygame.draw.rect(SCREEN, brick.color, brick.rect)

def handleCollisions(p1, ball, bricks):
    for brick in bricks:
        if brick.rect.collidepoint(ball.center):
            if ball.dy < 0:
                if ball.center[1] > brick.y + brick.rect.height:
                    ball.dx *= -1
                    bricks.remove(brick)
                else:
                    ball.dy *= -1
                    bricks.remove(brick)
            elif ball.dy > 0:
                if ball.center[1] < brick.y:
                    ball.dx *= -1
                    bricks.remove(brick)
                else:
                    ball.dy *= -1
                    bricks.remove(brick)
    if p1.rect.collidepoint(ball.center):
        ball.dy *= -1

def main():
    running = True
    menu = True
    newGame= True
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
            SCREEN.blit(menu_text, (SCREEN_CENTER_X - menu_text.get_width()//2, SCREEN_CENTER_Y - menu_text.get_height()//2))
            pygame.display.flip()
            continue
        if newGame:
            bricks = createBricks()
            newGame = False
        movePaddle(p1)
        moveBall(ball)
        draw(p1, ball, bricks)
        handleCollisions(p1, ball, bricks)
    pygame.quit()

if __name__ == '__main__':
    main()