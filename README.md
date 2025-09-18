
# Generative Art: Tidal & Climate Flower Visualization

This project visualizes:
- **Tidal data** from the Hong Kong Observatory as a dynamic, colorful spiral/starburst.
- **Climate data** (Vietnam, 1991-2020, from `chart.csv`) as a vibrant, animated flower of motion dots, with each petal representing a month.

## Features
- Fetches and parses tidal data from https://www.hko.gov.hk/tide/eCLKtext2027.html
- Reads climate data from a local `chart.csv` file (average temperature and precipitation by month)
- Visualizes:
  - Tidal heights as a moving, color-cycling spiral
  - Climate data as a flower of animated, pulsing dots
- Interactive: Switch between visualizations using on-screen buttons or keyboard (`T` for Tidal, `C` for Climate)
- Modern, beautiful, and responsive Pygame UI

## Setup
1. Place your `chart.csv` file in the same folder as `main.py`.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```sh
   python main.py
   ```

## Requirements
- Python 3.8+
- Pygame
- requests
- beautifulsoup4

## Notes
- This project is for creative coding and generative art purposes.
- You can add your own datasets and visualizations by extending `main.py`.
