import pygame
import numpy as np
from math import sin, cos, pi

# Constants
LENGTH1 = 300  # Length of the first pendulum rod
LENGTH2 = 400  # Length of the second pendulum rod
MASS1 = 50     # Mass of the first pendulum bob
MASS2 = 50    # Mass of the second pendulum bob
GRAVITY = -150 # Gravitational acceleration
WIDTH, HEIGHT = 2000, 1200           # Width and height of the window
OFFSET_X, OFFSET_Y = WIDTH // 2, HEIGHT // 4  # Where to draw the first pendulum

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
running = True

# Define color interpolation function
def interpolate_color(color1, color2, t):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3))

# Define the start and end colors for interpolation
color1 = (255, 0, 0)  # Red
color2 = (0, 0, 255)  # Blue

def derivatives(state):
    theta1, omega1, theta2, omega2 = state
    delta_theta = theta2 - theta1

    # Regularize the sine value to avoid division by a value too close to zero
    sin_delta = sin(delta_theta)
    den1 = (2 * MASS1 + MASS2) - MASS2 * cos(2 * delta_theta)
    den2 = LENGTH1 * den1 - LENGTH2 * MASS2 * cos(delta_theta)

    num1 = -GRAVITY * (2 * MASS1 + MASS2) * sin(theta1) - MASS2 * GRAVITY * sin(theta1 - 2 * theta2)
    num1 -= 2 * sin_delta * MASS2 * (omega2 ** 2 * LENGTH2 + omega1 ** 2 * LENGTH1 * cos(delta_theta))

    num2 = 2 * sin_delta * ((omega1 ** 2 * LENGTH1 * (MASS1 + MASS2)) + GRAVITY * (MASS1 + MASS2) * cos(theta1) + omega2 ** 2 * LENGTH2 * MASS2 * cos(theta1 - theta2))

    domega1_dt = num1 / (LENGTH1 * den1)
    domega2_dt = num2 / (LENGTH2 * den2)

    return np.array([omega1, domega1_dt, omega2, domega2_dt])

def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + dt/2 * k1)
    k3 = derivatives(state + dt/2 * k2)
    k4 = derivatives(state + dt * k3)
    return state + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Initialize pendulums with slightly different starting angles
pendulums = []
for i in range(1000):
    theta1 = np.pi / 4 + i * 0.000001  # Initial angle for first pendulum
    theta2 = np.pi / 4 + i * 0.000001  # Initial angle for second pendulum
    omega1 = 0                     # Initial angular velocity for first pendulum
    omega2 = 0                     # Initial angular velocity for second pendulum
    pendulums.append(np.array([theta1, omega1, theta2, omega2]))

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Time step (Delta time)
    dt = 0.1


    # Update pendulum positions using RK4 integration
    for i in range(len(pendulums)):
        pendulums[i] = rk4_step(pendulums[i], dt)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw pendulums
    for i, (theta1, omega1, theta2, omega2) in enumerate(pendulums):
        x1 = OFFSET_X + LENGTH1 * sin(theta1)
        y1 = OFFSET_Y + LENGTH1 * cos(theta1)
        x2 = x1 + LENGTH2 * sin(theta2)
        y2 = y1 + LENGTH2 * cos(theta2)

        # Interpolate pendulum color based on its index
        t = i / len(pendulums)
        ball_color = interpolate_color(color1, color2, t)

        # Draw the rods
        pygame.draw.line(screen, ball_color, (OFFSET_X, OFFSET_Y), (x1, y1), 2)
        pygame.draw.line(screen, ball_color, (x1, y1), (x2, y2), 2)

    # Update the display
    pygame.display.flip()

    clock.tick(120)
# Clean up
pygame.quit()