import pygame
import random
pygame.init()

SCREEN = pygame.display.set_mode((720, 640), pygame.SCALED)
pygame.display.set_caption('BRICKOUT')
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
SCREEN_CENTER_X = SCREEN_WIDTH//2
SCREEN_CENTER_Y = SCREEN_HEIGHT//2
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
FONT = pygame.font.SysFont('impact', 50)
PADDLE_SPEED = 8
MAX_VELOCITY = .5
PIP_SFX = pygame.mixer.Sound('Assets/pip.mp3')
WALL_SFX = pygame.mixer.Sound('Assets/wall.mp3')
FUMBLE_SFX = pygame.mixer.Sound('Assets/fumble.mp3')
BG_SFX = pygame.mixer.Sound('Assets/pong_track.mp3')


class Paddle:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.dx = PADDLE_SPEED
        self.score = 0
        self.lives = 3
        self.center = (self.x + self.rect.width//2, self.y + self.rect.height//2)
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.center = (self.x + self.rect.width//2, self.y + self.rect.height//2)

class Ball:
    def __init__(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.dx = random.randrange(-5, 5) * .01
        self.dy = .1
        self.center = (self.rect.width//2 + self.x, self.rect.height//2 + self.y)
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.center = (self.rect.width//2 + self.x, self.rect.height//2 + self.y)
    def reset(self):
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y
        self.dx = random.randrange(-5, 5) * .01
        self.dy = .1
        self.update()

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.color = color
        self.points = 150

def movePaddle(p1):
    mouse_move = pygame.mouse.get_rel()
    if mouse_move[0] > 0 and p1.x + p1.rect.width <= SCREEN_WIDTH:
        p1.x += p1.dx
        p1.update()
    if mouse_move[0] < 0 and p1.x >= 0:
        p1.x -= p1.dx
        p1.update()    

def handleWallCollision(ball, p1):
    if ball.center[0] >= SCREEN_WIDTH or ball.center[0] < 0:
        ball.dx *= -1
        ball.x += ball.dx
        ball.y += ball.dy
        ball.update()
        WALL_SFX.play()
    if ball.center[1] <= 0:
        ball.dy *= -1
        ball.x += ball.dx
        ball.y += ball.dy
        ball.update()
        WALL_SFX.play()
    if ball.center[1] >= SCREEN_HEIGHT:
        FUMBLE_SFX.play()
        pygame.time.delay(1000)
        p1.lives -= 1
        ball.reset()

def handleBrickCollision(ball, bricks, p1):
    for brick in bricks:
        if brick.rect.collidepoint(ball.center):
            if ball.dx < 0:
                if ball.center[0] == brick.rect.left:
                    ball.dx *= -1
                    ball.x += ball.dx
                    ball.y += ball.dy
                    ball.update()
                    bricks.remove(brick)
                    p1.score += brick.points
                    PIP_SFX.play()
                else:
                    ball.dy *= -1
                    ball.x += ball.dx
                    ball.y += ball.dy
                    ball.update()
                    bricks.remove(brick)
                    p1.score += brick.points
                    PIP_SFX.play()
            if ball.dx > 0:
                if ball.center[0] == brick.rect.right:
                    ball.dx *= -1
                    ball.x += ball.dx
                    ball.y += ball.dy
                    ball.update()
                    bricks.remove(brick)
                    p1.score += brick.points
                    PIP_SFX.play()
                else:
                    ball.dy *= -1
                    ball.x += ball.dx
                    ball.y += ball.dy
                    ball.update()
                    bricks.remove(brick)
                    p1.score += brick.points
                    PIP_SFX.play()

def handlePaddleCollision(p1, ball):
    if p1.rect.collidepoint(ball.center):
        if ball.center[0] == p1.center[0]:
            ball.dx = 0
            ball.dy *= -1
            ball.x += ball.dx
            ball.y += ball.dy
            ball.update()
            PIP_SFX.play()
        if ball.center[0] < p1.center[0]:
            ball.dx = ((p1.center[0] - ball.center[0])/p1.rect.width) * MAX_VELOCITY * -1
            ball.dy *= -1
            ball.x += ball.dx
            ball.y += ball.dy
            ball.update()
            PIP_SFX.play()
        if ball.center[0] > p1.center[0]:
            ball.dx = ((ball.center[0] - p1.center[0])/p1.rect.width) * MAX_VELOCITY
            ball.dy *= -1
            ball.x += ball.dx
            ball.y += ball.dy
            ball.update()
            PIP_SFX.play()

def moveAndCollide(p1, ball, bricks):
    movePaddle(p1)
    handleWallCollision(ball, p1)
    handleBrickCollision(ball, bricks, p1)
    handlePaddleCollision(p1, ball)
    ball.x += ball.dx
    ball.y += ball.dy
    ball.update()

def createBricks():
    bricks = []
    for i in range((SCREEN_WIDTH//10) - 1):
        for j in range(3):
            brick = Brick( i * 70 + 20, j * 30 + 150, WHITE )
            bricks.append(brick)
    return bricks

def draw(p1, ball, bricks):
    SCREEN.fill(BLACK)
    score = FONT.render(f'{p1.score}', 1, WHITE)
    lives = FONT.render(f'{p1.lives}', 1, WHITE)
    SCREEN.blit(score, (SCREEN_CENTER_X/2 - score.get_width()/2, 10))
    SCREEN.blit(lives, (SCREEN_WIDTH * 3 / 4 - lives.get_width()/2, 10))
    pygame.draw.rect(SCREEN, WHITE, p1)
    drawBricks(bricks)
    pygame.draw.rect(SCREEN, WHITE, ball.rect)
    pygame.display.flip()

def drawBricks(bricks):
    for brick in bricks:
        pygame.draw.rect(SCREEN, brick.color, brick.rect)

def gameOver(p1):
    SCREEN.fill(BLACK)
    game_over_text = FONT.render(f'YOUR SCORE: {p1.score}', 1, WHITE)
    SCREEN.blit(game_over_text, (SCREEN_CENTER_X - game_over_text.get_width()/2, SCREEN_CENTER_Y - game_over_text.get_height()/2))
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    BG_SFX.play(-1)
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
            SCREEN.fill(BLACK)
            menu_text = FONT.render('PRESS ANY BUTTON TO START', 1, WHITE)
            SCREEN.blit(menu_text, (SCREEN_CENTER_X - menu_text.get_width()//2, SCREEN_CENTER_Y - menu_text.get_height()//2))
            pygame.display.flip()
            continue
        if newGame:
            ball = Ball()
            p1 = Paddle()
            bricks = createBricks()
            newGame = False
        moveAndCollide(p1, ball, bricks)
        draw(p1, ball, bricks)
        if p1.lives == 0:
            gameOver(p1)
            menu = True
            newGame = True
    pygame.quit()

if __name__ == '__main__':
    main()