import pygame
import math
import cmath

# Initialize Pygame
pygame.init()

# Constants for the display
WIDTH, HEIGHT = 2000, 1200
BACKGROUND_COLOR = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rotating Lines with Complex Function')

# Function to compute the position based on the complex number z
def complex_to_screen(z, center, scale):
    # Convert a complex number z to a screen position, using the given center and scale.
    x = z.real * scale
    y = -z.imag * scale  # Negative because Pygame y-coordinates are inverted
    return int(center[0] + x), int(center[1] + y)

# Function to compute the complex rotation based on the function z(theta)
def z(theta):
    return cmath.exp(theta * 1j) + cmath.exp((0.1*math.pi + 2.125*theta)*1j)

# Center of the screen
center = (WIDTH // 2, HEIGHT // 2)
scale = 250  # The scale factor to adjust the size of the visualization

# Trail for the line
trail_points = []
max_trail_length = 300000

# Initialize theta
theta = 0
# Function to recalculate trail points based on the new scale
def update_trail_points(trail_points, center, old_scale, new_scale):
    new_trail_points = []
    scale_factor = new_scale / old_scale
    for point in trail_points:
        # Adjust the point relative to center, scale, then move back
        adjusted_x = (point[0] - center[0]) * scale_factor + center[0]
        adjusted_y = (point[1] - center[1]) * scale_factor + center[1]
        new_trail_points.append((int(adjusted_x), int(adjusted_y)))
    return new_trail_points

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Update theta for the next frame
    theta += 0.01

    # Compute the complex rotation based on theta
    complex_position = z(theta)

    # Convert complex numbers to screen coordinates
    line1_end = complex_to_screen(complex_position, center, scale)
    line2_end = complex_to_screen(complex_position * cmath.exp(math.pi * theta * 1j), center, scale)

    # Add the current end position of line 2 to the trail
    if len(trail_points) == 0 or trail_points[-1] != line2_end:
        trail_points.append(line2_end)
    if len(trail_points) > max_trail_length:
        trail_points.pop(0)

    # Compute the complex rotation based on theta
    complex_position = z(theta)

    # Convert complex numbers to screen coordinates
    line1_end = complex_to_screen(complex_position, center, scale)
    line2_end = complex_to_screen(complex_position * cmath.exp(math.pi * theta * 1j), center, scale)

    # Add the current end position of line 2 to the trail
    trail_points.append(line2_end)
    if len(trail_points) > max_trail_length:
        trail_points.pop(0)

    # Render
    screen.fill(BACKGROUND_COLOR)

    # Draw the trail for the line
    if len(trail_points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, trail_points, 3)

    # Draw line from the center to line1_end
    pygame.draw.line(screen, (255, 255, 255), center, line1_end, 2)
    pygame.draw.circle(screen, (255, 255, 255), line1_end, 10)
    pygame.draw.circle(screen, (20, 20, 20), line1_end, 8)

    # Draw line from line1_end to line2_end
    pygame.draw.line(screen, (255, 255, 255), line1_end, line2_end, 2)
    pygame.draw.circle(screen, (255, 255, 255), line2_end, 10)
    pygame.draw.circle(screen, (20, 20, 20), line2_end, 8)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(999999999999999999999)

# Quit Pygame
pygame.quit()