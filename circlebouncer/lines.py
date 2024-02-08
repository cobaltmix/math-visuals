import pygame
import sys
import math
from collections import deque
import random

# Initialize Pygame
pygame.init()
x, y = 0, 0

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
pygame.mixer.set_num_channels(64)

channels = [pygame.mixer.Channel(i) for i in range(64)]

note_files = [
    "F5.wav",
    "D5.wav",
    "A4.wav",
    "D5.wav",
        "F5.wav",
    "D5.wav",
    "A4.wav",
    "D5.wav",
        "F5.wav",
    "C5.wav",
    "A4.wav",
    "C5.wav",
    "F5.wav",
        "C5.wav",
    "A4.wav",
    "C5.wav",
        "E5.wav",
    "C#5.wav",
    "A4.wav",
    "C#5.wav",
        "E5.wav",
        "C#5.wav",
    "A4.wav",
    "C#5.wav",
        "E5.wav",
        "C#5.wav",
    "A4.wav",
    "C#5.wav",
        "E5.wav",

    "A5.wav",
    "D5.wav",
    "E5.wav",
    "F5.wav",
    "A5.wav",
    "G5.wav",
    "A5.wav",
    "C5.wav",
    "D5.wav",
        "E5.wav",
    "F5.wav",
    "E5.wav",
    "G5.wav",
    "A5.wav",
    "G5.wav",
    "F5.wav",
    "F5.wav",
    "F5.wav",
    "F5.wav",
    "A5.wav",
    "A5.wav",
    "G5.wav",
    "F5.wav",
    "A5.wav",
    "A5.wav",
    "A5.wav",
    "G5.wav",
    "A5.wav",
    "G5.wav",
    "F5.wav",
    "F5.wav",
    "F5.wav",
    "F5.wav",
        "A5.wav",
    "A5.wav",
    "G5.wav",
    "F5.wav",
]
notes = [pygame.mixer.Sound(note_file) for note_file in note_files]

# Current note index
current_note = 0


# Function to interpolate between colors
def interpolate_color(color1, color2, t):
    return tuple(color1[i] + (color2[i] - color1[i]) * t for i in range(3))


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


color_index, t, color_change_speed = 0, 0, 0.015

# Clock for controlling frame rate

clock = pygame.time.Clock()
# Main loop

running = True

while running:  # Handle events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # Bounce small circle and adjust radius
    if distance + small_circle_radius >= big_circle_radius:
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

        small_circle_radius *= 1.05

    if small_circle_radius >= big_circle_radius:
        small_circle_center = (screen_width / 2, screen_height / 2)

    # Render
    screen.fill(BLACK)

    pygame.draw.circle(screen, BALL_COLOR, big_circle_center, big_circle_radius + 5)
    pygame.draw.circle(screen, BLACK, big_circle_center, big_circle_radius)
    pygame.draw.circle(
        screen, (255, 255, 255), small_circle_center, small_circle_radius + 1
    )
    pygame.draw.circle(screen, BALL_COLOR, small_circle_center, small_circle_radius)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
