import pygame
import math
import random

# Initialize pygame
pygame.init()
TRAIL_COLOR = (255, 255, 255)
# Constants
WIDTH, HEIGHT = 2000, 1200  # Screen dimensions
DARK_GREY = (50, 50, 50)  # Background color
PLANET_COLORS = {  # Colors for planets
    "Sun": (255, 255, 0),
    "Mercury": (169, 169, 169),
    "Venus": (255, 140, 0),
    "Earth": (70, 130, 180),
    "Mars": (188, 143, 143),
    "Jupiter": (204, 166, 61),
    "Saturn": (131, 105, 83),
    "Uranus": (97, 202, 255),
    "Neptune": (50, 89, 168),
}

# Initialize Pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()
distance_multiplier = 3
RED_TINT_COLOR = (255, 50, 50)  # Semi-transparent red color for the asteroid belt tint

# Solar System bodies data (doubling the orbital speed for faster rotation)
speed_multiplier = 3  # Change this factor to scale the speed of the planets
solar_system_data = {
    "Sun": {
        "radius": 20,
        "distance": 0,
        "angle": 0,
        "color": PLANET_COLORS["Sun"],
        "orbital_speed": 0 * speed_multiplier,
    },
    "Mercury": {
        "radius": 2,
        "distance": 30 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Mercury"],
        "orbital_speed": 0.0016 * speed_multiplier,
    },
    "Venus": {
        "radius": 4,
        "distance": 50 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Venus"],
        "orbital_speed": 0.0012 * speed_multiplier,
    },
    "Earth": {
        "radius": 4,
        "distance": 70 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Earth"],
        "orbital_speed": 0.001 * speed_multiplier,
    },
    "Mars": {
        "radius": 3,
        "distance": 100 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Mars"],
        "orbital_speed": 0.0008 * speed_multiplier,
    },
    "Jupiter": {
        "radius": 10,
        "distance": 200 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Jupiter"],
        "orbital_speed": 0.0004 * speed_multiplier,
    },
    "Saturn": {
        "radius": 8,
        "distance": 360 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Saturn"],
        "orbital_speed": 0.0003 * speed_multiplier,
    },
    "Uranus": {
        "radius": 6,
        "distance": 500 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Uranus"],
        "orbital_speed": 0.0002 * speed_multiplier,
    },
    "Neptune": {
        "radius": 6,
        "distance": 600 * distance_multiplier,
        "angle": 0,
        "color": PLANET_COLORS["Neptune"],
        "orbital_speed": 0.0001 * speed_multiplier,
    },
    "Earth_Moon": {
        "radius": 1,
        "distance": 10,
        "angle": 0,
        "color": (200, 200, 200),
        "orbital_speed": 0.002 * speed_multiplier,
        "parent": "Earth",
    },
    "Mars_Phobos": {
        "radius": 1,
        "distance": 5,
        "angle": 0,
        "color": (150, 150, 150),
        "orbital_speed": 0.003 * speed_multiplier,
        "parent": "Mars",
    },
    "Mars_Deimos": {
        "radius": 0.8,
        "distance": 8,
        "angle": 0,
        "color": (150, 150, 150),
        "orbital_speed": 0.0035 * speed_multiplier,
        "parent": "Mars",
    },
}

# Constants for elliptical orbits
DWARF_PLANET_COLORS = {
    "Pluto": (190, 178, 174),
    "Eris": (255, 255, 255),
    "Haumea": (221, 228, 202),
    "Makemake": (239, 222, 205),
}

# Adjusted constants for more elliptical orbits
dwarf_planet_data = {
    "Pluto": {
        "radius": 1,
        "semi_major_axis": 700 * distance_multiplier,
        "semi_minor_axis": 550 * distance_multiplier,
        "angle": 0,
        "color": DWARF_PLANET_COLORS["Pluto"],
        "orbital_speed": 0.00009 * speed_multiplier,
    },
    "Eris": {
        "radius": 1,
        "semi_major_axis": 800 * distance_multiplier,
        "semi_minor_axis": 600 * distance_multiplier,
        "angle": 0,
        "color": DWARF_PLANET_COLORS["Eris"],
        "orbital_speed": 0.00008 * speed_multiplier,
    },
    "Haumea": {
        "radius": 1,
        "semi_major_axis": 850 * distance_multiplier,
        "semi_minor_axis": 630 * distance_multiplier,
        "angle": 0,
        "color": DWARF_PLANET_COLORS["Haumea"],
        "orbital_speed": 0.00007 * speed_multiplier,
    },
    "Makemake": {
        "radius": 1,
        "semi_major_axis": 900 * distance_multiplier,
        "semi_minor_axis": 650 * distance_multiplier,
        "angle": 0,
        "color": DWARF_PLANET_COLORS["Makemake"],
        "orbital_speed": 0.00006 * speed_multiplier,
    },
}
solar_system_data.update(dwarf_planet_data)


# Constants for the asteroid belt
ASTEROID_COUNT = 2000  # The number of simulated asteroids - adjust as necessary
INNER_BELT_RADIUS = 115 * distance_multiplier  # Inner radius of the asteroid belt
OUTER_BELT_RADIUS = 180 * distance_multiplier  # Outer radius of the asteroid belt
ASTEROID_COLOR = (169, 169, 169)  # Grey color for asteroids

# Generate random positions for the simulated asteroids in the belt
asteroid_belt_data = [
    {
        "radius": random.uniform(1, 5),  # Random size for visual variety
        "distance": random.uniform(
            INNER_BELT_RADIUS, OUTER_BELT_RADIUS
        ),  # Random orbital range
        "angle": random.uniform(0, 2 * math.pi),  # Random angle around the sun
        "orbital_speed": random.uniform(0.0005, 0.0009)
        * speed_multiplier,  # Random orbital speed
    }
    for _ in range(ASTEROID_COUNT)
]

# Random distance and speed range constants
MIN_MOON_DISTANCE = 10
MAX_MOON_DISTANCE = 80  # Adjusted to fit greater moon count for Saturn
MIN_ORBITAL_SPEED = 0.001
MAX_ORBITAL_SPEED = 0.004

# Constants for the Kuiper Belt
KUIPER_BELT_INNER_RADIUS = (
    30 * 75
)  # Inner radius of the Kuiper Belt in our simulation scale
KUIPER_BELT_OUTER_RADIUS = (
    30 * 75 + 25 * 75
)  # Outer radius of the Kuiper Belt in our simulation scale
KUIPER_BELT_COLOR = (
    0,
    255,
    0,
    64,
)  # Semi-transparent green color for the Kuiper Belt tint


def generate_moon_data(planet_name, moon_count):
    moon_data = {}
    # Ensure the range can accommodate the specified moon count
    distances = [
        MIN_MOON_DISTANCE + i * (MAX_MOON_DISTANCE - MIN_MOON_DISTANCE) // moon_count
        for i in range(moon_count)
    ]
    speeds = [
        random.uniform(MIN_ORBITAL_SPEED, MAX_ORBITAL_SPEED) for _ in range(moon_count)
    ]

    for i in range(moon_count):
        moon_data[f"{planet_name}_Moon{i+1}"] = {
            "radius": 0.4 + (i % 3) * 0.1,  # Arbitrary radius scaling
            "distance": distances[
                i
            ],  # Use the calculated distance to keep moons separate
            "angle": random.uniform(
                0, 2 * math.pi
            ),  # Random initial angle for varied orbits
            "color": (200, 200, 200),  # Grey color for all moons
            "orbital_speed": speeds[i] * speed_multiplier,  # Random orbital speed
            "parent": planet_name,
        }
    return moon_data


solar_system_data.update(generate_moon_data("Neptune", 14))
solar_system_data.update(generate_moon_data("Uranus", 27))
solar_system_data.update(generate_moon_data("Saturn", 146))
solar_system_data.update(generate_moon_data("Jupiter", 95))


# Trails for the planets
planet_trails = {name: [] for name in solar_system_data.keys()}
# Initial zoom and pan data
zoom = 1.0
pan_offset_x, pan_offset_y = WIDTH / 2, HEIGHT / 2
panning = False
trail_length = 2000


def draw_rings(planet, thickness, inner_radius, outer_radius):
    center_x, center_y = planet["distance"] * math.cos(planet["angle"]), planet[
        "distance"
    ] * math.sin(planet["angle"])
    center_x = center_x * zoom + pan_offset_x
    center_y = center_y * zoom + pan_offset_y

    for radius in range(inner_radius, outer_radius, thickness):
        # Apply the zoom factor to the radius, thickness remains unchanged as it's a pixel value
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(center_x), int(center_y)),
            int(radius * zoom),
            thickness,
        )


# Function to draw a planet and its trail
def draw_planet(planet, trail):
    # Check if the planet has an elliptical orbit
    if "semi_major_axis" in planet and "semi_minor_axis" in planet:
        # Calculate position on the ellipse using the parametric equations
        real_x = planet["semi_major_axis"] * math.cos(planet["angle"])
        real_y = planet["semi_minor_axis"] * math.sin(planet["angle"])
    else:
        # Circular orbit
        real_x = planet["distance"] * math.cos(planet["angle"])
        real_y = planet["distance"] * math.sin(planet["angle"])

    x = real_x * zoom + pan_offset_x
    y = real_y * zoom + pan_offset_y
    px, py = int(x), int(y)

    pygame.draw.circle(screen, planet["color"], (px, py), int(planet["radius"] * zoom))

    trail.append((real_x, real_y))
    if len(trail) > trail_length:
        del trail[0]

    trail_with_zoom_pan = [
        (int(point[0] * zoom + pan_offset_x), int(point[1] * zoom + pan_offset_y))
        for point in trail
    ]
    if len(trail_with_zoom_pan) > 1:
        pygame.draw.lines(screen, TRAIL_COLOR, False, trail_with_zoom_pan, 1)


def draw_asteroid_belt(
    screen, pan_offset_x, pan_offset_y, zoom, inner_radius, outer_radius
):
    # Create a new Surface with per-pixel alpha to draw the semi-transparent circle
    belt_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Generate points for the inner and outer edges of the asteroid belt
    inner_edge_points = []
    outer_edge_points = []
    # Draw for a bit more than 360 degrees for overlap
    for angle in range(0, 361, 1):  # Go up to 361 for a slight overlap
        rad_angle = math.radians(angle)
        inner_x = pan_offset_x + int(math.cos(rad_angle) * inner_radius * zoom)
        inner_y = pan_offset_y + int(math.sin(rad_angle) * inner_radius * zoom)
        inner_edge_points.append((inner_x, inner_y))

    for angle in range(360, -1, -1):  # Go in reverse for outer edge.
        rad_angle = math.radians(angle)
        outer_x = pan_offset_x + int(math.cos(rad_angle) * outer_radius * zoom)
        outer_y = pan_offset_y + int(math.sin(rad_angle) * outer_radius * zoom)
        outer_edge_points.append((outer_x, outer_y))

    # Combine the edge points and draw the polygon for the belt
    all_points = inner_edge_points + outer_edge_points
    pygame.draw.polygon(belt_surface, RED_TINT_COLOR + (128,), all_points)

    # Blit this surface onto the main screen surface
    screen.blit(belt_surface, (0, 0))

    # Draw the asteroids on the main screen surface
    for asteroid in asteroid_belt_data:
        real_x = asteroid["distance"] * math.cos(asteroid["angle"])
        real_y = asteroid["distance"] * math.sin(asteroid["angle"])
        x = real_x * zoom + pan_offset_x
        y = real_y * zoom + pan_offset_y
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pygame.draw.circle(
                screen, ASTEROID_COLOR, (int(x), int(y)), int(asteroid["radius"] * zoom)
            )


def draw_kuiper_belt(screen, pan_offset_x, pan_offset_y, zoom):
    kuiper_belt_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Generate points for the inner and outer edges of the Kuiper Belt
    kuiper_inner_edge_points = []
    kuiper_outer_edge_points = []
    for angle in range(0, 361):  # Go up to 361 for a slight overlap
        rad_angle = math.radians(angle)
        inner_x = pan_offset_x + int(
            math.cos(rad_angle) * KUIPER_BELT_INNER_RADIUS * zoom
        )
        inner_y = pan_offset_y + int(
            math.sin(rad_angle) * KUIPER_BELT_INNER_RADIUS * zoom
        )
        kuiper_inner_edge_points.append((inner_x, inner_y))

        outer_x = pan_offset_x + int(
            math.cos(rad_angle) * KUIPER_BELT_OUTER_RADIUS * zoom
        )
        outer_y = pan_offset_y + int(
            math.sin(rad_angle) * KUIPER_BELT_OUTER_RADIUS * zoom
        )
        kuiper_outer_edge_points.append((outer_x, outer_y))

    # Combine the edge points and draw the polygon for the belt
    all_points = kuiper_inner_edge_points + kuiper_outer_edge_points[::-1]
    pygame.draw.polygon(kuiper_belt_surface, KUIPER_BELT_COLOR, all_points)

    # Blit this Surface onto the main screen Surface
    screen.blit(kuiper_belt_surface, (0, 0))


# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                panning = True
                pan_start_x, pan_start_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                panning = False
        elif event.type == pygame.MOUSEMOTION:
            if panning:
                mouse_x, mouse_y = event.pos
                pan_offset_x += mouse_x - pan_start_x
                pan_offset_y += mouse_y - pan_start_y
                pan_start_x, pan_start_y = mouse_x, mouse_y
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:  # Scroll up
                zoom *= 1.1
            elif event.y == -1:  # Scroll down
                zoom /= 1.1

        # Clear the screen
    screen.fill(DARK_GREY)
    # Draw the asteroid belt
    draw_asteroid_belt(
        screen, pan_offset_x, pan_offset_y, zoom, INNER_BELT_RADIUS, OUTER_BELT_RADIUS
    )

    # Draw the Kuiper Belt tint
    draw_kuiper_belt(screen, pan_offset_x, pan_offset_y, zoom)

    for asteroid in asteroid_belt_data:
        asteroid["angle"] += asteroid["orbital_speed"]

    # Update and draw each planet and their trails
    for name, planet_data in solar_system_data.items():
        parent_name = planet_data.get("parent")
        if parent_name:
            parent_planet = solar_system_data[parent_name]
            planet_data["angle"] += planet_data["orbital_speed"]
            orbit_x = parent_planet["distance"] * math.cos(
                parent_planet["angle"]
            ) + planet_data["distance"] * math.cos(planet_data["angle"])
            orbit_y = parent_planet["distance"] * math.sin(
                parent_planet["angle"]
            ) + planet_data["distance"] * math.sin(planet_data["angle"])
            x = orbit_x * zoom + pan_offset_x
            y = orbit_y * zoom + pan_offset_y
            px, py = int(x), int(y)
            pygame.draw.circle(
                screen,
                planet_data["color"],
                (px, py),
                int(planet_data["radius"] * zoom),
            )
        else:
            planet_data["angle"] += planet_data["orbital_speed"]
            draw_planet(planet_data, planet_trails[name])

    # Draw rings for Saturn and Uranus with adjusted zoom
    saturn_data = solar_system_data["Saturn"]
    uranus_data = solar_system_data["Uranus"]
    neptune_data = solar_system_data["Neptune"]
    draw_rings(saturn_data, 1, saturn_data["radius"] + 6, saturn_data["radius"] + 9)
    draw_rings(uranus_data, 1, uranus_data["radius"] + 5, uranus_data["radius"] + 7)
    draw_rings(neptune_data, 1, neptune_data["radius"] + 4, neptune_data["radius"] + 5)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(1000)

pygame.quit()
