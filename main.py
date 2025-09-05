import pygame
import sys

# Game settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 30
PADDLE_SPEED = 14
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
BALL_SPEED_INCREMENT = 1.05  # Speed multiplier after each bounce

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

# Paddles and ball
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y
score_left = 0
score_right = 0
font = pygame.font.SysFont(None, 48)

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, left_paddle)
    pygame.draw.rect(screen, RED, right_paddle)
    pygame.draw.ellipse(screen, YELLOW, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.flip()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    # Reset to initial speed and reverse direction
    ball_speed_x = BALL_SPEED_X * (-1 if ball_speed_x > 0 else 1)
    ball_speed_y = BALL_SPEED_Y * (-1 if ball_speed_y > 0 else 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        # Left paddle: W/S for up/down, A/D for left/right
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_a] and left_paddle.left > 0:
            left_paddle.x -= PADDLE_SPEED
        if keys[pygame.K_d] and left_paddle.right < WIDTH//2:
            left_paddle.x += PADDLE_SPEED
        # Right paddle: Up/Down for up/down, Left/Right for left/right
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED
        if keys[pygame.K_LEFT] and right_paddle.left > WIDTH//2:
            right_paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and right_paddle.right < WIDTH:
            right_paddle.x += PADDLE_SPEED


    # Ball movement
    ball.x += int(ball_speed_x)
    ball.y += int(ball_speed_y)

    # Collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        ball_speed_y *= BALL_SPEED_INCREMENT
        ball_speed_x *= BALL_SPEED_INCREMENT

    # Collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        ball_speed_x *= BALL_SPEED_INCREMENT
        ball_speed_y *= BALL_SPEED_INCREMENT

    # Score
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

    draw()
    clock.tick(60)
