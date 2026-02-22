import pygame
import random
import sys

# --- 1. Pygame Initialization ---
pygame.init()

# --- 2. Screen Dimensions and Setup ---
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Apples")

# --- 3. Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255) # Color for the player's basket
APPLE_COLOR = RED   # Color for the falling apples

# --- 4. Game Clock and Frame Rate ---
clock = pygame.time.Clock()
Target_FPS = 100**6
FPS = Target_FPS # Frames per second
print("Target FPS set to:", Target_FPS)

# --- 5. Player Properties (Basket) ---
player_width = 100
player_height = 20
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10 # Position near the bottom of the screen  
player_speed = 30
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# --- 6. Falling Object Properties (Apples) ---
apple_size = 50
apple_speed_min = 1
apple_speed_max = 5
apples = [] # List to store dictionaries of apple 'rect' and 'speed'
APPLE_SPAWN_RATE = 10 # Spawn a new apple every 60 frames (approx. 1 second at 60 FPS)  
apple_spawn_counter = 0

# --- 7. Game Variables ---
score = 0
# Font for displaying the score
font = pygame.font.Font(None, 36) # Default font, size 36

# --- 8. Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player Movement ---
    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    # Keep player within screen bounds
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH

    # --- Spawn New Apples ---
    apple_spawn_counter += 1
    if apple_spawn_counter >= APPLE_SPAWN_RATE:
        apple_x = random.randint(0, SCREEN_WIDTH - apple_size)
        apple_y = -apple_size # Start the apple just above the screen
        apple_speed = random.randint(apple_speed_min, apple_speed_max)
        apples.append({'rect': pygame.Rect(apple_x, apple_y, apple_size, apple_size), 'speed': apple_speed})
        apple_spawn_counter = 0

    # --- Update Apple Positions and Check Collisions/Off-screen ---
    apples_to_remove = [] # List to safely store apples that need to be removed
    for apple in apples:
        # Move apple downwards
        apple['rect'].y += apple['speed']

        # Check for collision with player (basket)
        if player_rect.colliderect(apple['rect']):
            score += 1
            apples_to_remove.append(apple) # Mark apple for removal

        # Check if apple goes off-screen (missed)
        if apple['rect'].top > SCREEN_HEIGHT:
            apples_to_remove.append(apple) # Mark apple for removal

    # Remove caught/missed apples from the main list
    for apple in apples_to_remove:
        # Check if apple is still in the list before trying to remove
        # This handles cases where an apple might be added to apples_to_remove multiple times
        if apple in apples:
            apples.remove(apple)

    # --- Drawing ---
    screen.fill(BLACK) # Clear the screen with black background

    # Draw player
    pygame.draw.rect(screen, GREEN, player_rect)

    # Draw apples
    for apple in apples:
        pygame.draw.rect(screen, APPLE_COLOR, apple['rect']) # Drawing as rectangles for simplicity

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE) # Render text (text, antialias, color)
    screen.blit(score_text, (10, 10)) # Draw text on screen at (10, 10)

    # --- Update Display ---
    pygame.display.flip() # Update the full display Surface to the screen

    # --- Control Frame Rate ---
    clock.tick(FPS) # Limit the frame rate to FPS

# --- 9. Quit Pygame ---
pygame.quit()
sys.exit() # Exit the program