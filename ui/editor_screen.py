from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock

class MenuScreen(Screen):
    def start_tutorial(self):
        app = self.manager.app
        app.load_tutorial_script(0)
        self.manager.current = 'editor'
    
    def start_freeplay(self):
        app = self.manager.app
        app.current_script = "# Free Play - Write your own farming script!\n\n# Example: Auto-farm wheat\nfor y in range(5, 12):\n    for x in range(2, 18):\n        drone.move_to(x, y)\n        tile = farm.get_tile(x, y)\n        \n        if tile == 'dirt':\n            drone.plant('wheat')\n        elif tile == 'wheat' and farm.is_ready(x, y):\n            drone.harvest()\n            drone.plant('wheat')"
        self.manager.current = 'editor'
    
    def open_scripts(self):
        # Show saved scripts popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text='Saved Scripts', font_size=dp(20), size_hint_y=None, height=dp(40)))
        
        scroll = ScrollView()
        scripts_list = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        scripts_list.bind(minimum_height=scripts_list.setter('height'))
        
        # Example saved scripts
        scripts = [
            ("Auto Wheat Farm", "Auto-plant and harvest wheat"),
            ("Mixed Crops", "Plant wheat, corn, carrots"),
            ("Spiral Harvest", "Harvest in spiral pattern"),
        ]
        
        for name, desc in scripts:
            btn = Button(text=f"{name}\n{desc}", size_hint_y=None, height=dp(60), halign='left', valign='middle')
            btn.bind(on_press=lambda btn, n=name: self.load_script(n))
            scripts_list.add_widget(btn)
        
        scroll.add_widget(scripts_list)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint_y=None, height=dp(50))
        content.add_widget(close_btn)
        
        popup = Popup(title='My Scripts', content=content, size_hint=(0.9, 0.8))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def load_script(self, name):
        scripts = {
            "Auto Wheat Farm": "# Auto wheat farming\nfor y in range(5, 12):\n    for x in range(2, 18):\n        drone.move_to(x, y)\n        if farm.get_tile(x, y) == 'dirt':\n            drone.plant('wheat')\n        elif farm.get_tile(x, y) == 'wheat' and farm.is_ready(x, y):\n            drone.harvest()\n            drone.plant('wheat')",
            "Mixed Crops": "# Plant mixed crops\ncrops = ['wheat', 'corn', 'carrot']\nfor i, crop in enumerate(crops):\n    for y in range(5+i, 12, 3):\n        for x in range(2+i, 18, 3):\n            drone.move_to(x, y)\n            if farm.get_tile(x, y) == 'dirt':\n                drone.plant(crop)",
            "Spiral Harvest": "# Spiral harvest pattern\ncx, cy = 10, 7\nfor r in range(1, 8):\n    for dx, dy in [(r,0), (0,r), (-r,0), (0,-r)]:\n        drone.move_to(cx+dx, cy+dy)\n        if farm.is_ready(drone.x, drone.y):\n            drone.harvest()"
        }
        self.manager.app.current_script = scripts.get(name, "")
        self.manager.current = 'editor'
    
    def open_learn(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text='Python Basics for Drone Farming', font_size=dp(20), size_hint_y=None, height=dp(40)))
        
        scroll = ScrollView()
        learn_text = '''
DRONE COMMANDS:
• drone.move(dx, dy) - Move relative (dx, dy can be -1, 0, 1)
• drone.move_to(x, y) - Move to absolute position
• drone.plant(crop) - Plant crop on current tile
• drone.harvest() - Harvest crop on current tile
• drone.water() - Water current tile
• drone.wait() - Skip one turn

FARM INFO:
• farm.get_tile(x, y) - Get tile type at position
• farm.is_ready(x, y) - Check if crop is ready to harvest
• farm.width, farm.height - Farm dimensions

DRONE PROPERTIES:
• drone.x, drone.y - Current position
• drone.energy - Remaining energy (0-100)
• drone.inventory - Dict of harvested crops

CONTROL FLOW:
• for x in range(5): - Loop 5 times
• while condition: - Loop while true
• if condition: - Conditional
• else: - Else branch

EXAMPLE - Auto Farm:
for y in range(5, 12):
    for x in range(2, 18):
        drone.move_to(x, y)
        tile = farm.get_tile(x, y)
        if tile == 'dirt':
            drone.plant('wheat')
        elif tile == 'wheat' and farm.is_ready(x, y):
            drone.harvest()
            drone.plant('wheat')

TIPS:
• Drone starts at (10, 7) with 100 energy
• Each move costs 1 energy
• Wheat grows in 5 turns
• Harvest gives 3 wheat
'''
        learn_label = Label(text=learn_text, font_size=dp(14), halign='left', valign='top', text_size=(None, None))
        learn_label.bind(size=lambda s, w: s.setter('text_size')(s, (w[0]-20, None)))
        scroll.add_widget(learn_label)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint_y=None, height=dp(50))
        content.add_widget(close_btn)
        
        popup = Popup(title='Learn Python', content=content, size_hint=(0.95, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical')
        
        # Top bar
        top_bar = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        top_bar.add_widget(Button(text='← Back', size_hint_x=None, width=dp(80), on_press=self.go_back))
        top_bar.add_widget(Label(text='Drone Script Editor', font_size=dp(18), bold=True))
        top_bar.add_widget(Button(text='Run ▶', size_hint_x=None, width=dp(80), background_color=(0.2, 0.7, 0.2, 1), on_press=self.run_script))
        layout.add_widget(top_bar)
        
        # Tabs for editor + reference
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Editor tab
        editor_tab = TabbedPanelItem(text='Editor')
        editor_layout = BoxLayout(orientation='vertical')
        
        # Toolbar
        toolbar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        toolbar.add_widget(Button(text='Tutorial 1', size_hint_x=None, width=dp(100), on_press=lambda b: self.load_tutorial(0)))
        toolbar.add_widget(Button(text='Tutorial 2', size_hint_x=None, width=dp(100), on_press=lambda b: self.load_tutorial(1)))
        toolbar.add_widget(Button(text='Tutorial 3', size_hint_x=None, width=dp(100), on_press=lambda b: self.load_tutorial(1)))
        toolbar.add_widget(Button(text='Clear', size_hint_x=None, width=dp(80), on_press=self.clear_code))
        editor_layout.add_widget(toolbar)
        
        # Code editor
        self.code_input = TextInput(
            text='# Write your drone script here\n',
            font_size=dp(14),
            font_name='RobotoMono-Regular',
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.9, 0.95, 0.9, 1),
            cursor_color=(1, 1, 1, 1),
            selection_color=(0.3, 0.6, 0.9, 0.5),
            multiline=True,
            padding=dp(10)
        )
        editor_layout.add_widget(self.code_input)
        editor_tab.content = editor_layout
        tab_panel.add_widget(editor_tab)
        
        # Reference tab
        ref_tab = TabbedPanelItem(text='Reference')
        ref_scroll = ScrollView()
        ref_label = Label(text='''
DRONE API REFERENCE

MOVEMENT:
drone.move(dx, dy)        # Relative move (-1, 0, 1)
drone.move_to(x, y)       # Absolute position
drone.wait()              # Skip turn

FARMING:
drone.plant('crop')       # 'wheat', 'corn', 'carrot'
drone.harvest()           # Harvest current tile
drone.water()             # Water current tile
drone.fertilize()         # Fertilize current tile

INFO:
drone.x, drone.y          # Position
drone.energy              # 0-100
drone.inventory           # {'wheat': 5, ...}

FARM:
farm.get_tile(x, y)       # 'dirt', 'wheat', 'corn', etc.
farm.is_ready(x, y)       # True if ready to harvest
farm.width, farm.height   # Map size

CROPS: 'wheat' (5 turns), 'corn' (8 turns), 'carrot' (4 turns)

CONTROL FLOW:
for i in range(n): ...
while condition: ...
if condition: ... else: ...
        ''', font_size=dp(12), halign='left', valign='top', size_hint_y=None)
        self.bind(size=lambda *x: None)
        ref_label.bind(texture_size=lambda *x: ref_label.setter('height')(ref_label, ref_label.texture_size[1]))
        ref_scroll.add_widget(ref_label)
        ref_tab.content = ref_scroll
        tab_panel.add_widget(ref_tab)
        
        # Examples tab
        ex_tab = TabbedPanelItem(text='Examples')
        ex_scroll = ScrollView()
        ex_label = Label(text='''
EXAMPLE 1: Simple movement
drone.move(1, 0)   # Right
drone.move(0, 1)   # Down
drone.move(-1, 0)  # Left

EXAMPLE 2: Plant and harvest
drone.move_to(5, 5)
if farm.get_tile(5, 5) == 'dirt':
    drone.plant('wheat')
# ... wait 5 turns ...
drone.harvest()

EXAMPLE 3: Auto-farm loop
for y in range(5, 12):
    for x in range(2, 18):
        drone.move_to(x, y)
        tile = farm.get_tile(x, y)
        if tile == 'dirt':
            drone.plant('wheat')
        elif tile == 'wheat' and farm.is_ready(x, y):
            drone.harvest()
            drone.plant('wheat')

EXAMPLE 4: Spiral harvest
cx, cy = 10, 7
for r in range(1, 8):
    for dx, dy in [(r,0), (0,r), (-r,0), (0,-r)]:
        drone.move_to(cx+dx, cy+dy)
        if farm.is_ready(drone.x, drone.y):
            drone.harvest()
''', font_size=dp(12), halign='left', valign='top', size_hint_y=None)
        ex_label.bind(texture_size=lambda *x: ex_label.setter('height')(ex_label, ex_label.texture_size[1]))
        ex_scroll.add_widget(ex_label)
        ex_tab.content = ex_scroll
        tab_panel.add_widget(ex_tab)
        
        layout.add_widget(tab_panel)
        self.add_widget(layout)
    
    def go_back(self, *args):
        self.manager.current = 'menu'
    
    def load_tutorial(self, num):
        app = self.manager.app
        app.load_tutorial_script(num)
        self.code_input.text = app.current_script
    
    def clear_code(self, *args):
        self.code_input.text = '# Write your drone script here\n'
    
    def run_script(self, *args):
        self.manager.app.current_script = self.code_input.text
        self.manager.app.start_simulation()


class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drone = None
        self.farm = None
        self.simulation_running = False
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical')
        
        # Top bar
        top_bar = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        top_bar.add_widget(Button(text='← Editor', size_hint_x=None, width=dp(100), on_press=self.go_back))
        top_bar.add_widget(Label(text='Simulation', font_size=dp(20), bold=True))
        self.status_label = Label(text='Ready', font_size=dp(16))
        top_bar.add_widget(self.status_label)
        layout.add_widget(top_bar)
        
        # Stats bar
        stats_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        self.energy_label = Label(text='Energy: 100', font_size=dp(14))
        self.pos_label = Label(text='Pos: (10, 7)', font_size=dp(14))
        self.inv_label = Label(text='Inv: {}', font_size=dp(14))
        stats_bar.add_widget(self.energy_label)
        stats_bar.add_widget(self.pos_label)
        stats_bar.add_widget(self.inv_label)
        layout.add_widget(stats_bar)
        
        # Farm view
        self.farm_view = FarmView()
        layout.add_widget(self.farm_view)
        
        # Controls
        controls = BoxLayout(size_hint_y=None, height=dp(120), spacing=dp(5), padding=dp(10))
        
        # Directional pad
        dpad = BoxLayout(orientation='vertical', spacing=dp(5))
        row1 = BoxLayout()
        row1.add_widget(Label(size_hint_x=None, width=dp(60)))
        row1.add_widget(Button(text='↑', font_size=dp(20), on_press=lambda b: self.manual_move(0, -1)))
        dpad.add_widget(row1)
        
        row2 = BoxLayout()
        row2.add_widget(Button(text='←', font_size=dp(20), on_press=lambda b: self.manual_move(-1, 0)))
        row2.add_widget(Button(text='Wait', font_size=dp(16), on_press=lambda b: self.manual_wait()))
        row2.add_widget(Button(text='→', font_size=dp(20), on_press=lambda b: self.manual_move(1, 0)))
        dpad.add_widget(row2)
        
        row3 = BoxLayout()
        row3.add_widget(Label(size_hint_x=None, width=dp(60)))
        row3.add_widget(Button(text='↓', font_size=dp(20), on_press=lambda b: self.manual_move(0, 1)))
        dpad.add_widget(row3)
        
        controls.add_widget(dpad)
        
        # Action buttons
        actions = BoxLayout(orientation='vertical', spacing=dp(5))
        actions.add_widget(Button(text='Plant Wheat', on_press=lambda b: self.manual_action('plant', 'wheat')))
        actions.add_widget(Button(text='Harvest', on_press=lambda b: self.manual_action('harvest')))
        actions.add_widget(Button(text='Water', on_press=lambda b: self.manual_action('water')))
        actions.add_widget(Button(text='Fertilize', on_press=lambda b: self.manual_action('fertilize')))
        controls.add_widget(actions)
        
        layout.add_widget(controls)
        self.add_widget(layout)
    
    def start_simulation(self, drone, farm, message):
        self.drone = drone
        self.farm = farm
        self.farm_view.set_farm(farm)
        self.farm_view.set_drone(drone)
        self.simulation_running = True
        self.status_label.text = message
        self.update_stats()
        # Animate farm
        Clock.schedule_interval(self.update_simulation, 1/10)
    
    def update_simulation(self, dt):
        if self.simulation_running and self.drone:
            self.update_stats()
            self.farm_view.update()
    
    def update_stats(self):
        if self.drone:
            self.energy_label.text = f'Energy: {self.drone.energy}'
            self.pos_label.text = f'Pos: ({self.drone.x}, {self.drone.y})'
            inv_str = ', '.join(f'{k}:{v}' for k,v in self.drone.inventory.items()) if self.drone.inventory else '{}'
            self.inv_label.text = f'Inv: {{{inv_str}}}'
    
    def manual_move(self, dx, dy):
        if self.drone and self.drone.energy > 0:
            self.drone.move(dx, dy)
            self.update_stats()
    
    def manual_wait(self):
        if self.drone:
            self.drone.wait()
            self.update_stats()
    
    def manual_action(self, action, crop=None):
        if not self.drone:
            return
        if action == 'plant' and crop:
            self.drone.plant(crop)
        elif action == 'harvest':
            self.drone.harvest()
        elif action == 'water':
            self.drone.water()
        elif action == 'fertilize':
            self.drone.fertilize()
        self.update_stats()
    
    def go_back(self, *args):
        self.simulation_running = False
        Clock.unschedule(self.update_simulation)
        self.manager.current = 'editor'


class FarmView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.farm = None
        self.drone = None
        self.tile_widgets = {}
        self.orientation = 'vertical'
        self.spacing = 1
        self.padding = dp(5)
    
    def set_farm(self, farm):
        self.farm = farm
        self.redraw()
    
    def set_drone(self, drone):
        self.drone = drone
    
    def redraw(self):
        self.clear_widgets()
        self.tile_widgets = {}
        
        if not self.farm:
            return
        
        # Color mapping
        colors = {
            'dirt': (0.55, 0.35, 0.15, 1),
            'water': (0.2, 0.4, 0.8, 1),
            'wheat': (0.8, 0.7, 0.2, 1),
            'corn': (0.9, 0.8, 0.1, 1),
            'carrot': (0.9, 0.4, 0.1, 1),
            'grass': (0.2, 0.6, 0.2, 1),
        }
        
        # Growth stage opacity
        growth_colors = {
            0: 0.3,  # Just planted
            1: 0.5,
            2: 0.7,
            3: 0.9,
            4: 1.0,  # Ready
        }
        
        for y in range(self.farm.height):
            row = BoxLayout(spacing=1)
            for x in range(self.farm.width):
                tile = self.farm.get_tile(x, y)
                growth = self.farm.get_growth(x, y)
                
                base_color = colors.get(tile, (0.5, 0.5, 0.5, 1))
                alpha = growth_colors.get(growth, 1.0) if tile != 'dirt' and tile != 'water' else 1.0
                
                btn = Button(
                    background_color=(*base_color[:3], alpha),
                    size_hint=(None, None),
                    width=dp(24),
                    height=dp(24),
                    on_press=lambda btn, x=x, y=y: self.on_tile_click(x, y)
                )
                
                # Mark drone position
                if self.drone and self.drone.x == x and self.drone.y == y:
                    btn.background_color = (0.1, 0.8, 0.1, 1)
                    btn.text = '🚁'
                    btn.font_size = 10
                
                # Show growth stage for crops
                if tile in ['wheat', 'corn', 'carrot'] and growth > 0:
                    btn.text = str(growth)
                    btn.font_size = 8
                
                self.tile_widgets[(x, y)] = btn
                row.add_widget(btn)
            self.add_widget(row)
    
    def on_tile_click(self, x, y):
        print(f"Tile ({x}, {y}): {self.farm.get_tile(x, y)}")
    
    def update(self):
        if self.farm and self.drone:
            self.redraw()