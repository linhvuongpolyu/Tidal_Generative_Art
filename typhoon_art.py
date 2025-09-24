import pygame
import requests
import io
from bs4 import BeautifulSoup
import math
import colorsys

WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (0, 0, 0)
FPS = 60

# Dataset URL for historical typhoon warnings
DATA_URL = "https://envf.ust.hk/dataview/warnings/current/select_data_typh.py?signal__string=1_or_higher&start_time__YMD=19970701&end_time__YMD=20250924&submit=+Query+"

# Fetch and parse typhoon warning data

def fetch_typhoon_data(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    warnings = []
    if not table:
        print("No table found in HTML.")
        return warnings
    rows = table.find_all('tr')
    header = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
    print("HTML Table Header:", header)
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        intensity = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        signal = cols[2].get_text(strip=True)
        issuing = cols[3].get_text(strip=True)
        cancelling = cols[4].get_text(strip=True)
        duration = cols[5].get_text(strip=True)
        year = issuing[:4] if len(issuing) >= 4 else ''
        warnings.append({
            'intensity': intensity,
            'name': name,
            'signal': signal,
            'issuing': issuing,
            'cancelling': cancelling,
            'duration': duration,
            'year': year
        })
    print(f"Parsed {len(warnings)} warnings from HTML table.")
    return warnings

# Generative art: Colorful motion spiral for typhoon warnings

def draw_typhoon_spiral(screen, warnings, angle_offset, color_phase):
    n = len(warnings)
    # Add background stars
    NUM_BG_STARS = 180
    if not hasattr(draw_typhoon_spiral, 'bg_stars'):
        import random
        draw_typhoon_spiral.bg_stars = []
        for i in range(NUM_BG_STARS):
            x = random.randint(30, WIDTH-30)
            y = random.randint(30, HEIGHT-30)
            size = random.randint(2, 4)
            phase = random.uniform(0, 2*math.pi)
            draw_typhoon_spiral.bg_stars.append({'x': x, 'y': y, 'size': size, 'phase': phase})
    # Group warnings by year
    year_dict = {}
    for w in warnings:
        year = w['year']
        if year:
            year_dict.setdefault(year, []).append(w)
    years = sorted(year_dict.keys())
    if not years:
        pygame.font.init()
        err_font = pygame.font.SysFont("Arial", 32, bold=True)
        err_text = "No valid typhoon warning data found."
        err_surf = err_font.render(err_text, True, (255, 80, 80))
        screen.blit(err_surf, (WIDTH//2 - err_surf.get_width()//2, HEIGHT//2 - 40))
        return
    if not hasattr(draw_typhoon_spiral, 'frame'):
        draw_typhoon_spiral.frame = 0
    draw_typhoon_spiral.frame += 1
    year_idx = (draw_typhoon_spiral.frame // 60) % len(years)
    current_year = years[year_idx]
    # Precompute fixed random positions for all warnings
    import random
    if not hasattr(draw_typhoon_spiral, 'fixed_positions'):
        draw_typhoon_spiral.fixed_positions = {}
        for w in warnings:
            key = w['issuing']+w['name']
            x = random.randint(40, WIDTH-40)
            y = random.randint(40, HEIGHT-40)
            draw_typhoon_spiral.fixed_positions[key] = (x, y)
    frame = draw_typhoon_spiral.frame if hasattr(draw_typhoon_spiral, 'frame') else 0
    # Draw background stars
    for i, star in enumerate(draw_typhoon_spiral.bg_stars):
        twinkle_phase = (frame * 0.04 + star['phase']) % (2 * math.pi)
        twinkle = 0.7 + 0.3 * math.sin(twinkle_phase)
        move_radius = 6
        move_angle = (frame * 0.01 + i * 0.5) % (2 * math.pi)
        x = int(star['x'] + move_radius * math.cos(move_angle))
        y = int(star['y'] + move_radius * math.sin(move_angle))
        base_radius = int(star['size'] * twinkle)
        glow_radius = base_radius + int(8 * twinkle)
        color = (220, 220, 255)
        def draw_diamond(surf, color, center, size):
            cx, cy = center
            points = [
                (cx, cy - size),
                (cx + size, cy),
                (cx, cy + size),
                (cx - size, cy)
            ]
            pygame.draw.polygon(surf, color, points)
        # Glow
        for r in range(glow_radius, base_radius, -2):
            alpha = int(40 * twinkle * (1 - (r-base_radius)/(glow_radius-base_radius)))
            glow = (*color, alpha)
            glow_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            draw_diamond(glow_surf, glow, (r, r), r)
            screen.blit(glow_surf, (x-r, y-r))
        draw_diamond(screen, color, (x, y), base_radius)
    # Draw warning stars
    for i, w in enumerate(warnings):
        signal = w['signal']
        year = w['year']
        try:
            sig_num = int(signal.replace('No.', '').replace(' ', '')) if signal else 1
        except Exception:
            sig_num = 1
        twinkle_phase = (frame * 0.04 + i * 0.7) % (2 * math.pi)
        twinkle = 0.7 + 0.3 * math.sin(twinkle_phase)
        key = w['issuing']+w['name']
        base_x, base_y = draw_typhoon_spiral.fixed_positions.get(key, (random.randint(40, WIDTH-40), random.randint(40, HEIGHT-40)))
        move_radius = 8 + sig_num * 2
        move_angle = (frame * 0.01 + i * 0.5) % (2 * math.pi)
        x = int(base_x + move_radius * math.cos(move_angle))
        y = int(base_y + move_radius * math.sin(move_angle))
        base_radius = int((2 + max(1, 10 - sig_num * 2)) * twinkle)
        glow_radius = base_radius + int(10 * twinkle)
        hue = (color_phase + sig_num * 0.1 + i / n) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.8, twinkle)
        color = tuple(int(255 * c) for c in rgb)
        def draw_diamond(surf, color, center, size):
            cx, cy = center
            points = [
                (cx, cy - size),
                (cx + size, cy),
                (cx, cy + size),
                (cx - size, cy)
            ]
            pygame.draw.polygon(surf, color, points)
        if year == current_year:
            # Glow: soft glow around diamond, shine bright
            for r in range(glow_radius, base_radius, -2):
                alpha = int(80 * twinkle * (1 - (r-base_radius)/(glow_radius-base_radius)))
                glow = (*color, alpha)
                glow_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                draw_diamond(glow_surf, glow, (r, r), r)
                screen.blit(glow_surf, (x-r, y-r))
            draw_diamond(screen, color, (x, y), base_radius)
            draw_diamond(screen, (255,255,255), (x, y), max(1, base_radius//2))
        else:
            # Dim warning stars when not active year
            faded = tuple(int(c * 0.18) for c in color)
            for r in range(glow_radius, base_radius, -2):
                alpha = int(30 * twinkle * (1 - (r-base_radius)/(glow_radius-base_radius)))
                glow = (*faded, alpha)
                glow_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                draw_diamond(glow_surf, glow, (r, r), r)
                screen.blit(glow_surf, (x-r, y-r))
            draw_diamond(screen, faded, (x, y), base_radius)
    # Show current year label
    pygame.font.init()
    year_font = pygame.font.SysFont("Arial", 28, bold=True)
    year_surf = year_font.render(f"Year: {current_year}", True, (200, 220, 255))
    screen.blit(year_surf, (WIDTH//2 - year_surf.get_width()//2, 80))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Historical Typhoon Warnings Generative Art")
    clock = pygame.time.Clock()

    print("Fetching typhoon warning data...")
    warnings = fetch_typhoon_data(DATA_URL)
    print(f"Loaded {len(warnings)} typhoon warnings.")

    angle_offset = 0
    color_phase = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        draw_typhoon_spiral(screen, warnings, angle_offset, color_phase)

        # Title
        pygame.font.init()
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        title_text = "Historical Typhoon Warnings in Hong Kong (1998-2025)"
        title_surf = title_font.render(title_text, True, (255, 230, 120))
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 40))

        pygame.display.flip()
        angle_offset += 0.008
        color_phase = (color_phase + 0.003) % 1.0
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
