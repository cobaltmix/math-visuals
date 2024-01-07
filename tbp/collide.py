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
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [RED, GREEN, BLUE]

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

channels = [pygame.mixer.Channel(i) for i in range(64)]

# Load sound files for the notes
note_files = [
    "C6.wav",
    "C6.wav",
    "C6.wav",
    "C6.wav",
    "C6.wav",
    "D6.wav",
    "C6.wav",
    "D6.wav",
    "D6.wav",
    "F6.wav",
    "D6.wav",
    "F6.wav",
    "F6.wav",
    "D6.wav",
    "F6.wav",
    "D6.wav",
    "D6.wav",
    "C6.wav",
    "D6.wav",
    "C6.wav",
    "C6.wav",
    "A5#.wav",
    "C6.wav",
    "A5#.wav",
    "A5#.wav",
    "C6.wav",
    "A5#.wav",
    "C6.wav",
    "A5#.wav",
    "D6#.wav",
    "C6.wav",
    "D6#.wav",
    "D6#.wav",
    "C6.wav",
    "D6#.wav",
    "C6.wav",
    "C6.wav",
    "D6.wav",
    "C6.wav",
    "D6.wav",
    "D6.wav",
    "A5#.wav",
    "D6.wav",
    "A5#.wav",
    "A5#.wav",
    "A5.wav",
    "A5#.wav",
    "A5.wav",
    "A5.wav",
    "A5#.wav",
    "A5.wav",
    "A5#.wav",
    "A5#.wav",
    "G5.wav",
    "A5#.wav",
    "G5.wav",
    "G5.wav",
    "F5.wav",
    "G5.wav",
    "F5.wav",
    "F5.wav",
    "C6.wav",
    "F5.wav",
    "C6.wav",
    "C6.wav",
    "C6.wav",
    "C6.wav",
    "C6.wav",

]
notes = [pygame.mixer.Sound(note_file) for note_file in note_files]

# Current note index
current_note = 0
last_note_time = 0  # Time when the last note was played
note_cooldown = 200  # Cooldown between notes in milliseconds


# Constants
G = 1  # Gravitational constant in our simulation
dt = 0.01  # sTime step for the integrator
MASS_SCALE = 5  # Scale factor for drawing the stars

# Initial conditions
masses = np.array([9e3, 8e3, 7e3])  # Mass of the stars in tons
positions = np.array(
    [[200,600], [900,900], [1800, 600]], dtype=float
)  # Initial positions
velocities = np.zeros_like(positions)  # Initial velocities - will update two values below.

# Set initial upward velocities for smaller stars
# The exact values require tuning based on the simulation parameters for a stable orbit.
velocities[0, 1] = 0  # Star 0 velocity in y-direction
velocities[1, 1] = 0  # Star 1 velocity in y-direction
velocities[0, 0] = 0  # Star 0 velocity in x-direction
velocities[1, 0] = 0  # Star 1 velocity in x-direction
velocities[0, 0] = 0  # Star 2 velocity in x-direction
velocities[1, 0] = 0
trail_points = [[] for _ in positions]  # List to store the trail points for each circle

def check_collision_and_update_masses(masses, positions, velocities, current_note, last_note_time):
    num_bodies = len(masses)
    for i in range(num_bodies):
        for j in range(i+1, num_bodies):  # Only check each pair once
            distance = np.linalg.norm(positions[i] - positions[j])
            radius_i = np.sqrt(masses[i] / MASS_SCALE)
            radius_j = np.sqrt(masses[j] / MASS_SCALE)
            # Determine if there's a collision
            if distance < (radius_i + radius_j):
                # Calculate elastic collision response

                # Move to the next note, wrapping around if at the end of the list
                available_channel = next(
                    (channel for channel in channels if not channel.get_busy()), None
                )
                if available_channel is not None:
                    available_channel.play(notes[current_note])
                current_note = (current_note + 1) % len(notes)

                mass_sum = masses[i] + masses[j]
                v1 = velocities[i] - 2 * masses[j] / mass_sum * (np.dot(velocities[i] - velocities[j], positions[i] - positions[j]) /
                                                                  np.linalg.norm(positions[i] - positions[j])**2) * (positions[i] - positions[j])
                v2 = velocities[j] - 2 * masses[i] / mass_sum * (np.dot(velocities[j] - velocities[i], positions[j] - positions[i]) /
                                                                  np.linalg.norm(positions[j] - positions[i])**2) * (positions[j] - positions[i])
                velocities[i] = v1
                velocities[j] = v2

                # # Apply growth to the masses
                # masses[i] *= 1.1
                # masses[j] *= 1.1

                # Repulsion step to prevent sticking
                overlap = (radius_i + radius_j) - distance
                direction = (positions[j] - positions[i]) / distance
                repulsion_force = direction * overlap * 0.5
                positions[i] -= repulsion_force
                positions[j] += repulsion_force

                # Play a sound if the cooldown has passed
                current_time = pygame.time.get_ticks()
                if current_time - last_note_time >= note_cooldown:
                    available_channel = next(
                        (channel for channel in channels if not channel.get_busy()), None
                    )
                    if available_channel:
                        available_channel.play(notes[current_note])
                    last_note_time = current_time
                    current_note = (current_note + 1) % len(notes)

    return velocities, current_note, last_note_time

# Define the acceleration due to gravity
def gravity_acceleration(masses, positions):
    acc = np.zeros_like(positions)
    num_bodies = len(masses)
    for i in range(num_bodies):
        for j in range(num_bodies):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec)
                acc[i] += G * masses[j] * r_vec / r_mag**1.31
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
    screen.fill(BLACK)

    # Update and draw stars
    # Update and draw stars
    positions, velocities = update_system(masses, positions, velocities, dt)

    velocities, current_note, last_note_time = check_collision_and_update_masses(masses, positions, velocities, current_note, last_note_time)

    # Check for note cooldown
    current_time = pygame.time.get_ticks()
    if current_time - last_note_time >= note_cooldown:
        check_collision_and_update_masses(masses, positions, velocities, current_note, last_note_time)
        last_note_time = current_time
        current_note = (current_note + 1) % len(notes)

    for i, (pos, mass) in enumerate(zip(positions, masses)):
        # Add position to trail points, ensuring it's a valid integer tuple
        trail_points[i].append(tuple(pos.astype(int)))

        # Draw the trail if there are at least 2 points, using the star's color
        if len(trail_points[i]) >= 2:
            if len(trail_points[i]) > 200:  # Limit the number of trail points
                trail_points[i].pop(0)
            # Use the color specific to this star for the trail
            pygame.draw.lines(screen, colors[i], False, trail_points[i], 3)  # Draw the trail line

        # Draw the circle with a black border and fill with the star's color
        pygame.draw.circle(
            screen, WHITE, pos.astype(int), int(np.sqrt(mass / MASS_SCALE) + 2)
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


