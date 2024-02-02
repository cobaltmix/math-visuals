import pygame
import math
from pygame.locals import *

# Initialize pygame
pygame.init()
# Add this after initializing pygame
pygame.font.init()  # Initialize the font module
font = pygame.font.SysFont("Arial", 80)  # Create a Font object

# Constants
WIDTH, HEIGHT = 2000, 1200
CENTER = (WIDTH // 2, HEIGHT // 2)
LARGE_CIRCLE_RADIUS = HEIGHT // 2.2
GRAVITY = 0.06
FRICTION = 1
MIN_SPLIT_SPEED = 40
BALL_SPLIT_COOLDOWN = 1000  # Number of frames to wait before ball can split again
MAX_BALLS = 10000
# Load the sound
collision_sound = pygame.mixer.Sound("bounce.wav")
# You can optionally initialize more channels if needed
pygame.mixer.set_num_channels(100000)

# Colors
RAINBOW_COLORS = [
    (255, 0, 0),  # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (75, 0, 130),  # Indigo
    (143, 0, 255),  # Violet
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls Simulation")
clock = pygame.time.Clock()


# Ball class
class Ball:
    def __init__(self, radius, color, position, velocity, cooldown=0, sound=None):
        self.radius = radius
        self.color = color
        self.position = position
        self.velocity = velocity
        self.cooldown = cooldown  # Cooldown to prevent ball from splitting too quickly
        self.sound = sound

    def move(self, GRAVITY):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )
        # Apply gravity
        self.velocity = (
            self.velocity[0],
            self.velocity[1]
            + GRAVITY * (1 if self.position[1] < HEIGHT - self.radius else -1),
        )
        # Apply friction
        self.velocity = (
            self.velocity[0] * FRICTION,
            self.velocity[1]
            if self.position[1] < HEIGHT - self.radius
            else self.velocity[1] * FRICTION,
        )
        # Cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position[0]), int(self.position[1])),
            self.radius,
        )

    def bounce(self, GRAVITY):
        collision_occurred = False
        distance_from_center = math.hypot(
            self.position[0] - CENTER[0], self.position[1] - CENTER[1]
        )


        if distance_from_center + self.radius > LARGE_CIRCLE_RADIUS:



            collision_occurred = True
            self.cooldown = BALL_SPLIT_COOLDOWN  # Activate cooldown to prevent immediate re-splitting

            # Calculate normal of collision
            collision_normal = (
                self.position[0] - CENTER[0],
                self.position[1] - CENTER[1],
            )
            normal_length = math.hypot(*collision_normal)
            collision_normal = (
                collision_normal[0] / normal_length,
                collision_normal[1] / normal_length,
            )

            # Rotate the collision normal by a small angle to increase the bounce angle
            # Determine rotation direction (clockwise or counter-clockwise) based on velocity
            rotation_angle = (
                math.pi / 12
            )  # Adjust this angle to change the bounce strength
            rotation_direction = -math.copysign(
                1,
                self.velocity[0] * collision_normal[1]
                - self.velocity[1] * collision_normal[0],
            )
            sin_angle = math.sin(rotation_angle * rotation_direction)
            cos_angle = math.cos(rotation_angle * rotation_direction)
            modified_normal = (
                cos_angle * collision_normal[0] - sin_angle * collision_normal[1],
                sin_angle * collision_normal[0] + cos_angle * collision_normal[1],
            )

            # Reflect the velocity vector over the modified normal
            dot_product = sum(v * n for v, n in zip(self.velocity, modified_normal))
            self.velocity = [
                v - 2 * dot_product * n for v, n in zip(self.velocity, modified_normal)
            ]

            # Move the ball to the edge of the large circle if it's overlapping
            overlap = distance_from_center + self.radius - LARGE_CIRCLE_RADIUS
            self.position = [
                p - overlap * n for p, n in zip(self.position, modified_normal)
            ]

            # Play sound if provided
            if self.sound:
                # Try to play the sound on any available channel
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.sound)

        return collision_occurred


def run_simulation(GRAVITY):
    running = True

    # Start with a single big ball
    initial_radius = 100
    initial_color_index = 0
    balls = [Ball(initial_radius, RAINBOW_COLORS[initial_color_index], (CENTER[0], CENTER[1] + initial_radius + 10), (3, -4))]
    color_index = (initial_color_index + 1) % len(RAINBOW_COLORS)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Array to accumulate the new set of balls for the next frame
        new_balls = []

        for ball in balls:
            ball.move(GRAVITY)
            if ball.cooldown > 0:
                ball.cooldown -= 1

            collision_occurred = ball.bounce(GRAVITY)

            # Check for collision and if the ball can split (no cooldown and not too small)
            if collision_occurred and ball.cooldown == 0 and len(balls) <= MAX_BALLS:
                color = RAINBOW_COLORS[color_index]
                color_index = (color_index + 1) % len(RAINBOW_COLORS)

                # Conditions for splitting the ball
                if ball.radius > 5:
                    new_radius = ball.radius // 2

                    velocity_magnitude = math.hypot(*ball.velocity)
                    if velocity_magnitude > MIN_SPLIT_SPEED:
                        angle_offset = math.pi / 90  # Offset by about 2 degrees

                        for offset in (-angle_offset, angle_offset):
                            new_angle = math.atan2(ball.velocity[1], ball.velocity[0]) + offset
                            new_velocity = (
                                velocity_magnitude * math.cos(new_angle) / 2,
                                velocity_magnitude * math.sin(new_angle) / 2,
                            )
                            new_balls.append(
                                Ball(
                                    new_radius,
                                    color,
                                    ball.position,
                                    new_velocity,
                                    BALL_SPLIT_COOLDOWN,
                                    collision_sound,
                                )
                            )
                else:
                    # If the ball is too small to split, just add it back to the list
                    new_balls.append(ball)
            else:
                new_balls.append(ball)

        balls = new_balls  # Replace the current list of balls with the updated list

        screen.fill((255, 255, 255))  # White background
        pygame.draw.circle(screen, (0, 0, 0), CENTER, LARGE_CIRCLE_RADIUS, 4)  # Draw the large circle
        for ball in balls:
            ball.draw(screen)  # Draw all the balls

        # Render gravity value text
        gravity_text = font.render(f"Gravity: {GRAVITY:.3f}", True, (0, 0, 0))
        text_rect = gravity_text.get_rect()
        text_rect.topright = (WIDTH - 100, 100)  # 10-pixel margin from the top right corner
        screen.blit(gravity_text, text_rect)  # Blit the text

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


run_simulation(GRAVITY)