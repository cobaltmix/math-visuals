import pygame
import sys
import math
from collections import deque

# Initialize Pygame
pygame.init()
x,y = 0,0

# Set up display
screen_width, screen_height = 1500, 1300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conserved Bounce Angle Simulation")

# Colors and gradient interpolation function
BLACK = (0, 0, 0)
colors = [
    (255, 0, 0),  # Red
    (0, 0, 255),  # Blue
    (255, 0, 255),  # Purple
    (255, 165, 0),  # Orange
]

pygame.mixer.init()
pygame.mixer.set_num_channels(16)

channels = [pygame.mixer.Channel(i) for i in range(16)]

# Load sound files for the notes
note_files = [
    "f2.wav",
    "a2.wav",
    "g3.wav",
    "e3.wav",
    "c3.wav",
    "b3.wav",
    "g4.wav",
    "f4.wav",
    "d4.wav",
    "a4.wav",
    "e5.wav",
    "b5.wav",
]
notes = [pygame.mixer.Sound(note_file) for note_file in note_files]

# Current note index
current_note = 0


# Function to interpolate between colors
def interpolate_color(color1, color2, t):
    return tuple(color1[i] + (color2[i] - color1[i]) * t for i in range(3))

# Black hole settings
black_hole_center = (screen_width // 2, screen_height // 2)
black_hole_radius = 10  # Radius just for rendering
black_hole_force_multiplier = 1000  # Controls strength of attraction
small_circle_mass = 100  # The mass for the gravitational calculation
min_threshold_distance = 50  # Minimum distance at which the force starts to become stronger
max_threshold_distance = 200  # Maximum distance at which the force caps off

def calculate_gravitational_force(position, mass):
    distance_x = black_hole_center[0] - position[0]
    distance_y = black_hole_center[1] - position[1]
    distance = math.sqrt(distance_x**2 + distance_y**2)

    # Prevent division by zero for very small distances
    if distance < min_threshold_distance:
        return (0, 0)

    # Scale the force based on the distance
    if distance > max_threshold_distance:
        distance_scale = max_threshold_distance
    else:
        distance_scale = distance

    # Calculate radial force magnitude based on the scaled distance (inverse square law)
    force_magnitude = black_hole_force_multiplier * mass / (distance_scale**2)

    # Calculate radial force vector components
    radial_force_x = force_magnitude * (distance_x / distance)
    radial_force_y = force_magnitude * (distance_y / distance)

    # Calculate tangential force to simulate black hole spin (perpendicular to radial force)
    tangential_force_x = -radial_force_y  # x component is negative y component of radial force
    tangential_force_y = -radial_force_x   # y component is x component of radial force

    # Optional: scale the tangential force as needed
    spin_strength = 0.8  # Adjust as necessary to control how much the circle curves
    tangential_force_x *= spin_strength
    tangential_force_y *= spin_strength

    # Combine radial and tangential forces
    total_force_x = radial_force_x + tangential_force_x
    total_force_y = radial_force_y + tangential_force_y

    return (total_force_x, total_force_y)


# Circle settings
big_circle_center = (screen_width // 2, screen_height // 2)
big_circle_radius = 550
small_circle_radius = 20
small_circle_center = (
    big_circle_center[0],
    big_circle_center[1] - big_circle_radius + small_circle_radius,
)

# Small circle movement and trail settings
velocity = [5, 0.2]  # Reduced initial velocity for slower movement
gravity = 0.4  # Reduced gravity for slower acceleration

# Color interpolation settings
color_index, t, color_change_speed = 0, 0, 0.005

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Update velocity with calculated gravitational force
    gravity_force = calculate_gravitational_force(small_circle_center, small_circle_mass)
    velocity[0] += gravity_force[0]
    velocity[1] += gravity_force[1]

    # Update small circle and trail
    velocity[1] += gravity
    small_circle_center = (
        small_circle_center[0] + velocity[0],
        small_circle_center[1] + velocity[1],
    )
    distance = math.hypot(
        small_circle_center[0] - big_circle_center[0],
        small_circle_center[1] - big_circle_center[1],
    )
    t = (t + color_change_speed) % 1
    if t < color_change_speed:
        color_index = (color_index + 1) % len(colors)
    BALL_COLOR = interpolate_color(
        colors[color_index], colors[(color_index + 1) % len(colors)], t
    )

    # Calculate gravitational force towards the black hole
    gravity_force = calculate_gravitational_force(small_circle_center, small_circle_mass)



    # Render the black hole (optional)
    pygame.draw.circle(screen, (255, 255, 255), black_hole_center, black_hole_radius)

    # Bounce small circle and adjust radius
    if distance + small_circle_radius - 5 >= big_circle_radius:
        # Play the next note

        # Move to the next note, wrapping around if at the end of the list
        available_channel = next(
            (channel for channel in channels if not channel.get_busy()), None
        )
        if available_channel is not None:
            available_channel.play(notes[current_note])
        current_note = (current_note + 1) % len(notes)

        nx, ny = [
            (c1 - c2) / distance
            for c1, c2 in zip(small_circle_center, big_circle_center)
        ]
        dot_product = sum(velocity[i] * n for i, n in enumerate((nx, ny)))
        velocity = [v - 2 * dot_product * n for v, n in zip(velocity, (nx, ny))]

        while distance + small_circle_radius + 5 >= big_circle_radius:
            small_circle_center = (
                small_circle_center[0] - nx,
                small_circle_center[1] - ny,
            )
            distance = math.hypot(
                *(c1 - c2 for c1, c2 in zip(small_circle_center, big_circle_center))
            )

        velocity[0] -= 0.3*velocity[0]
        velocity[1] -= 0.3*velocity[1]


    if small_circle_radius + 10 >= big_circle_radius:
        small_circle_center = (
            screen_width/2, screen_height/2
        )


    # Render
    screen.fill(BLACK)

    pygame.draw.circle(
        screen, (255, 255, 255), big_circle_center, big_circle_radius + 5
    )
    pygame.draw.circle(screen, BLACK, big_circle_center, big_circle_radius)
    pygame.draw.circle(
        screen, (255, 255, 255), small_circle_center, small_circle_radius + 1
    )
    pygame.draw.circle(screen, BALL_COLOR, small_circle_center, small_circle_radius)
    pygame.draw.circle(screen, (255, 255, 255), black_hole_center, black_hole_radius)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
