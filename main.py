#!/usr/bin/env python3
"""
The Farmer Was Replaced - Mobile Edition
A Python-programmable drone farming game for mobile.
Learn Python by writing scripts to control your farming drone!
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# Import our modules
from ui.editor_screen import EditorScreen
from ui.simulation_screen import SimulationScreen
from ui.menu_screen import MenuScreen
from simulation.drone import Drone
from simulation.farm import Farm

# Kivy UI layout
KV = '''
ScreenManager:
    MenuScreen:
    EditorScreen:
    SimulationScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        
        Label:
            text: 'The Farmer Was Replaced'
            font_size: dp(32)
            bold: True
            size_hint_y: None
            height: dp(60)
            color: 0.2, 0.6, 0.2, 1
        
        Label:
            text: 'Program your drone to farm!'
            font_size: dp(18)
            size_hint_y: None
            height: dp(40)
            color: 0.4, 0.4, 0.4, 1
        
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: None
            height: dp(200)
            
            Button:
                text: 'Start Farming (Tutorial)'
                font_size: dp(20)
                background_color: 0.2, 0.7, 0.2, 1
                on_press: root.start_tutorial()
            
            Button:
                text: 'Free Play'
                font_size: dp(20)
                background_color: 0.3, 0.5, 0.8, 1
                on_press: root.start_freeplay()
            
            Button:
                text: 'My Scripts'
                font_size: dp(20)
                background_color: 0.8, 0.6, 0.2, 1
                on_press: root.open_scripts()
            
            Button:
                text: 'Learn Python'
                font_size: dp(20)
                background_color: 0.6, 0.3, 0.8, 1
                on_press: root.open_learn()

<EditorScreen>:
    name: 'editor'
    
<SimulationScreen>:
    name: 'simulation'
'''

class FarmerDroneApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drone = None
        self.farm = None
        self.current_script = ""
        self.tutorial_step = 0
    
    def build(self):
        self.title = 'Farmer Drone - Mobile'
        Window.clearcolor = (0.95, 0.98, 0.95, 1)
        
        # Initialize game objects
        self.farm = Farm(width=20, height=15)
        self.drone = Drone(self.farm, x=10, y=7)
        
        # Load KV
        root = Builder.load_string(KV)
        return root
    
    def on_start(self):
        # Load tutorial script
        self.load_tutorial_script(0)
    
    def load_tutorial_script(self, step):
        self.tutorial_step = step
        scripts = {
            0: '''# Tutorial 1: Move the drone
# The drone starts at position (10, 7)
# Use drone.move(dx, dy) to move

# Move right 3 times
drone.move(1, 0)
drone.move(1, 0)
drone.move(1, 0)

# Now move down 2 times
drone.move(0, 1)
drone.move(0, 1)

# Check what's under the drone
print("Position:", drone.x, drone.y)
print("Tile:", farm.get_tile(drone.x, drone.y))''',
            1: '''# Tutorial 2: Plant seeds
# Move to dirt tile first
while farm.get_tile(drone.x, drone.y) != 'dirt':
    drone.move(1, 0)
    if drone.x >= farm.width - 1:
        drone.x = 0
        drone.move(0, 1)

# Plant seeds on dirt
if farm.get_tile(drone.x, drone.y) == 'dirt':
    drone.plant('wheat')
    print("Planted wheat!")

# Water it
drone.water()''',
            2: '''# Tutorial 3: Harvest loop
# Simple farming automation
crops_planted = 0

for y in range(5, 10):
    for x in range(2, 18):
        drone.move_to(x, y)
        tile = farm.get_tile(x, y)
        
        if tile == 'dirt':
            drone.plant('wheat')
            crops_planted += 1
        elif tile == 'wheat' and farm.is_ready(x, y):
            drone.harvest()
            drone.plant('wheat')  # Replant

print(f"Managed {crops_planted} crops!")'''
        }
        self.current_script = scripts.get(step, scripts[0])
        # Update editor if on that screen
        editor = self.root.get_screen('editor')
        if hasattr(editor, 'code_input'):
            editor.code_input.text = self.current_script
    
    def run_script(self, script_text):
        """Execute user's Python script safely"""
        self.current_script = script_text
        
        # Reset drone and farm for simulation
        self.drone.reset()
        self.farm.reset()
        
        # Create safe execution environment
        safe_globals = {
            'drone': self.drone,
            'farm': self.farm,
            'print': print,
            'range': range,
            'len': len,
            'int': int,
            'str': str,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
        }
        
        try:
            exec(script_text, {"__builtins__": {}}, safe_globals)
            return True, "Script completed successfully!"
        except Exception as e:
            return False, f"Error: {type(e).__name__}: {e}"

    def start_simulation(self):
        """Switch to simulation screen and run"""
        success, msg = self.run_script(self.current_script)
        sim_screen = self.root.get_screen('simulation')
        sim_screen.start_simulation(self.drone, self.farm, msg)
        self.root.current = 'simulation'


if __name__ == '__main__':
    FarmerDroneApp().run()