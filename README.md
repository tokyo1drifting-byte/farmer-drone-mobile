# The Farmer Was Replaced - Mobile Edition

A Python-programmable drone farming game for Android. Learn Python by writing scripts to control your farming drone!

## Game Concept

You control a flying drone that automates farming tasks. Write Python scripts to:
- Move the drone around the farm
- Plant crops (wheat, corn, carrots)
- Water and fertilize crops
- Harvest when ready
- Automate everything with loops and conditionals

## Features

- **Code Editor** - Write Python scripts with syntax highlighting
- **Visual Simulation** - Watch your drone farm in real-time
- **Tutorials** - 3 guided tutorials teaching Python basics
- **Reference** - Built-in API documentation
- **Free Play** - Create your own farming automation
- **Manual Controls** - Take direct control when needed

## Learning Python

This game teaches:
- Variables and data types
- Loops (`for`, `while`)
- Conditionals (`if/else`)
- Functions and methods
- Lists and dictionaries
- Object-oriented concepts

## Building for Android

### Requirements
- Linux/macOS (or WSL2 on Windows)
- Python 3.8+
- Buildozer: `pip install buildozer`
- Android SDK/NDK (auto-installed by buildozer)

### Build
```bash
# First time setup (downloads SDK/NDK - takes 10-30 mins)
buildozer android debug

# Subsequent builds (faster)
buildozer android debug
```

The APK will be in `bin/` directory.

### Deploy to device
```bash
# With USB debugging enabled
buildozer android debug deploy run
```

## Project Structure

```
farmer_drone_mobile/
├── main.py                 # App entry point
├── buildozer.spec          # Android build config
├── simulation/
│   ├── __init__.py
│   ├── drone.py           # Drone logic & API
│   └── farm.py            # Farm simulation & crops
├── ui/
│   ├── __init__.py
│   ├── menu_screen.py     # Main menu
│   ├── editor_screen.py   # Code editor + reference
│   └── simulation_screen.py # Visual farm + controls
└── assets/
    └── icon.png           # App icon
```

## Drone API Quick Reference

```python
# Movement
drone.move(dx, dy)        # Relative move (-1, 0, 1)
drone.move_to(x, y)       # Absolute position
drone.wait()              # Skip turn, recover energy

# Farming
drone.plant('wheat')      # 'wheat', 'corn', 'carrot'
drone.harvest()           # Harvest current tile
drone.water()             # Water current tile
drone.fertilize()         # Speed up growth

# Info
drone.x, drone.y          # Position
drone.energy              # 0-100
drone.inventory           # {'wheat': 5, ...}

# Farm info
farm.get_tile(x, y)       # 'dirt', 'wheat', etc.
farm.is_ready(x, y)       # True if ready to harvest
farm.width, farm.height   # Map size
```

## Example Scripts

### Auto-farm wheat
```python
for y in range(5, 12):
    for x in range(2, 18):
        drone.move_to(x, y)
        tile = farm.get_tile(x, y)
        if tile == 'dirt':
            drone.plant('wheat')
        elif tile == 'wheat' and farm.is_ready(x, y):
            drone.harvest()
            drone.plant('wheat')
```

### Spiral harvest pattern
```python
cx, cy = 10, 7
for r in range(1, 8):
    for dx, dy in [(r,0), (0,r), (-r,0), (0,-r)]:
        drone.move_to(cx+dx, cy+dy)
        if farm.is_ready(drone.x, drone.y):
            drone.harvest()
```

## Controls

- **Editor**: Write code, press ▶ Run
- **Simulation**: Watch drone, use D-pad for manual control
- **Manual buttons**: Plant, Harvest, Water, Fertilize
- **Back**: Return to editor/menu

## Educational Design

- **Tutorial 1**: Basic movement and inspection
- **Tutorial 2**: Planting and watering
- **Tutorial 3**: Automated farming loops
- **Reference tab**: Complete API docs in editor
- **Examples tab**: Copy-paste starter scripts

## License

Educational project - learn Python through game development!