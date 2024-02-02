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
GRAVITY = 0
FRICTION = 1
MIN_SPLIT_SPEED = 40
BALL_SPLIT_COOLDOWN = 1000  # Number of frames to wait before ball can split again
MAX_BALLS = 10000
# Load the sound
collision_sound = pygame.mixer.Sound("bounce.wav")
# You can optionally initialize more channels if needed
pygame.mixer.set_num_channels(100000)
# Constants for black hole
BLACK_HOLE_RADIUS = 50
BLACK_HOLE_GRAVITY_STRENGTH = 15  # Adjust the strength of the black hole's gravity

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

    def move(self):
        # Regular gravity effect (comment this part out if you don't want regular gravity)
        self.velocity = (
            self.velocity[0],
            self.velocity[1]
            + GRAVITY * (1 if self.position[1] < HEIGHT - self.radius else -1),
        )

        # Black hole gravity effect
        direction_to_center = (
            CENTER[0] - self.position[0],
            CENTER[1] - self.position[1],
        )
        distance_to_center = math.hypot(*direction_to_center)

        # Normalize the direction vector
        direction_to_center = (
            direction_to_center[0] / distance_to_center,
            direction_to_center[1] / distance_to_center,
        )

        # Only apply black hole gravity if the distance is larger than BLACK_HOLE_RADIUS
        if distance_to_center > BLACK_HOLE_RADIUS:
            # Calculate force magnitude (gravity strength inversely proportional to distance squared, constrained to a minimum distance)
            force_magnitude = (
                BLACK_HOLE_GRAVITY_STRENGTH
                * (self.radius**2)
                / max(distance_to_center, self.radius) ** 2
            )

            # Apply black hole gravity towards the center
            self.velocity = (
                self.velocity[0] + force_magnitude * direction_to_center[0],
                self.velocity[1] + force_magnitude * direction_to_center[1],
            )

        # Update ball position with the new velocity
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )

        # Apply friction
        self.velocity = (
            self.velocity[0] * FRICTION,
            self.velocity[1]
            if self.position[1] < HEIGHT - self.radius
            else self.velocity[1] * FRICTION,
        )

        # Prevent the ball from passing into the black hole by resetting its position
        if distance_to_center - self.radius < BLACK_HOLE_RADIUS:
            # Place the ball just outside the black hole's radius
            overlap = self.radius + distance_to_center - BLACK_HOLE_RADIUS
            self.position = (
                self.position[0] - overlap * direction_to_center[0],
                self.position[1] - overlap * direction_to_center[1],
            )
            # Invert the velocity to simulate a bounce from the black hole's edge
            self.velocity = (-self.velocity[0], -self.velocity[1])

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position[0]), int(self.position[1])),
            self.radius,
        )

    def bounce(self):
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
    # Start with a single ball with an upward velocity to ensure it will hit the circle's border
    balls = [Ball(10, RAINBOW_COLORS[0], (CENTER[0]-100, CENTER[1] + 50), (3, -4))]
    color_index = 1

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Array to accumulate the new set of balls for the next frame
        new_balls = []

        for ball in balls:
            ball.move()
            if ball.cooldown > 0:
                ball.cooldown -= 1

            collision_occurred = ball.bounce()

            if (
                collision_occurred
                and ball.cooldown == BALL_SPLIT_COOLDOWN
                and len(balls) <= MAX_BALLS
            ):
                color = RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
                color_index += 1

                velocity_magnitude = math.hypot(*ball.velocity)
                velocity_angle = math.atan2(ball.velocity[1], ball.velocity[0])

                # Split the ball at slightly different angles
                angle_offset = math.pi / 90  # Offset by 15 degrees
                for offset in (-angle_offset, angle_offset):
                    new_angle = velocity_angle + offset
                    new_velocity = (
                        velocity_magnitude * math.cos(new_angle),
                        velocity_magnitude * math.sin(new_angle),
                    )
                    new_balls.append(
                        Ball(
                            ball.radius,
                            color,
                            ball.position,
                            new_velocity,
                            BALL_SPLIT_COOLDOWN,
                            collision_sound,
                        )
                    )

            elif ball.cooldown < BALL_SPLIT_COOLDOWN:
                new_balls.append(ball)

        balls = new_balls  # Replace the current list of balls with the updated list

        screen.fill((255, 255, 255))  # White background
        pygame.draw.circle(
            screen, (0, 0, 0), CENTER, LARGE_CIRCLE_RADIUS, 4
        )  # Draw the large circle
        for ball in balls:
            ball.draw(screen)  # Draw all the balls
            # Draw the black hole
        pygame.draw.circle(screen, (0, 0, 0), CENTER, BLACK_HOLE_RADIUS)

        # # Render gravity value text
        # gravity_text = font.render(f"Gravity: {GRAVITY:.3f}", True, (0, 0, 0))
        # text_rect = gravity_text.get_rect()
        # text_rect.topright = (
        #     WIDTH - 100,
        #     100,
        # )  # 10-pixel margin from the top right corner
        # screen.blit(gravity_text, text_rect)  # Blit the text

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


run_simulation(GRAVITY)
