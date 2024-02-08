import pygame
import sys
import math
from collections import deque

# Initialize Pygame
pygame.init()
x, y = 0, 0

# Set up display
screen_width, screen_height = 1500, 1300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conserved Bounce Angle Simulation")
previous_circle_positions = deque(maxlen=3000)  # Change maxlen to manage trail length

# Colors and gradient interpolation function
BLACK = (0, 0, 0)
colors = [
    (255, 0, 0),  # Red
    (0, 0, 255),  # Blue
    (255, 0, 255),  # Purple
    (255, 165, 0),  # Orange
]

pygame.mixer.init()
pygame.mixer.set_num_channels(128)

channels = [pygame.mixer.Channel(i) for i in range(128)]

# # Load sound files for the notes
# note_files = [
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "B4.wav",
#     "D5.wav",
#     "C5.wav",
#     "A4.wav",
#     "C4.wav",
#     "E4.wav",
#     "A4.wav",
#     "B4.wav",
#     "E4.wav",
#     "G#4.wav",
#     "B4.wav",
#     "C5.wav",
#     "E4.wav",
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "B4.wav",
#     "D5.wav",
#     "C5.wav",
#     "A4.wav",
#     "C4.wav",
#     "E4.wav",
#     "A4.wav",
#     "B4.wav",
#     "D4.wav",
#     "C5.wav",
#     "B4.wav",
#     "A4.wav",
#     "B4.wav",
#     "C5.wav",
#     "D5.wav",
#     "E5.wav",
#     "G4.wav",
#     "F5.wav",
#     "E5.wav",
#     "D5.wav",
#     "F4.wav",
#     "E5.wav",
#     "D5.wav",
#     "C5.wav",
#     "E4.wav",
#     "D5.wav",
#     "C5.wav",
#     "B4.wav",
#     "E4.wav",
#     "E4.wav",
#     "E5.wav",
#     "E5.wav",
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "D#5.wav",
#     "E5.wav",
#     "B4.wav",
#     "D5.wav",
#     "C5.wav",
#     "A4.wav",
# ]
# Load sound files for the notes
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


# note_files = [
#     "D1.wav", "D#1.wav",
#     "E1.wav",
#     "F1.wav", "F#1.wav",
#     "G1.wav", "G#1.wav",
#     "A1.wav", "A#1.wav",
#     "B1.wav",
#     "C2.wav", "C#2.wav",
#     "D2.wav", "D#2.wav",
#     "E2.wav",
#     "F2.wav", "F#2.wav",
#     "G2.wav", "G#2.wav",
#     "A2.wav", "A#2.wav",
#     "B2.wav",
#     "C3.wav", "C#3.wav",
#     "D3.wav", "D#3.wav",
#     "E3.wav",
#     "F3.wav", "F#3.wav",
#     "G3.wav", "G#3.wav",
#     "A3.wav", "A#3.wav",
#     "B3.wav",
#     "C4.wav", "C#4.wav",
#     "D4.wav", "D#4.wav",
#     "E4.wav",
#     "F4.wav", "F#4.wav",
#     "G4.wav", "G#4.wav",
#     "A4.wav", "A#4.wav",
#     "B4.wav",
#     "C5.wav", "C#5.wav",
#     "D5.wav", "D#5.wav",
#     "E5.wav",
#     "F5.wav", "F#5.wav",
#     "G5.wav", "G#5.wav",
#     "A5.wav", "A#5.wav",
#     "B5.wav",
#     "C6.wav", "C#6.wav",
#     "D6.wav", "D#6.wav",
#     "E6.wav",
#     "F6.wav", "F#6.wav",
#     "G6.wav", "G#6.wav",
#     "A6.wav", "A#6.wav",
#     "B6.wav",
#     "C7.wav", "C#7.wav",
#     "D7.wav", "D#7.wav",
#     "E7.wav",
#     "F7.wav", "F#7.wav",
#     "G7.wav", "G#7.wav",
#     "A7.wav", "A#7.wav",
#     "B7.wav", "C8.wav"
# ]
notes = [pygame.mixer.Sound(note_file) for note_file in note_files]

# Current note index
current_note = 0


# Function to interpolate between colors
def interpolate_color(color1, color2, t):
    return tuple(color1[i] + (color2[i] - color1[i]) * t for i in range(3))


# Circle settings
big_circle_center = (screen_width // 2, screen_height // 2)
big_circle_radius = 550
small_circle_radius = 50
small_circle_center = (
    big_circle_center[0],
    big_circle_center[1] - big_circle_radius + small_circle_radius,
)

# Small circle movement and trail settings
velocity = [10, 0]  # Reduced initial velocity for slower movement
gravity = 0.6  # Reduced gravity for slower acceleration


color_index, t, color_change_speed = 0, 0, 0.03
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

    if small_circle_radius + 10 >= big_circle_radius:
        small_circle_center = (screen_width / 2, screen_height / 2)
    trail_radius = int(small_circle_radius) + 1

    # Add the current small circle position and radius to the trail deque
    previous_circle_positions.appendleft(
        (small_circle_center, small_circle_radius, BALL_COLOR)
    )

    # Render
    screen.fill(BLACK)

    # Set clipping area to be the big circle only
    clip_rect = pygame.Rect(
        big_circle_center[0] - big_circle_radius - 3,
        big_circle_center[1] - big_circle_radius - 3,
        big_circle_radius * 2.1,
        big_circle_radius * 2.1,
    )

    # Render the big black circle and the big colored circle borders
    pygame.draw.circle(screen, BALL_COLOR, big_circle_center, big_circle_radius + 5)
    pygame.draw.circle(screen, BLACK, big_circle_center, big_circle_radius)
    # Draw the trail of the previous small circle positions with their stored radii

    screen.set_clip(clip_rect)
    for pos, rad, col in previous_circle_positions:
        pygame.draw.circle(screen, col, pos, rad)
        # Remove clipping to draw other elements
    screen.set_clip(None)

    # Render the current small circle position
    pygame.draw.circle(screen, BLACK, small_circle_center, small_circle_radius+5)
    pygame.draw.circle(screen, BALL_COLOR, small_circle_center, small_circle_radius)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
