import pygame
from math import sin, cos, radians
import numpy as np
import random

# Constants for visualization from the first file
WIDTH, HEIGHT = 2000, 1200           # Width and height of the window
OFFSET_X, OFFSET_Y = WIDTH // 2, HEIGHT // 2  # Where to draw the first pendulum

# Physics constants from the first file
LENGTH1 = 2  # Length of the first pendulum rod in meters
LENGTH2 = 2  # Length of the second pendulum rod in meters
MASS1 = 2    # Mass of the first pendulum bob in kilograms
MASS2 = 2   # Mass of the second pendulum bob in kilograms
GRAVITY = -150  # Gravitational acceleration in m/s^2
SCALE = 100  # Pixels per meter for drawing scale

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Pendulums Simulation")
clock = pygame.time.Clock()
running = True
is_running_simulation = True

# Colors from the first file with orange, pink, and purple added
colors = [
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
]

def interpolate_color(t):
    # Determine which colors to interpolate between based on t
    num_colors = len(colors)
    scaled_t = t * (num_colors - 1)
    first_color_index = int(scaled_t)
    second_color_index = min(first_color_index + 1, num_colors - 1)
    local_t = scaled_t - first_color_index

    # Get the starting and ending color for this segment
    color_start = colors[first_color_index]
    color_end = colors[second_color_index]

    # Interpolate between the two colors in this segment
    return tuple(int(color_start[i] + (color_end[i] - color_start[i]) * local_t) for i in range(3))

# Link class from the second file
class Link:
    def __init__(self, mass, length, theta_0, omega_0):
        self.mass = mass
        self.length = length
        self.theta = theta_0
        self.omega = omega_0

# DoublePendulum class from the second file
class DoublePendulum:
    def __init__(self, link1, link2, color):
        self.link1 = link1
        self.link2 = link2
        self.color = color

    def get_positions(self):
        x1 = self.link1.length * SCALE * sin(self.link1.theta) + OFFSET_X
        y1 = -self.link1.length * SCALE * cos(self.link1.theta) + OFFSET_Y  # Notice the minus sign to invert y-axis
        x2 = x1 + self.link2.length * SCALE * sin(self.link2.theta)
        y2 = y1 - self.link2.length * SCALE * cos(self.link2.theta)         # Notice the minus sign to invert y-axis

        return (x1, y1), (x2, y2)

    def update(self, dt):
        l1, l2, m1, m2 = self.link1.length, self.link2.length, self.link1.mass, self.link2.mass
        theta1, omega1, theta2, omega2 = self.link1.theta, self.link1.omega, self.link2.theta, self.link2.omega

        # Equations of motion for a double pendulum
        delta_theta = theta2 - theta1
        den1 = (m1 + m2) * l1 - m2 * l1 * cos(delta_theta) ** 2

        omega1_deriv = (m2 * l1 * omega1 ** 2 * sin(delta_theta) * cos(delta_theta) +
                        m2 * GRAVITY * sin(theta2) * cos(delta_theta) +
                        m2 * l2 * omega2 ** 2 * sin(delta_theta) -
                        (m1 + m2) * GRAVITY * sin(theta1)) / den1

        den2 = (l2 / l1) * den1

        omega2_deriv = (-m2 * l2 * omega2 ** 2 * sin(delta_theta) * cos(delta_theta) +
                        (m1 + m2) * GRAVITY * sin(theta1) * cos(delta_theta) -
                        (m1 + m2) * l1 * omega1 ** 2 * sin(delta_theta) -
                        (m1 + m2) * GRAVITY * sin(theta2)) / den2

        # Update velocities and positions
        omega1 += omega1_deriv * dt
        theta1 += omega1 * dt
        omega2 += omega2_deriv * dt
        theta2 += omega2 * dt

        self.link1.theta, self.link1.omega, self.link2.theta, self.link2.omega = theta1, omega1, theta2, omega2

    def draw(self, surface):
        (x1, y1), (x2, y2) = self.get_positions()

        # Draw the rods and pendulums
        pygame.draw.line(surface, self.color, (OFFSET_X, OFFSET_Y), (x1, y1), 1)
        pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), 1)
# Create 200 Double Pendulum objects with initial conditions from the second file

pendulums = []
offset_increment = 0.000000001  # Radians to offset each pendulum by
for i in range(6000):
    theta_1 = 1.5 + (i * offset_increment)  # Apply offset to base angle theta_1
    theta_2 = 1.5 + (i * offset_increment)  # Apply offset to base angle theta_2
    link1 = Link(mass=MASS1, length=LENGTH1, theta_0=theta_1, omega_0=0)
    link2 = Link(mass=MASS2, length=LENGTH2, theta_0=theta_2, omega_0=0)
    pendulums.append(DoublePendulum(link1, link2, interpolate_color(i / 6000)))

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                is_running_simulation = not is_running_simulation

    # Simulation update
    if is_running_simulation:
        dt = 0.01
        for pendulum in pendulums:
            pendulum.update(dt)  # Update each pendulum

    # Drawing
    screen.fill((0,0,0))
    for pendulum in pendulums:
        pendulum.draw(screen)  # Draw each pendulum
    pygame.display.flip()  # Update display

    clock.tick(120)  # Run at 60 frames per second

# Exit Pygame
pygame.quit()