import pygame
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)




# Load Player Image
player_img = pygame.image.load('player_ship.png')  # Replace with the path to your image
player_width, player_height = 100, 100
player_img = pygame.transform.scale(player_img, (player_width, player_height))  # Resize the image if necessary

# Load Enemy Image
enemy_img = pygame.image.load('enemy_ship.png')  # Replace with the path to your image
enemy_width, enemy_height = 50, 50
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))  # Resize the image if necessary


targetTime = 0
trigger = True

# Player Position
player_x = screen_width // 2 - player_width // 2  # Center horizontally
player_y = screen_height - player_height - 50  # Near the bottom
player_speed = 0.7

# Enemy Settings
enemy_rows = 4
enemy_cols = 9
enemy_padding = 20  # Space between enemies
enemy_offset_x = 100  # Horizontal offset from the left side of the screen
enemy_offset_y = 20   # Vertical offset from the top of the screen
enemy_spawn_rate = 5 # A enemy will spawn on a 5 or higher out of 10 
# Enemy Movement Settings
enemy_speed = .2
direction = 1  # 1 for right, -1 for left

# Initialize the score
score = 0
font = pygame.font.Font(None, 36)  # Use default font, size 36
win_font = pygame.font.Font(None, 72)  # Use default font, size 72 for "YOU WIN"

menu_font = pygame.font.Font(None, 74)
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

# Function to display the score on the screen
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))  # Position the score at the top-left of the screen

# Create a list to store enemies, each enemy is represented as a dictionary with x, y and alive status
enemies = []
for row in range(enemy_rows):
    for col in range(enemy_cols):
        enemy_x = enemy_offset_x + col * (enemy_width + enemy_padding)
        enemy_y = enemy_offset_y + row * (enemy_height + enemy_padding)
        spawn_num=random.randint(0, 10)
        if spawn_num <enemy_spawn_rate:
            enemies.append({"x": enemy_x, "y": enemy_y, "alive": True})
last_enemy_spawn=pygame.time.get_ticks()

# Function to check if a bullet hits an enemy
def check_collision(bullet, enemy):
    bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)

    return bullet_rect.colliderect(enemy_rect)

# Bullet Settings
bullet_width = 9
bullet_height = 10
bullet_speed = 1
bullets = []  # List to store all active bullets



#####################################################



# Enemy Bullet Settings
enemy_bullet_width = 9
enemy_bullet_height = 15
enemy_bullet_speed = 0.5
enemy_bullets = []  # List to store all active enemy bullets

def shoot_enemy_bullet(enemy):
    bullet_x = enemy["x"] + enemy_width // 2 - enemy_bullet_width // 2
    bullet_y = enemy["y"] + enemy_height
    enemy_bullets.append([bullet_x, bullet_y])

def check_player_collision(bullet):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    bullet_rect = pygame.Rect(bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height)
    return bullet_rect.colliderect(player_rect)


#####################################################



# Function to create a new bullet
def shoot_bullet():
    bullet_x = player_x + player_width // 2 - bullet_width // 2  # Center bullet relative to player
    bullet_y = player_y
    bullets.append([bullet_x, bullet_y])



# Bullet firing interval (cooldown)
bullet_cooldown = 500  # Time in milliseconds between shots
last_bullet_time = pygame.time.get_ticks()  # Get the current time in milliseconds
# Function to display the "YOU WIN" message


# Update Enemy Positions
def move_enemies():
    global direction
    move_down = False

    # Check if any enemy has reached the screen edges
    for enemy in enemies:
        if enemy["alive"]:
            enemy["x"] += direction * enemy_speed

            # Check for boundary collision
            if enemy["x"] < 0 or enemy["x"] > screen_width - enemy_width:
                move_down = True

    # Move enemies down and reverse direction
    if move_down:
        for enemy in enemies:
            if enemy["alive"]:
                enemy["x"] -= direction * enemy_speed  # Adjust position back
                enemy["y"] += enemy_height / 2  # Move down
        direction *= -1  # Reverse direction


# Function to display the "YOU WIN" message



def display_win_message():
    win_text = win_font.render("YOU WIN", True, GREEN)
    text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(win_text, text_rect)


def display_lose_message():
    win_text = win_font.render("YOU LOSE", True, RED)
    text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(win_text, text_rect)

# Main Game Loop after menu
def game_loop():
    running = True
    game_over = False  # Track whether the game is over
    win_start_time = None  # To keep track of when the win message was displayed
    while running:
        screen.fill(BLACK)  # Fill the screen with black

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_lose_message()
                running = False


        if not game_over:
            # Player Movement
            keys = pygame.key.get_pressed()
            global player_x
            global player_y

            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
                player_x += player_speed

            # Bullet cooldown
            global trigger
            if trigger:
                startTime = pygame.time.get_ticks()
                targetTime = startTime + bullet_cooldown
                trigger = False
            # if current_time - last_bullet_time > bullet_cooldown:
            if keys[pygame.K_SPACE]:

                if pygame.time.get_ticks() > targetTime:
                    shoot_bullet()
                    trigger = True
                    startTime = pygame.time.get_ticks()
                    targetTime = startTime + bullet_cooldown

            # Move bullets upward s
            global bullets
            for bullet in bullets:
                bullet[1] -= bullet_speed

            # Remove bullets that are off the screen
            bullets = [bullet for bullet in bullets if bullet[1] > 0]


            # have a chance to spawn additinal enemies ever 5 seconds
            temp_time=pygame.time.get_ticks()
            global last_enemy_spawn
            if (temp_time - last_enemy_spawn) >5000: 
                col=random.randint(0, enemy_cols)
                row=random.randint(0, enemy_rows)
                enemy_x = enemy_offset_x + col * (enemy_width + enemy_padding)
                enemy_y = enemy_offset_y + row * (enemy_height + enemy_padding)
                spawn_num=random.randint(0, 10)
                if spawn_num <enemy_spawn_rate:
                    enemies.append({"x": enemy_x, "y": enemy_y, "alive": True})
                    last_enemy_spawn=pygame.time.get_ticks()
            # Move enemies
            move_enemies()




            # Draw the Player
            screen.blit(player_img, (player_x, player_y))

            # Draw bullets
            for bullet in bullets:
                pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))




        ############################################################

            for enemy in enemies:
                if enemy["alive"]:
                    if random.randint(0, 10) < 5:  # Random chance to shoot
                        current_time = pygame.time.get_ticks()
                        global last_bullet_time
                        if current_time - last_bullet_time > (bullet_cooldown / 2):
                            last_bullet_time = current_time
                            shoot_enemy_bullet(enemy)

                # Move enemy bullets downwards
                global enemy_bullets          
            for bullet in enemy_bullets:
                bullet[1] += enemy_bullet_speed

                # Remove enemy bullets that go off the screen
            enemy_bullets = [bullet for bullet in enemy_bullets if bullet[1] < screen_height]

            # Check for collisions between enemy bullets and player
            for bullet in enemy_bullets:
                if check_player_collision(bullet):
                    game_over = True  # End the game if the player is hit 
                    lose_start_time=pygame.time.get_ticks()
                    break

            # Draw enemy bullets
            for bullet in enemy_bullets:
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))



        ############################################################
            # Draw enemies and check for collisions
            all_enemies_destroyed = True
            for enemy in enemies:
                if enemy["alive"]:
                    all_enemies_destroyed = False
                    # pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_width, enemy_height))
                    screen.blit(enemy_img, (enemy["x"], enemy["y"]))

                    global score 
                    for bullet in bullets:
                        if check_collision(bullet, enemy):
                            enemy["alive"] = False  # Destroy the enemy
                            bullets.remove(bullet)  # Remove the bullet that hit the enemy
                            score += 10  # Increase score by 10 points per enemy
                            break  # Exit the loop to avoid modifying the bullets list during iteration

            if all_enemies_destroyed:
                game_over = True  # End the game
                win_start_time = pygame.time.get_ticks()  # Record the time when game ended
                display_win_message()  # Display the win message


        else:
            
            # Display the win message if game is over
            if win_start_time is None:
                display_lose_message()
            #display_win_message()

            # Check if enough time has passed to close the window
            if (lose_start_time is not None and pygame.time.get_ticks() - lose_start_time >2000 ) or (win_start_time is not None and pygame.time.get_ticks() - win_start_time > 2000) :  # 2 seconds
                running = False

        # Display the current score
        display_score()

        # Update display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Start menu
menu()

# Start game after menu
game_loop()
