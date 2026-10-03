"""
Drone simulation - controls the farming drone
"""

class Drone:
    def __init__(self, farm, x=10, y=7):
        self.farm = farm
        self.x = x
        self.y = y
        self.energy = 100
        self.max_energy = 100
        self.inventory = {}  # {'wheat': 5, 'corn': 2}
        self._last_action = None
    
    def reset(self):
        """Reset drone to starting state"""
        self.x = 10
        self.y = 7
        self.energy = 100
        self.inventory = {}
        self._last_action = None
    
    def _check_bounds(self, x, y):
        """Ensure position is within farm bounds"""
        x = max(0, min(x, self.farm.width - 1))
        y = max(0, min(y, self.farm.height - 1))
        return x, y
    
    def _consume_energy(self, amount=1):
        """Consume energy, return False if not enough"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def _add_to_inventory(self, item, count=1):
        """Add item to inventory"""
        self.inventory[item] = self.inventory.get(item, 0) + count
    
    # ===== MOVEMENT =====
    def move(self, dx, dy):
        """Move relative (-1, 0, 1)"""
        if not self._consume_energy(1):
            return False, "Not enough energy!"
        
        new_x = self.x + dx
        new_y = self.y + dy
        new_x, new_y = self._check_bounds(new_x, new_y)
        
        if new_x != self.x or new_y != self.y:
            self.x = new_x
            self.y = new_y
            return True, f"Moved to ({self.x}, {self.y})"
        return False, "Can't move there"
    
    def move_to(self, x, y):
        """Move to absolute position (pathfinding not implemented, direct)"""
        x, y = self._check_bounds(x, y)
        distance = abs(x - self.x) + abs(y - self.y)
        
        if not self._consume_energy(distance):
            return False, "Not enough energy!"
        
        self.x = x
        self.y = y
        return True, f"Moved to ({self.x}, {self.y})"
    
    def wait(self):
        """Skip turn, recover small energy"""
        self.energy = min(self.max_energy, self.energy + 2)
        return True, f"Waited. Energy: {self.energy}"
    
    # ===== FARMING =====
    def plant(self, crop='wheat'):
        """Plant crop on current tile"""
        if not self._consume_energy(2):
            return False, "Not enough energy to plant!"
        
        valid_crops = ['wheat', 'corn', 'carrot']
        if crop not in valid_crops:
            return False, f"Unknown crop: {crop}"
        
        tile = self.farm.get_tile(self.x, self.y)
        if tile != 'dirt':
            return False, f"Can't plant on {tile}!"
        
        self.farm.set_tile(self.x, self.y, crop, growth=0)
        self._last_action = f"Planted {crop}"
        return True, f"Planted {crop} at ({self.x}, {self.y})"
    
    def harvest(self):
        """Harvest crop on current tile"""
        if not self._consume_energy(2):
            return False, "Not enough energy to harvest!"
        
        tile = self.farm.get_tile(self.x, self.y)
        if not self.farm.is_ready(self.x, self.y):
            return False, f"{tile} not ready to harvest!"
        
        # Crop yields
        yields = {
            'wheat': 3,
            'corn': 2,
            'carrot': 4,
        }
        
        yield_count = yields.get(tile, 1)
        self._add_to_inventory(tile, yield_count)
        self.farm.set_tile(self.x, self.y, 'dirt')
        self._last_action = f"Harvested {yield_count} {tile}"
        return True, f"Harvested {yield_count} {tile}!"
    
    def water(self):
        """Water current tile"""
        if not self._consume_energy(1):
            return False, "Not enough energy to water!"
        
        tile = self.farm.get_tile(self.x, self.y)
        if tile in ['wheat', 'corn', 'carrot']:
            self.farm.water(self.x, self.y)
            self._last_action = "Watered crop"
            return True, "Watered crop"
        return False, "Nothing to water here"
    
    def fertilize(self):
        """Fertilize current tile"""
        if not self._consume_energy(3):
            return False, "Not enough energy to fertilize!"
        
        tile = self.farm.get_tile(self.x, self.y)
        if tile in ['wheat', 'corn', 'carrot']:
            self.farm.fertilize(self.x, self.y)
            self._last_action = "Fertilized crop"
            return True, "Fertilized crop (growth speed increased)"
        return False, "Nothing to fertilize here"
    
    def get_status(self):
        return {
            'position': (self.x, self.y),
            'energy': self.energy,
            'inventory': self.inventory.copy(),
            'last_action': self._last_action
        }


# Crop growth times (in turns)
CROP_GROWTH_TIME = {
    'wheat': 5,
    'corn': 8,
    'carrot': 4,
}

CROP_YIELDS = {
    'wheat': 3,
    'corn': 2,
    'carrot': 4,
}