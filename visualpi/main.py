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

# Function to compute the position of the line end based on the angle and length
def calculate_end_point(start_x, start_y, angle, length):
    end_x = start_x + length * math.cos(angle)
    end_y = start_y + length * math.sin(angle)
    return end_x, end_y

# Function to compute the complex rotation speeds based on the function z(theta)
def z(theta):
    return cmath.exp(math.cos(theta) *2j) + cmath.exp(math.pi ** math.sin(theta) * 2j)

# Fixed line lengths
length_line1 = 300
length_line2 = 200

# Initial angles for the lines (radians)
angle_line1 = 0
angle_line2 = 0

# Initial theta
theta = 0

# Trail for the second line
trail_points = []
max_trail_length = 300000

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Compute the complex rotation speeds
    complex_speed = z(theta)
    rotation_speed_1 = complex_speed.real * 0.02
    rotation_speed_2 = complex_speed.imag * 0.03

    # Calculate the new angles for the lines, ensuring they're within the range [0, 2*pi)
    angle_line1 = (angle_line1 + rotation_speed_1) % (2 * math.pi)
    angle_line2 = (angle_line2 + rotation_speed_2) % (2 * math.pi)
    # Update theta for the next frame
    theta += 0.01

    # Calculate the new angles for the lines
    angle_line1 = (angle_line1 + rotation_speed_1) % (2*math.pi)
    angle_line2 = (angle_line2 + rotation_speed_2) % (2*math.pi)

    # Calculate the end points for the lines
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    end_x1, end_y1 = calculate_end_point(center_x, center_y, angle_line1, length_line1)
    end_x2, end_y2 = calculate_end_point(end_x1, end_y1, angle_line2, length_line2)

    # Add the current end position of line 2 to the trail
    trail_points.append((end_x2, end_y2))
    if len(trail_points) > max_trail_length:
        trail_points.pop(0)

    # Render
    screen.fill(BACKGROUND_COLOR)

    # Draw line 1
    pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (end_x1, end_y1), 2)

    # Draw line 2
    pygame.draw.line(screen, (0, 255, 0), (end_x1, end_y1), (end_x2, end_y2), 2)

    # Draw the trail for the second line
    if len(trail_points) > 1:
        pygame.draw.lines(screen, (0, 0, 255), False, trail_points, 2)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(1000)

# Quit Pygame
pygame.quit()