import pygame
import time
import random

# Initialize Pygame
pygame.init()

# --- Screen settings ---
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)        # Food color 🍎
GREEN = (0, 255, 0)        # Snake color 🐍
GREY = (169, 169, 169)     # Background color 🟫
YELLOW = (255, 255, 102)


# --- Clock and Font ---
clock = pygame.time.Clock()
snake_speed = 20
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# --- Helper functions ---
def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size, block_size])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    rect = mesg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(mesg, rect)

# --- Main game function ---
def game_loop():
    game_over = False
    game_close = False

    # Snake starting position
    x = WIDTH // 2
    y = HEIGHT // 2

    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:

        while game_close:
            screen.fill(GREY)
            message("Game Over! Womp Womp. Press Q to quit or C to play again.", RED, -20)
            your_score(length_of_snake - 1)
            pygame.display.update()

            # Restart or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Handle key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Move snake
        x += x_change
        y += y_change

        # Wall collision
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(GREY)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Update snake
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        # Food collision
        if x == food_x and y == food_y:
            length_of_snake += 1
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# --- Run the game ---
game_loop()
