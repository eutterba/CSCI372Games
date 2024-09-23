import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Menu options
def draw_menu():
    screen.fill(WHITE)
    title_text = font.render("pirate's pass", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    start_text = small_font.render("Start", True, BLACK)
    quit_text = small_font.render("Quit", True, BLACK)

    # Draw buttons
    start_button = pygame.Rect(screen_width // 2 - 100, 250, 200, 50)
    quit_button = pygame.Rect(screen_width // 2 - 100, 350, 200, 50)

    pygame.draw.rect(screen, GREEN, start_button)
    pygame.draw.rect(screen, RED, quit_button)

    screen.blit(start_text, (start_button.x + 50, start_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

    return start_button, quit_button

def menu():
    while True:
        start_button, quit_button = draw_menu()
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_button.collidepoint(mouse_pos):
                    return  # Start the game
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Main game loop (after menu)
def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Add your game logic here
        screen.fill(BLACK)
        # Display game running text (just as a placeholder)
        game_text = font.render("Game Running", True, WHITE)
        screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, screen_height // 2 - game_text.get_height() // 2))

        pygame.display.update()

    pygame.quit()
    sys.exit()

# Start menu
menu()

# Start game after menu
game_loop()
