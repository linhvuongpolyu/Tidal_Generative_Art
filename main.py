import pygame
import requests
from bs4 import BeautifulSoup
import math
import colorsys
import sys

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (10, 10, 30)
SPIRAL_COLOR = (0, 200, 255)
FPS = 60

TIDE_URL = "https://www.hko.gov.hk/tide/eCLKtext2027.html"


def fetch_tidal_data(url):
    """Fetch and parse tidal data from the given URL. Returns a list of (time, height) tuples."""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    data = []
    # Find the table with tidal data
    table = soup.find('table')
    if not table:
        return data
    for row in table.find_all('tr')[1:]:  # skip header
        cols = row.find_all('td')
        if len(cols) >= 2:
            time = cols[0].get_text(strip=True)
            try:
                height = float(cols[1].get_text(strip=True))
                data.append((time, height))
            except ValueError:
                continue
    return data


def normalize_heights(data, min_radius=80, max_radius=350):
    if not data:
        return []
    heights = [h for _, h in data]
    min_h, max_h = min(heights), max(heights)
    norm = lambda h: min_radius + (h - min_h) / (max_h - min_h) * (max_radius - min_radius) if max_h > min_h else min_radius
    return [norm(h) for h in heights]


def draw_animated_starburst(screen, radii, angle_offset, color_phase):
    n = len(radii)
    for i, r in enumerate(radii):
        angle = angle_offset + (2 * math.pi * i / n)
        x_end = CENTER[0] + r * math.cos(angle)
        y_end = CENTER[1] + r * math.sin(angle)
        # Animate color: cycle hue based on time and index
        hue = (color_phase + i / n) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.4, 1.0)
        color = tuple(int(255 * c) for c in rgb)
        pygame.draw.line(screen, color, CENTER, (x_end, y_end), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tidal Spiral Visualization")
    clock = pygame.time.Clock()

    print("Fetching tidal data...")
    data = fetch_tidal_data(TIDE_URL)
    if not data:
        print("No tidal data found. Exiting.")
        sys.exit(1)
    radii = normalize_heights(data)

    angle_offset = 0
    color_phase = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        draw_animated_starburst(screen, radii, angle_offset, color_phase)
        pygame.display.flip()
        angle_offset += 0.01  # rotate
        color_phase = (color_phase + 0.003) % 1.0  # cycle color
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()