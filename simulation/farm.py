"""
Farm simulation - manages the farm grid, tiles, and crop growth
"""

import random

class Farm:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.tiles = {}  # (x, y) -> {'type': 'dirt', 'growth': 0, 'watered': False, 'fertilized': False}
        self.turn = 0
        self.initialize_farm()
    
    def initialize_farm(self):
        """Create initial farm layout"""
        for y in range(self.height):
            for x in range(self.width):
                # Mostly dirt, some water, some grass
                r = random.random()
                if r < 0.05:
                    tile_type = 'water'
                elif r < 0.1:
                    tile_type = 'grass'
                else:
                    tile_type = 'dirt'
                
                self.tiles[(x, y)] = {
                    'type': tile_type,
                    'growth': 0,
                    'watered': False,
                    'fertilized': False,
                    'crop_type': None
                }
    
    def reset(self):
        """Reset farm to initial state"""
        self.turn = 0
        self.initialize_farm()
    
    def get_tile(self, x, y):
        """Get tile type at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[(x, y)]['type']
        return 'void'
    
    def get_growth(self, x, y):
        """Get growth stage (0-4)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[(x, y)]['growth']
        return 0
    
    def get_crop_type(self, x, y):
        """Get crop type at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[(x, y)]['crop_type']
        return None
    
    def set_tile(self, x, y, tile_type, growth=0, crop_type=None):
        """Set tile type and properties"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[(x, y)] = {
                'type': tile_type,
                'growth': growth,
                'watered': False,
                'fertilized': False,
                'crop_type': crop_type if tile_type in ['wheat', 'corn', 'carrot'] else None
            }
    
    def is_ready(self, x, y):
        """Check if crop is ready to harvest"""
        tile = self.get_tile(x, y)
        growth = self.get_growth(x, y)
        
        if tile in ['wheat', 'corn', 'carrot']:
            required = CROP_GROWTH_TIME.get(tile, 5)
            return growth >= 4  # Ready at stage 4 (0-indexed, so 5th stage)
        return False
    
    def water(self, x, y):
        """Water a tile"""
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.tiles[(x, y)]['type']
            if tile in ['wheat', 'corn', 'carrot']:
                self.tiles[(x, y)]['watered'] = True
                return True
        return False
    
    def fertilize(self, x, y):
        """Fertilize a tile"""
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.tiles[(x, y)]['type']
            if tile in ['wheat', 'corn', 'carrot']:
                self.tiles[(x, y)]['fertilized'] = True
                return True
        return False
    
    def update(self):
        """Advance one turn - grow crops"""
        self.turn += 1
        
        for y in range(self.height):
            for x in range(self.width):
                tile_data = self.tiles[(x, y)]
                tile_type = tile_data['type']
                
                if tile_type in ['wheat', 'corn', 'carrot']:
                    # Grow crop
                    growth = tile_data['growth']
                    max_growth = 4  # 0-4 (5 stages)
                    
                    if growth < 4:
                        # Growth speed modifiers
                        speed = 1.0
                        if tile_data['watered']:
                            speed += 0.5
                        if tile_data['fertilized']:
                            speed += 0.3
                        
                        # Random growth chance based on speed
                        if random.random() < 0.3 * speed:
                            tile_data['growth'] = min(4, growth + 1)
                        
                        # Reset watered/fertilized after effect
                        tile_data['watered'] = False
                        tile_data['fertilized'] = False
    
    def get_status(self):
        """Get farm statistics"""
        counts = {}
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[(x, y)]['type']
                counts[tile] = counts.get(tile, 0) + 1
        return counts
    
    def get_tile_info(self, x, y):
        """Get detailed tile info"""
        if 0 <= x < self.width and 0 <= y < self.height:
            data = self.tiles[(x, y)]
            return {
                'type': data['type'],
                'growth': data['growth'],
                'watered': data['watered'],
                'fertilized': data['fertilized'],
                'crop_type': data['crop_type']
            }
        return None


# Crop configuration
CROP_GROWTH_TIME = {
    'wheat': 5,   # turns to grow
    'corn': 8,
    'carrot': 4,
}

CROP_YIELDS = {
    'wheat': 3,
    'corn': 2,
    'carrot': 4,
}

CROP_COLORS = {
    'wheat': (0.8, 0.7, 0.2),
    'corn': (0.9, 0.8, 0.1),
    'carrot': (0.9, 0.4, 0.1),
}