import pygame
import sys
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load sound files
BALL_SOUNDS = {
    'red': pygame.mixer.Sound('A4.wav'),
    'green': pygame.mixer.Sound('B4.wav'),
    'blue': pygame.mixer.Sound('C5.wav'),
    'yellow': pygame.mixer.Sound('D5.wav'),
    'orange': pygame.mixer.Sound('E5.wav'),
}

# Function to map color to sound
def get_sound_by_color(color):
    color_to_name = {
        (255, 0, 0): 'red',
        (0, 255, 0): 'green',
        (0, 0, 255): 'blue',
        (255, 255, 0): 'yellow',
        (255, 165, 0): 'orange',
    }
    color_name = color_to_name.get(color, None)
    return BALL_SOUNDS.get(color_name, None)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls with Closing Walls and Sounds")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Ball properties
BALL_SIZE = 20
NUM_BALLS = 5
INITIAL_BALL_X = WIDTH // 2  # Start position for all balls

# Walls
wall_width = 10
left_wall_x = 0
right_wall_x = WIDTH - wall_width
wall_speed = 0.2

# Ball class
class Ball:
    def __init__(self, color, speed, y):
        self.color = color
        self.speed = speed
        self.x = INITIAL_BALL_X
        self.y = y
        self.sound = get_sound_by_color(color)

    def move(self, left_wall_x, right_wall_x):
        bounced = False
        self.x += self.speed
        if self.x > right_wall_x - BALL_SIZE:
            self.x = right_wall_x - BALL_SIZE
            self.speed = -self.speed
            bounced = True
        elif self.x < left_wall_x  + + BALL_SIZE:
            self.x = left_wall_x + BALL_SIZE
            self.speed = -self.speed
            bounced = True
        if bounced and self.sound:
            self.sound.play()

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_SIZE+1)
        pygame.draw.circle(screen, self.color, (self.x, self.y), BALL_SIZE)

# Create balls with different y values
ball_spacing = HEIGHT // (NUM_BALLS + 1)
velo = [2,3,4,6,8]
balls = [Ball(color, velo[i], (i + 1) * ball_spacing) for i, color in enumerate(BALL_COLORS)]


pygame.mixer.set_num_channels(64)
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Move and draw balls
    for ball in balls:
        ball.move(left_wall_x, right_wall_x)
        ball.draw(screen)

    # Move walls
    left_wall_x += wall_speed
    right_wall_x -= wall_speed

    # Draw walls
    pygame.draw.rect(screen, WHITE, (left_wall_x - wall_width, 0, wall_width, HEIGHT))
    pygame.draw.rect(screen, WHITE, (right_wall_x, 0, wall_width, HEIGHT))

    # Update screen
    pygame.display.flip()

    # Control the wall speed and stop if they meet
    if right_wall_x <= left_wall_x + BALL_SIZE+20:
        wall_speed = 0
        break

    clock.tick(60) # Limit to 60 frames per second

pygame.quit()
sys.exit()