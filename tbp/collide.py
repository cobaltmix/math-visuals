import pygame
import numpy as np
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 2000, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three-Body Problem")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [RED, GREEN, BLUE]

# Constants
G = 1.4  # Gravitational constant in our simulation
dt = 0.01  # Time step for the integrator
MASS_SCALE = 3  # Scale factor for drawing the stars

# Initial conditions
masses = np.array([4e3, 5e3, 5.385e3])  # Mass of the stars in tons
positions = np.array(
    [[200,300], [900,900], [1800, 300]], dtype=float
)  # Initial positions
velocities = np.zeros_like(positions)  # Initial velocities - will update two values below.

# Set initial upward velocities for smaller stars
# The exact values require tuning based on the simulation parameters for a stable orbit.
velocities[0, 1] = 100  # Star 0 velocity in y-direction
velocities[1, 1] = -100  # Star 1 velocity in y-direction
velocities[0, 0] = 100  # Star 0 velocity in x-direction
velocities[1, 0] = 0  # Star 1 velocity in x-direction
velocities[2, 0] = -100  # Star 2 velocity in x-direction
velocities[2, 1] = 100
trail_points = [[] for _ in positions]  # List to store the trail points for each circle

def check_collision_and_update_masses(masses, positions):
    num_bodies = len(masses)
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):  # Only check each pair once
            distance = np.linalg.norm(positions[i] - positions[j])
            # Determine if there's a collision, adding buffer (2) to ensure the visual overlap
            if distance < (np.sqrt(masses[i] / MASS_SCALE) + np.sqrt(masses[j] / MASS_SCALE) + 2):
                # Increase mass by 10% for both stars
                masses[i] += 100
                masses[j] += 100


# Define the acceleration due to gravity
def gravity_acceleration(masses, positions):
    acc = np.zeros_like(positions)
    num_bodies = len(masses)
    for i in range(num_bodies):
        for j in range(num_bodies):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec)
                acc[i] += G * masses[j] * r_vec / r_mag**1.6
    return acc


# Define the update function
def update_system(masses, positions, velocities, dt):
    pos_new = positions + velocities * dt
    acc = gravity_acceleration(masses, positions)
    vel_new = velocities + acc * dt

    # Check for boundary collision and bounce if necessary
    for i, pos in enumerate(pos_new):
        if pos[0] <= 0 or pos[0] >= WIDTH:  # Check x boundaries
            vel_new[i, 0] = -vel_new[i, 0] + (0.8*vel_new[i, 0])  # Reverse x velocity
            pos_new[i, 0] = max(0, min(pos[0], WIDTH))  # Keep inside window
        if pos[1] <= 0 or pos[1] >= HEIGHT:  # Check y boundaries
            vel_new[i, 1] = -vel_new[i, 1] + (0.8*vel_new[i, 1])  # Reverse y velocity
            pos_new[i, 1] = max(0, min(pos[1], HEIGHT))  # Keep inside window

    return pos_new, vel_new

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Update and draw stars
    positions, velocities = update_system(masses, positions, velocities, dt)
    check_collision_and_update_masses(masses, positions)

    for i, (pos, mass) in enumerate(zip(positions, masses)):
        # Add position to trail points, ensuring it's a valid integer tuple
        trail_points[i].append(tuple(pos.astype(int)))

        # Draw the trail if there are at least 2 points, using the star's color
        if len(trail_points[i]) >= 2:
            if len(trail_points[i]) > 1000:  # Limit the number of trail points
                trail_points[i].pop(0)
            # Use the color specific to this star for the trail
            pygame.draw.lines(screen, colors[i], False, trail_points[i], 3)  # Draw the trail line

        # Draw the circle with a black border and fill with the star's color
        pygame.draw.circle(
            screen, (0,0,0), pos.astype(int), int(np.sqrt(mass / MASS_SCALE) + 3)
        )
        pygame.draw.circle(
            screen, colors[i], pos.astype(int), int(np.sqrt(mass / MASS_SCALE))
        )

    pygame.display.flip()
    clock.tick(120)

    # Event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()


