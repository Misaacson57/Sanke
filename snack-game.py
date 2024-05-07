import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((600, 400))

# Define colors
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game mode and initial setup
game_mode = 'Normal'
snake = [(300, 200)]
direction = 'UP'
speed = 5
segment_size = 20
score = 0
food = []

def get_random_food_position():
    """Generate a random position for new food on the screen, ensuring it doesn't spawn on the snake."""
    x = random.randint(0, (600 // segment_size) - 1) * segment_size
    y = random.randint(0, (400 // segment_size) - 1) * segment_size
    while (x, y) in snake:
        x = random.randint(0, (600 // segment_size) - 1) * segment_size
        y = random.randint(0, (400 // segment_size) - 1) * segment_size
    return (x, y)

def start_screen():
    """Display the start screen and allow the player to choose a game mode."""
    global game_mode
    screen.fill(LIGHT_BLUE)
    font = pygame.font.Font(None, 36)
    options = ["Normal (Press N)", "Impossible (Press I)"]
    y_pos = 100
    for option in options:
        text = font.render(option, True, WHITE)
        screen.blit(text, (150, y_pos))
        y_pos += 100
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    game_mode = 'Normal'
                    return
                elif event.key == pygame.K_i:
                    game_mode = 'Impossible'
                    return

def adjust_game_speed():
    """Adjust the speed of the game based on the selected game mode."""
    global speed
    if game_mode == 'Normal':
        speed = 5
    elif game_mode == 'Impossible':
        speed = 15

def game_over():
    """Display the game over screen and ask the player if they want to restart or quit."""
    screen.fill(LIGHT_BLUE)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Try Again? Your Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(300, 150))
    screen.blit(text, text_rect)
    retry_text = font.render("Press Y to Restart or N to Quit", True, WHITE)
    retry_rect = retry_text.get_rect(center=(300, 250))
    screen.blit(retry_text, retry_rect)
    pygame.display.update()
    wait_for_input()

def wait_for_input():
    """Wait for the player's input on the game over screen."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    restart_game()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def restart_game():
    """Restart the game by resetting the game state."""
    global snake, direction, speed, score, food
    snake = [(300, 200)]
    direction = 'UP'
    speed = 5 if game_mode == 'Normal' else 15
    score = 0
    food = get_random_food_position()
    main()

def handle_keys():
    """Handle key presses to update the direction of the snake."""
    global direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    elif keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    elif keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'

def move_snake():
    """Update the position of the snake, check for collisions, and handle food consumption."""
    global snake, food, speed, score
    x, y = snake[0]
    if direction == 'UP':
        y -= segment_size
    elif direction == 'DOWN':
        y += segment_size
    elif direction == 'LEFT':
        x -= segment_size
    elif direction == 'RIGHT':
        x += segment_size

    new_head = (x, y)

    # Boundary collision check
    if x < 0 or x >= 600 or y < 0 or y >= 400:
        game_over()
        return

    # Check for self-collision excluding the scenario of eating (new head = old food)
    if new_head in snake and new_head != food:
        game_over()
        return

    # Food consumption and growth handling
    if new_head == food:
        food = get_random_food_position()
        score += 100
        if game_mode == 'Impossible':
            # In Impossible mode, grow by five segments
            additional_segments = [new_head] * 5  # Create a list of new heads
            snake = additional_segments + snake  # Prepend multiple heads
        else:
            # Normal growth
            snake.insert(0, new_head)  # Insert new head at the front
        if game_mode != 'Impossible':
            speed += 1
    else:
        snake.insert(0, new_head)  # Insert new head at the front
        snake.pop()  # Remove the last segment to maintain the same length

    # Spawn new food if necessary
    if new_head == food:
        while food in snake:
            food = get_random_food_position()  # Ensure food is not spawned inside the snake

    # Refresh the game display
    screen.fill(LIGHT_BLUE)
    pygame.draw.rect(screen, WHITE, pygame.Rect(food[0], food[1], segment_size, segment_size))
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], segment_size, segment_size))
    pygame.display.flip()

def main():
    """Main game loop."""
    global food
    adjust_game_speed()
    food = get_random_food_position()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_keys()
        move_snake()

        screen.fill(LIGHT_BLUE)
        pygame.draw.rect(screen, WHITE, pygame.Rect(food[0], food[1], segment_size, segment_size))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], segment_size, segment_size))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == '__main__':
    start_screen()
    main()
