import pygame
from math import sin, cos, pi
import numpy as np

import matplotlib

# Generate a colormap for smooth color transition
from matplotlib.colors import LinearSegmentedColormap

# Define your colors
colors = [(255, 0, 0), (0, 0, 255), (255, 165, 0)]
# Normalize the RGB values to the range [0, 1], as required by LinearSegmentedColormap
colors = [(r/255.0, g/255.0, b/255.0) for r, g, b in colors]
cmap = LinearSegmentedColormap.from_list('pendulum_cmap', colors, N=20000)

# Constants for visualization
WIDTH, HEIGHT = 2000, 1200
OFFSET_X, OFFSET_Y = WIDTH // 2, HEIGHT // 2

# Physics constants
LENGTH1, LENGTH2 = 2, 2
MASS1, MASS2 = 2, 2
GRAVITY = -100
SCALE = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Pendulums Simulation")
clock = pygame.time.Clock()
running = True
is_running_simulation = True

# Colors
colors = [(255, 0, 0), (0, 255, 255),(0, 255, 0), (0, 0, 255), (255, 165, 0)]

# Pre-calculate cos and sin for theta_1 and theta_2
theta_1_radians = np.linspace(0.1, 0.1 + 0.000001 * 9999, 10000)
theta_2_radians = theta_1_radians.copy()  # They start the same
cos_theta_1 = np.cos(theta_1_radians)
sin_theta_1 = np.sin(theta_1_radians)
cos_theta_2 = np.cos(theta_2_radians)
sin_theta_2 = np.sin(theta_2_radians)

# Omega (angular velocity) initialization
omega_1 = np.zeros(10000)
omega_2 = np.zeros(10000)

# Pre-calculate constant expressions and denominators
m1_plus_m2 = MASS1 + MASS2
l1_m2 = LENGTH1 * MASS2
l2_m1_plus_m2_inv = LENGTH2 / (m1_plus_m2 * LENGTH1)
gravity_sin_theta_2 = GRAVITY * sin_theta_2
gravity_sin_theta_1 = GRAVITY * sin_theta_1
l1_omega_1_sqrd = l1_m2 * omega_1 ** 2
l2_omega_2_sqrd = LENGTH2 * omega_2 ** 2
m2_g_sin_theta_2_cos_theta_1 = MASS2 * gravity_sin_theta_2 * cos_theta_1
m1_plus_m2_g_sin_theta_1_cos_theta_2 = m1_plus_m2 * gravity_sin_theta_1 * cos_theta_2
dt = 0.01

def calculate_double_pendulum(theta_1, theta_2, omega_1, omega_2, dt, LENGTH1, LENGTH2, MASS1, MASS2, GRAVITY):
    # Constants
    g_over_l1 = GRAVITY / LENGTH1
    g_over_l2 = GRAVITY / LENGTH2
    m1_plus_m2 = MASS1 + MASS2

    # Intermediate calculations for angular accelerations
    sin_1 = np.sin(theta_1)
    sin_2 = np.sin(theta_2)
    sin_12 = np.sin(theta_1 - theta_2)
    cos_12 = np.cos(theta_1 - theta_2)

    # Equations of motion derived using Lagrangian mechanics
    denom = (m1_plus_m2 - MASS2 * cos_12**2)

    omega_1_deriv = (MASS2 * g_over_l1 * sin_2 * cos_12 - MASS2 * sin_12 * (LENGTH1 * omega_1**2 * cos_12 + LENGTH2 * omega_2**2) -
                    m1_plus_m2 * g_over_l1 * sin_1) / (LENGTH1 * denom)

    omega_2_deriv = (m1_plus_m2 * (LENGTH1 * omega_1**2 * sin_12 - g_over_l2 * sin_2 + g_over_l2 * sin_1 * cos_12) +
                    MASS2 * LENGTH2 * omega_2**2 * sin_12 * cos_12) / (LENGTH2 * denom)

    # Integrate angular accelerations to get velocities
    omega_1 += omega_1_deriv * dt
    omega_2 += omega_2_deriv * dt

    # Integrate angular velocities to get angles
    theta_1 += omega_1 * dt
    theta_2 += omega_2 * dt

    return theta_1, theta_2, omega_1, omega_2

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                is_running_simulation = not is_running_simulation

    if is_running_simulation:

        if is_running_simulation:
            theta_1_radians, theta_2_radians, omega_1, omega_2 = calculate_double_pendulum(
                theta_1_radians, theta_2_radians, omega_1, omega_2, dt, LENGTH1, LENGTH2, MASS1, MASS2, GRAVITY)
        # Update omega and theta values
        delta_theta = theta_2_radians - theta_1_radians
        cos_delta_theta = np.cos(delta_theta)
        sin_delta_theta = np.sin(delta_theta)

        den1 = (m1_plus_m2 * LENGTH1) - (MASS2 * LENGTH1 * cos_delta_theta ** 2)

        # Calculate omega derivatives
        omega_1_deriv = (l1_omega_1_sqrd * sin_delta_theta * cos_delta_theta +
                         m2_g_sin_theta_2_cos_theta_1 +
                         l2_omega_2_sqrd * sin_delta_theta -
                         m1_plus_m2 * gravity_sin_theta_1) / den1

        den2 = (LENGTH2 / LENGTH1) * den1
        omega_2_deriv = (-l2_omega_2_sqrd * sin_delta_theta * cos_delta_theta +  # Corrected line
                         m1_plus_m2_g_sin_theta_1_cos_theta_2 -
                         m1_plus_m2 * l1_omega_1_sqrd * sin_delta_theta -
                         m1_plus_m2 * gravity_sin_theta_2) / den2



        # Calculate positions
        x1 = LENGTH1 * SCALE * np.sin(theta_1_radians) + OFFSET_X
        y1 = -LENGTH1 * SCALE * np.cos(theta_1_radians) + OFFSET_Y
        x2 = x1 + LENGTH2 * SCALE * np.sin(theta_2_radians)
        y2 = y1 - LENGTH2 * SCALE * np.cos(theta_2_radians)

        # Just update the entire screen rather than each pendulum
        screen.fill((0, 0, 0))
        for i in range(10000):
            # Get interpolated color from the colormap
            pendulum_color = cmap(i)[:3]  # Drop the alpha value
            pendulum_color = [int(c * 255) for c in pendulum_color]  # Convert to RGB format
            pygame.draw.line(screen, pendulum_color, (OFFSET_X, OFFSET_Y), (x1[i], y1[i]), 1)
            pygame.draw.line(screen, pendulum_color, (x1[i], y1[i]), (x2[i], y2[i]), 1)
        pygame.display.flip()
    clock.tick(600000000)

pygame.quit()