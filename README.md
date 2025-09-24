

# Generative Art: Tidal, Climate Flower & Typhoon Star Field Visualization

This project visualizes:
- **Tidal data** from the Hong Kong Observatory as a dynamic, colorful spiral/starburst.
- **Climate data** (Vietnam, 1991-2020, from `chart.csv`) as a vibrant, animated flower of motion dots, with each petal representing a month.
- **Historical Typhoon Warnings in Hong Kong (1998-2025)** as a glowing, animated diamond star field. Each warning is a star that twinkles and shines when its year is active, with a dreamy animated background of twinkling stars.

## Features
- Fetches and parses tidal data from https://www.hko.gov.hk/tide/eCLKtext2027.html
- Reads climate data from a local `chart.csv` file (average temperature and precipitation by month)
- Fetches and parses typhoon warning data from https://envf.ust.hk/dataview/warnings/current/select_data_typh.py?signal__string=1_or_higher&start_time__YMD=19970701&end_time__YMD=20250924&submit=+Query+
- Visualizes:
  - Tidal heights as a moving, color-cycling spiral
  - Climate data as a flower of animated, pulsing dots
  - Typhoon warnings as a star field of glowing, twinkling diamonds
- Interactive: Switch between visualizations using on-screen buttons or keyboard (`T` for Tidal, `C` for Climate)
- Modern, beautiful, and responsive Pygame UI

## Setup
1. Place your `chart.csv` file in the same folder as `main.py` (for climate flower).
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```sh
   python main.py
   ```
   Or run the typhoon star field visualization:
   ```sh
   python typhoon_art.py
   ```

## Requirements
- Python 3.8+
- pygame
- requests
- beautifulsoup4

## Notes
- This project is for creative coding and generative art purposes.
- You can add your own datasets and visualizations by extending `main.py` or creating new scripts.
