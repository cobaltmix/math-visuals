import pygame
import numpy as np
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 2000, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Collision")

# Define colors
WHITE = (255, 255, 255)

# Constants
G = 1e-14  # Gravitational constant in our simulation
dt = 0.000001  # Time step for the integrator
MASS_SCALE = 9e23  # Scale factor for drawing the black holes

# Define the gravitational acceleration function
def gravity_acceleration(m1, m2, r1, r2):
    distance_vector = r2 - r1
    distance_magnitude = np.linalg.norm(distance_vector)
    force_magnitude = G * m1 * m2 / distance_magnitude**2
    force_vector = force_magnitude * distance_vector / distance_magnitude
    return force_vector / m1, -force_vector / m2

# Define the update function
def update_black_holes(m1, m2, r1, r2, v1, v2, dt):
    a1, a2 = gravity_acceleration(m1, m2, r1, r2)
    r1 += v1 * dt
    r2 += v2 * dt
    v1 += a1 * dt
    v2 += a2 * dt

    return r1, r2, v1, v2

# Initial conditions
m1, m2 = 1e30, 1e29  # Masses of the black holes
r1 = np.array([WIDTH / 4, HEIGHT / 2])  # Position of the first black hole
r2 = np.array([3 * WIDTH / 4, HEIGHT / 2])  # Position of the second black hole
v1 = np.array([0, 1e3])  # Velocity of the first black hole
v2 = np.array([0, -1e3])  # Velocity of the second black hole

# Main loop
running = True
clock = pygame.time.Clock()
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    r1, r2, v1, v2 = update_black_holes(m1, m2, r1, r2, v1, v2, dt)

    # Collision detection
    if np.linalg.norm(r1 - r2) < (m1 / MASS_SCALE)**(1/3) + (m2 / MASS_SCALE)**(1/3):
        v1 = -v1
        v2 = -v2

    screen.fill(WHITE)
    pygame.draw.circle(screen, (0, 0, 0), r1.astype(int), int((m1 / MASS_SCALE)**(1/3)))
    pygame.draw.circle(screen, (0, 0, 0), r2.astype(int), int((m2 / MASS_SCALE)**(1/3)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()