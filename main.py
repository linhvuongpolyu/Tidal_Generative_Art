import pygame
import requests
from bs4 import BeautifulSoup
import math
import colorsys
import sys
import csv
import os

WIDTH, HEIGHT = 800, 1000  # Tall window to ensure buttons are visible
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (10, 10, 30)
FPS = 60

TIDE_URL = "https://www.hko.gov.hk/tide/eCLKtext2027.html"

def fetch_tidal_data(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    data = []
    table = soup.find('table')
    if not table:
        return data
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            time = cols[0].get_text(strip=True)
            try:
                height = float(cols[1].get_text(strip=True))
                data.append((time, height))
            except ValueError:
                continue
    return data

def normalize_heights(data, min_radius=80, max_radius=250):
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
        hue = (color_phase + i / n) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.4, 1.0)
        color = tuple(int(255 * c) for c in rgb)
        pygame.draw.line(screen, color, CENTER, (x_end, y_end), 3)

def read_climate_csv(path):
    months = []
    mean_temps = []
    precipitation = []
    print(f"DEBUG: Reading climate CSV from {path}")
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            print(f"DEBUG: CSV row: {row}")
            months.append(row['Category'].strip('"'))
            mean_temp = float(row['Average Mean Surface Air Temperature (°C)'].replace(',', '.'))
            precip = float(row['Precipitation (mm)'].replace(',', '.'))
            mean_temps.append(mean_temp)
            precipitation.append(precip)
    print(f"DEBUG: Parsed months: {months}")
    print(f"DEBUG: Parsed mean_temps: {mean_temps}")
    print(f"DEBUG: Parsed precipitation: {precipitation}")
    return months, mean_temps, precipitation

def normalize_list(data, min_out, max_out):
    min_d, max_d = min(data), max(data)
    if max_d == min_d:
        return [min_out for _ in data]
    return [min_out + (d - min_d) / (max_d - min_d) * (max_out - min_out) for d in data]

def draw_climate_flower(screen, temps, precips, angle_offset, color_phase):
    n = len(temps)
    radii = normalize_list(temps, 120, 240)
    thicknesses = normalize_list(precips, 8, 24)
    for i in range(n):
        # Animate each dot with a pulsing effect
        angle = angle_offset + (2 * math.pi * i / n)
        pulse = 1 + 0.18 * math.sin(color_phase * 2 * math.pi + i * 2 * math.pi / n * 2)
        r = radii[i] * pulse
        x = CENTER[0] + r * math.cos(angle)
        y = CENTER[1] + r * math.sin(angle)
        # Animate color for each dot
        hue = (color_phase + i / n) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 1.0)
        color = tuple(int(255 * c) for c in rgb)
        # Draw a moving dot at the petal tip
        pygame.draw.circle(screen, color, (int(x), int(y)), int(thicknesses[i] * (0.7 + 0.3 * pulse)))

def draw_button(screen, rect, text, active):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 28)
    color = (80, 180, 255) if active else (60, 60, 90)
    border = (180, 220, 255) if active else (120, 120, 160)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, border, rect, 3)
    surf = font.render(text, True, (30, 30, 50) if active else (200, 200, 220))
    text_rect = surf.get_rect(center=rect.center)
    screen.blit(surf, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tidal & Climate Generative Art")
    clock = pygame.time.Clock()

    # Fetch tidal data
    print("Fetching tidal data...")
    data = fetch_tidal_data(TIDE_URL)
    print(f"DEBUG: Tidal data count: {len(data)}")
    if not data:
        print("No tidal data found. Exiting.")
        sys.exit(1)
    radii = normalize_heights(data)
    print(f"DEBUG: Normalized tidal radii: {radii[:10]}...")

    # Read climate data
    climate_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chart.csv"))
    print(f"DEBUG: Looking for climate CSV at {climate_path}")
    if not os.path.exists(climate_path):
        print("Climate data file not found:", climate_path)
        sys.exit(1)
    months, mean_temps, precipitation = read_climate_csv(climate_path)

    mode = "tidal"  # or "climate"
    angle_offset = 0
    color_phase = 0

    # Button setup (drawn higher so they're always visible)
    btn_w, btn_h = 220, 60
    btn_tidal = pygame.Rect(WIDTH // 2 - btn_w - 40, HEIGHT - btn_h - 120, btn_w, btn_h)
    btn_climate = pygame.Rect(WIDTH // 2 + 40, HEIGHT - btn_h - 120, btn_w, btn_h)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    print("DEBUG: Switched to tidal mode (keyboard)")
                    mode = "tidal"
                elif event.key == pygame.K_c:
                    print("DEBUG: Switched to climate mode (keyboard)")
                    mode = "climate"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        screen.fill(BG_COLOR)
        # Draw art with smaller radius to leave space for buttons
        if mode == "tidal":
            draw_animated_starburst(screen, radii, angle_offset, color_phase)
        elif mode == "climate":
            draw_climate_flower(screen, mean_temps, precipitation, angle_offset, color_phase)


        # Draw a semi-transparent overlay at the bottom for button area
        overlay = pygame.Surface((WIDTH, 180), pygame.SRCALPHA)
        overlay.fill((20, 20, 40, 180))  # RGBA: last value is alpha for transparency
        screen.blit(overlay, (0, HEIGHT-180))

        # Draw buttons (higher up)
        draw_button(screen, btn_tidal, "Tidal Art", mode == "tidal")
        draw_button(screen, btn_climate, "Climate Flower", mode == "climate")

        # Button click logic
        if mouse_click:
            if btn_tidal.collidepoint(mouse_pos):
                print("DEBUG: Switched to tidal mode (button)")
                mode = "tidal"
            elif btn_climate.collidepoint(mouse_pos):
                print("DEBUG: Switched to climate mode (button)")
                mode = "climate"

        # Show current mode label and data title
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 28)
        label = font.render(f"Current mode: {mode.capitalize()}", True, (200, 220, 255))
        screen.blit(label, (20, 20))
        # Data title for each visualization
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        if mode == "tidal":
            title_text = "Tidal Data: Hong Kong Observatory (https://www.hko.gov.hk/tide/eCLKtext2027.html)"
        elif mode == "climate":
            title_text = "Climate Data: Vietnam 1991-2020 (chart.csv)"
        else:
            title_text = ""
        title_surf = title_font.render(title_text, True, (255, 230, 120))
        # Add more space between the title and the upper edge
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 90))

        pygame.display.flip()
        angle_offset += 0.01
        color_phase = (color_phase + 0.004) % 1.0
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()