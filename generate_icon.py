#!/usr/bin/env python3
"""Generate app icon PNG from vector description"""
from PIL import Image, ImageDraw

# Create 108x108 image
img = Image.new('RGBA', (108, 108), (46, 125, 50, 255))  # Green background
draw = ImageDraw.Draw(img)

# Drone body (white triangle)
draw.polygon([(54, 30), (44, 42), (64, 42)], fill=(255, 255, 255, 255))

# Drone rotors (light gray)
draw.polygon([(38, 38), (42, 34), (48, 38), (44, 42)], fill=(224, 224, 224, 255))
draw.polygon([(70, 38), (66, 34), (60, 38), (64, 42)], fill=(224, 224, 224, 255))
draw.polygon([(38, 62), (42, 66), (48, 62), (44, 58)], fill=(224, 224, 224, 255))
draw.polygon([(70, 62), (66, 66), (60, 62), (64, 58)], fill=(224, 224, 224, 255))

# Wheat stalks (golden)
draw.polygon([(20, 80), (22, 65), (24, 80)], fill=(245, 230, 82, 255))
draw.polygon([(30, 80), (32, 62), (34, 80)], fill=(245, 230, 82, 255))
draw.polygon([(40, 80), (42, 68), (44, 80)], fill=(245, 230, 82, 255))

# Sun (yellow)
draw.polygon([(90, 18), (90, 8), (90, 28)], fill=(255, 213, 79, 255))
draw.polygon([(100, 18), (90, 18), (80, 18)], fill=(255, 213, 79, 255))
draw.polygon([(90, 18), (86, 14), (90, 22)], fill=(255, 213, 79, 255))

# Save
img.save('/root/farmer_drone_mobile/assets/icon.png')
print("Icon saved to assets/icon.png")