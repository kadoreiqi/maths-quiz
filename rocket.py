import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import math
import time

class RocketLaunchGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Rocket Launch Mission Control! 🌟")
        self.root.geometry("1000x800")
        self.root.configure(bg='#001122')  # Space background
        
        # Game state
        self.score = 0
        self.total_questions = 0
        self.current_value = 0
        self.current_target_value = 0
        self.current_unit_from = ""
        self.current_unit_to = ""
        self.rocket_y = 0
        self.animation_running = False
        self.log_file = "rocket_launch_log.txt"
        
        # Canvas for animation
        self.canvas_width = 400
        self.canvas_height = 500
        
        # Colors
        self.colors = {
            'space': '#001122',
            'ground': '#8B4513',
            'rocket': '#FF4500',
            'fire': '#FF6B00',
            'success': '#32CD32',
            'error': '#FF6B6B',
            'text': '#FFFFFF',
            'button': '#4169E1',
            'launchpad': '#708090'
        }
        
        # Animation variables
        self.rocket_pos = [self.canvas_width//2, self.canvas_height - 80]
        self.fire_particles = []
        self.firework_particles = []
        self.stars = []
        
        self.setup_ui()
        self.create_background()
        self.new_mission()
        self.animate()  # Start animation loop
        
    def setup_ui(self):
        """Create the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['space'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 ROCKET LAUNCH MISSION CONTROL 🌟",
            font=('Arial', 20, 'bold'),
            fg='#FFD700',
            bg=self.colors['space']
        )
        title_label.pack(pady=(0, 20))
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=self.colors['space'])
        content_frame.pack(fill='both', expand=True)
        
        # Left side - Animation
        left_frame = tk.Frame(content_frame, bg=self.colors['space'])
        left_frame.pack(side='left', padx=(0, 20))
        
        tk.Label(
            left_frame,
            text="🎯 LAUNCH TRAJECTORY",
            font=('Arial', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['space']
        ).pack(pady=(0, 10))
        
        self.canvas = tk.Canvas(
            left_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#000033',
            highlightthickness=2,
            highlightbackground='#FFD700'
        )
        self.canvas.pack()
        
        # Right side - Mission Control
        right_frame = tk.Frame(content_frame, bg=self.colors['space'], width=400)
        right_frame.pack(side='right', fill='both', expand=True)
        right_frame.pack_propagate(False)
        
        # Mission info
        mission_frame = tk.Frame(right_frame, bg='#002244', relief='raised', bd=3)
        mission_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            mission_frame,
            text="📡 MISSION BRIEFING",
            font=('Arial', 16, 'bold'),
            fg='#00FFFF',
            bg='#002244'
        ).pack(pady=10)
        
        self.mission_label = tk.Label(
            mission_frame,
            text="Loading mission...",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg='#002244',
            wraplength=350,
            justify='center'
        )
        self.mission_label.pack(pady=(0, 20))
        
        # Question display
        self.question_label = tk.Label(
            mission_frame,
            text="",
            font=('Arial', 14, 'bold'),
            fg='#FFFF00',
            bg='#002244',
            wraplength=350
        )
        self.question_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = tk.Frame(right_frame, bg='#003366', relief='raised', bd=3)
        input_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            input_frame,
            text="🎮 LAUNCH COMPUTER",
            font=('Arial', 14, 'bold'),
            fg='#00FF00',
            bg='#003366'
        ).pack(pady=10)
        
        self.input_label = tk.Label(
            input_frame,
            text="Enter value:",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg='#003366'
        )
        self.input_label.pack()
        
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(
            input_frame,
            textvariable=self.answer_var,
            font=('Arial', 16, 'bold'),
            width=15,
            justify='center',
            bg='#FFFFFF',
            fg='#000000',
            bd=3,
            relief='ridge'
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda event: self.launch_rocket())
        
        # Launch button
        self.launch_button = tk.Button(
            input_frame,
            text="🚀 LAUNCH ROCKET!",
            font=('Arial', 14, 'bold'),
            bg='#FF4500',
            fg='white',
            padx=20,
            pady=10,
            command=self.launch_rocket,
            relief='raised',
            bd=3
        )
        self.launch_button.pack(pady=(10, 20))
        
        # Status display
        status_frame = tk.Frame(right_frame, bg='#001100', relief='raised', bd=3)
        status_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            status_frame,
            text="📊 MISSION STATUS",
            font=('Arial', 14, 'bold'),
            fg='#00FF00',
            bg='#001100'
        ).pack(pady=10)
        
        self.score_label = tk.Label(
            status_frame,
            text="🏆 Successful Launches: 0/0",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text'],
            bg='#001100'
        )
        self.score_label.pack(pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="⚡ READY FOR LAUNCH",
            font=('Arial', 12, 'bold'),
            fg='#FFFF00',
            bg='#001100'
        )
        self.status_label.pack(pady=(0, 20))
        
        # Control buttons
        control_frame = tk.Frame(right_frame, bg=self.colors['space'])
        control_frame.pack(fill='x')
        
        self.next_button = tk.Button(
            control_frame,
            text="🎯 Next Mission",
            font=('Arial', 12, 'bold'),
            bg=self.colors['button'],
            fg='white',
            padx=15,
            pady=8,
            command=self.new_mission,
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.next_button.pack(side='left', padx=(0, 10))
        
        help_button = tk.Button(
            control_frame,
            text="❓ Help",
            font=('Arial', 12),
            bg='#4B0082',
            fg='white',
            padx=15,
            pady=8,
            command=self.show_help,
            relief='raised',
            bd=2
        )
        help_button.pack(side='left', padx=(0, 10))
        
        exit_button = tk.Button(
            control_frame,
            text="🚪 Exit",
            font=('Arial', 12),
            bg='#8B0000',
            fg='white',
            padx=15,
            pady=8,
            command=self.exit_game,
            relief='raised',
            bd=2
        )
        exit_button.pack(side='right')
        
        self.answer_entry.focus()
    
    def create_background(self):
        """Create the space background with stars, ground, and launch pad"""
        self.canvas.delete("all")
        
        # Create stars
        self.stars = []
        for _ in range(30):
            x = random.randint(10, self.canvas_width-10)
            y = random.randint(10, self.canvas_height-200)
            size = random.randint(1, 2)
            star_id = self.canvas.create_oval(x-size, y-size, x+size, y+size, fill='white', outline='white')
            self.stars.append([star_id, x, y, random.uniform(0.5, 2.0)])
        
        # Ground
        self.canvas.create_rectangle(0, self.canvas_height-60, self.canvas_width, self.canvas_height, 
                                   fill=self.colors['ground'], outline=self.colors['ground'])
        
        # Launch pad
        pad_center = self.canvas_width // 2
        self.canvas.create_rectangle(pad_center-30, self.canvas_height-80, pad_center+30, self.canvas_height-60,
                                   fill=self.colors['launchpad'], outline='white', width=2)
        
        # Altitude markers (every 1 km)
        for i in range(1, 5):  # 1km to 4km markers
            y_pos = self.canvas_height - 100 - (i * 80)  # Each km = 80 pixels
            if y_pos > 10:
                self.canvas.create_line(10, y_pos, 30, y_pos, fill='#00FF00', width=2)
                self.canvas.create_text(35, y_pos, text=f"{i}km", fill='#00FF00', font=('Arial', 9, 'bold'))
        
        # Reset rocket position
        self.rocket_pos = [self.canvas_width//2, self.canvas_height - 80]
        self.draw_rocket()
    
    def draw_rocket(self):
        """Draw the rocket at current position"""
        self.canvas.delete("rocket")
        x, y = self.rocket_pos
        
        # Rocket body
        self.canvas.create_rectangle(x-8, y-30, x+8, y, fill=self.colors['rocket'], outline='white', tags="rocket")
        # Rocket nose
        self.canvas.create_polygon(x, y-40, x-8, y-30, x+8, y-30, fill='silver', outline='white', tags="rocket")
        # Fins
        self.canvas.create_polygon(x-8, y-10, x-15, y, x-8, y, fill='red', outline='white', tags="rocket")
        self.canvas.create_polygon(x+8, y-10, x+15, y, x+8, y, fill='red', outline='white', tags="rocket")
    
    def draw_rocket_fire(self):
        """Draw rocket exhaust flames"""
        if not self.animation_running:
            return
            
        self.canvas.delete("fire")
        x, y = self.rocket_pos
        
        # Main flame
        flame_height = random.randint(15, 25)
        self.canvas.create_polygon(
            x-6, y, x, y+flame_height, x+6, y,
            fill=self.colors['fire'], outline='yellow', tags="fire"
        )
        
        # Side flames
        for i in range(3):
            fx = x + random.randint(-10, 10)
            fy = y + random.randint(5, 15)
            size = random.randint(2, 4)
            self.canvas.create_oval(fx-size, fy-size, fx+size, fy+size, 
                                  fill='yellow', outline='orange', tags="fire")
    
    def draw_fireworks(self):
        """Draw celebration fireworks"""
        if not self.firework_particles:
            return
            
        self.canvas.delete("fireworks")
        
        for particle in self.firework_particles[:]:
            x, y, vx, vy, life, color = particle
            
            # Update position
            x += vx
            y += vy
            vy += 0.3  # gravity
            life -= 1
            
            if life > 0:
                size = max(1, life // 3)
                self.canvas.create_oval(x-size, y-size, x+size, y+size, 
                                      fill=color, outline=color, tags="fireworks")
                particle[0], particle[1], particle[3], particle[5] = x, y, vy, life
            else:
                self.firework_particles.remove(particle)
    
    def create_firework(self, x, y):
        """Create a firework explosion"""
        colors = ['red', 'yellow', 'green', 'blue', 'purple', 'orange', 'pink']
        for _ in range(12):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(20, 40)
            color = random.choice(colors)
            self.firework_particles.append([x, y, vx, vy, life, color])
    
    def format_number(self, num):
        """Format number to appropriate precision (up to 5 significant figures)"""
        if num == int(num):
            return str(int(num))
        else:
            # Format with up to 5 significant figures
            formatted = f"{num:.5g}"
            return formatted
    
    def generate_mission(self):
        """Generate a new mission with meters/km conversion (0-4km range)"""
        # Randomly choose conversion direction
        conversion_type = random.choice(['m_to_km', 'km_to_m'])
        
        if conversion_type == 'm_to_km':
            # Generate meters that convert to 0-4km range
            # Create various types of values for interesting conversions
            value_types = [
                # Whole kilometers
                lambda: random.randint(0, 4) * 1000,
                # Half kilometers  
                lambda: random.choice([500, 1500, 2500, 3500]),
                # Quarter kilometers
                lambda: random.choice([250, 750, 1250, 1750, 2250, 2750, 3250, 3750]),
                # Decimal kilometers with varying precision
                lambda: int(random.uniform(0, 4000)),
                # More precise values
                lambda: int(random.uniform(0, 4000) * 10) / 10,
            ]
            
            meters = random.choice(value_types)()
            target_km = meters / 1000
            
            unit_from = "meters"
            unit_to = "km"
            
        else:  # km_to_m
            # Generate km values in 0-4 range
            km_types = [
                # Whole numbers
                lambda: float(random.randint(0, 4)),
                # Half values
                lambda: random.choice([0.5, 1.5, 2.5, 3.5]),
                # Quarter values
                lambda: random.choice([0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75]),
                # Random decimal values
                lambda: round(random.uniform(0, 4), random.randint(1, 3)),
                # Very precise values
                lambda: round(random.uniform(0, 4), 4),
            ]
            
            km_value = random.choice(km_types)()
            target_meters = km_value * 1000
            
            meters = km_value
            target_km = target_meters
            
            unit_from = "km"
            unit_to = "meters"
        
        # Generate mission stories
        if conversion_type == 'm_to_km':
            mission_stories = [
                f"🛰️ Deploy satellite at {self.format_number(meters)} meters altitude",
                f"🌌 Reach space station at {self.format_number(meters)} meters height", 
                f"🚀 Launch payload to {self.format_number(meters)} meters orbit",
                f"⭐ Conduct experiments at {self.format_number(meters)} meters above Earth",
                f"🌍 Monitor weather from {self.format_number(meters)} meters altitude"
            ]
            story = random.choice(mission_stories)
            question = f"Mission altitude: {self.format_number(meters)} {unit_from}\nConvert to {unit_to} for launch computer:"
            visual_km = target_km  # For animation
            
        else:  # km_to_m
            mission_stories = [
                f"🛰️ Deploy satellite at {self.format_number(meters)} km altitude",
                f"🌌 Reach space station at {self.format_number(meters)} km height",
                f"🚀 Launch payload to {self.format_number(meters)} km orbit", 
                f"⭐ Conduct experiments at {self.format_number(meters)} km above Earth",
                f"🌍 Monitor weather from {self.format_number(meters)} km altitude"
            ]
            story = random.choice(mission_stories)
            question = f"Mission altitude: {self.format_number(meters)} {unit_from}\nConvert to {unit_to} for launch computer:"
            visual_km = meters  # For animation (km value)
        
        return story, question, meters, target_km, unit_from, unit_to, visual_km
    
    def new_mission(self):
        """Start a new mission"""
        if self.animation_running:
            return
            
        story, question, value, target_value, unit_from, unit_to, visual_km = self.generate_mission()
        
        self.current_value = value
        self.current_target_value = target_value
        self.current_unit_from = unit_from
        self.current_unit_to = unit_to
        self.visual_km = visual_km  # For animation purposes
        self.user_answer = 0
        
        self.mission_label.config(text=story)
        self.question_label.config(text=question)
        self.input_label.config(text=f"Enter value in {unit_to}:")
        self.answer_var.set("")
        self.status_label.config(text="⚡ READY FOR LAUNCH", fg='#FFFF00')
        
        # Reset animation
        self.create_background()
        self.launch_button.config(state='normal')
        self.next_button.config(state='disabled')
        self.answer_entry.config(state='normal')
        self.answer_entry.focus()
    
    def is_answer_correct(self, user_answer, target_answer):
        """Check if answer is correct within reasonable tolerance"""
        if abs(target_answer) < 1e-10:  # Handle zero case
            return abs(user_answer) < 1e-10
        
        # Use relative tolerance for better precision handling
        relative_tolerance = 1e-9
        absolute_tolerance = 1e-12
        
        return abs(user_answer - target_answer) <= max(relative_tolerance * abs(target_answer), absolute_tolerance)
    
    def launch_rocket(self):
        """Launch the rocket with user's answer"""
        if self.animation_running:
            return
            
        user_input = self.answer_var.get().strip()
        
        if not user_input:
            messagebox.showwarning("Mission Control", "🚨 Enter target value before launch!")
            return
        
        try:
            self.user_answer = float(user_input)
        except ValueError:
            messagebox.showerror("Input Error", "⚠️ Please enter a valid number!")
            return
        
        # Check answer
        is_correct = self.is_answer_correct(self.user_answer, self.current_target_value)
        
        self.total_questions += 1
        
        # Disable controls during animation
        self.launch_button.config(state='disabled')
        self.answer_entry.config(state='disabled')
        
        if is_correct:
            self.score += 1
            self.status_label.config(text="🎯 PERFECT TRAJECTORY!", fg=self.colors['success'])
            self.animate_successful_launch()
        else:
            self.status_label.config(text="❌ TRAJECTORY ERROR!", fg=self.colors['error'])
            self.animate_launch_with_user_path()
        
        self.update_score_display()
        conversion_text = f"{self.format_number(self.current_value)} {self.current_unit_from} to {self.current_unit_to}"
        self.log_attempt(conversion_text, user_input, self.current_target_value, is_correct)
    
    def animate_successful_launch(self):
        """Animate successful rocket launch to target"""
        self.animation_running = True
        target_height = self.canvas_height - 100 - (self.visual_km * 80)  # 80 pixels per km
        target_height = max(10, target_height)  # Keep within canvas
        
        def launch_step():
            if self.rocket_pos[1] > target_height:
                self.rocket_pos[1] -= 3  # Move up
                self.draw_rocket()
                self.draw_rocket_fire()
                self.root.after(50, launch_step)
            else:
                # Reached target - celebrate!
                self.canvas.delete("fire")
                self.status_label.config(text="🚀 MISSION SUCCESS!", fg=self.colors['success'])
                
                # Create fireworks
                for _ in range(3):
                    fx = random.randint(50, self.canvas_width-50)
                    fy = random.randint(50, 150)
                    self.create_firework(fx, fy)
                
                self.animation_running = False
                self.next_button.config(state='normal')
                self.next_button.focus()
        
        launch_step()
    
    def animate_launch_with_user_path(self):
        """Animate rocket launch to user's entered value, then show correct path"""
        self.animation_running = True
        original_y = self.rocket_pos[1]
        
        # Calculate heights based on conversion type
        if self.current_unit_to == "km":
            # User answered in km, show km scale
            user_target_height = self.canvas_height - 100 - (self.user_answer * 80)
            correct_target_height = self.canvas_height - 100 - (self.current_target_value * 80)
            user_display = f"{self.format_number(self.user_answer)}km"
            correct_display = f"{self.format_number(self.current_target_value)}km"
        else:
            # User answered in meters, convert to km for display
            user_km = self.user_answer / 1000
            correct_km = self.current_target_value / 1000
            user_target_height = self.canvas_height - 100 - (user_km * 80)
            correct_target_height = self.canvas_height - 100 - (correct_km * 80)
            user_display = f"{self.format_number(self.user_answer)}m"
            correct_display = f"{self.format_number(self.current_target_value)}m"
        
        # Clamp heights to canvas bounds
        user_target_height = max(10, min(user_target_height, self.canvas_height - 100))
        correct_target_height = max(10, min(correct_target_height, self.canvas_height - 100))
        
        # Phase 1: Launch to user's altitude
        def launch_to_user_altitude():
            if abs(self.rocket_pos[1] - user_target_height) > 3:
                if self.rocket_pos[1] > user_target_height:
                    self.rocket_pos[1] -= 3
                else:
                    self.rocket_pos[1] += 3
                self.draw_rocket()
                self.draw_rocket_fire()
                self.root.after(50, launch_to_user_altitude)
            else:
                # Reached user's altitude
                self.canvas.delete("fire")
                
                # Show user's altitude marker
                x, y = self.rocket_pos
                self.canvas.create_line(10, y, self.canvas_width-10, y, 
                                      fill='#FF6B6B', width=3, tags="user_path")
                self.canvas.create_text(self.canvas_width-70, y-10, 
                                      text=f"Your: {user_display}", 
                                      fill='#FF6B6B', font=('Arial', 9, 'bold'), tags="user_path")
                
                # Update status
                self.status_label.config(
                    text=f"🚀 Reached your target", 
                    fg='#FFB347'
                )
                
                # Wait a moment, then show correct path
                self.root.after(1500, show_correct_path)
        
        def show_correct_path():
            # Show correct altitude marker
            self.canvas.create_line(10, correct_target_height, self.canvas_width-10, correct_target_height,
                                  fill='#32CD32', width=3, tags="correct_path")
            self.canvas.create_text(self.canvas_width-70, correct_target_height-10,
                                  text=f"Target: {correct_display}",
                                  fill='#32CD32', font=('Arial', 9, 'bold'), tags="correct_path")
            
            # Draw arrow pointing to correct altitude
            if correct_target_height < self.rocket_pos[1]:  # Target is higher
                arrow_y = self.rocket_pos[1] - 20
                self.canvas.create_line(self.rocket_pos[0], self.rocket_pos[1]-10, 
                                      self.rocket_pos[0], arrow_y, 
                                      fill='#32CD32', width=3, tags="arrow")
                self.canvas.create_polygon(self.rocket_pos[0], arrow_y-5,
                                         self.rocket_pos[0]-5, arrow_y+5,
                                         self.rocket_pos[0]+5, arrow_y+5,
                                         fill='#32CD32', tags="arrow")
                direction = "↑ HIGHER"
            else:  # Target is lower
                arrow_y = self.rocket_pos[1] + 20
                self.canvas.create_line(self.rocket_pos[0], self.rocket_pos[1]+10, 
                                      self.rocket_pos[0], arrow_y, 
                                      fill='#32CD32', width=3, tags="arrow")
                self.canvas.create_polygon(self.rocket_pos[0], arrow_y+5,
                                         self.rocket_pos[0]-5, arrow_y-5,
                                         self.rocket_pos[0]+5, arrow_y-5,
                                         fill='#32CD32', tags="arrow")
                direction = "↓ LOWER"
            
            # Show conversion hint
            if self.current_unit_from == "meters":
                hint_text = f"💡 {direction}\nHint: {self.format_number(self.current_value)}m ÷ 1000 = {self.format_number(self.current_target_value)}km"
            else:
                hint_text = f"💡 {direction}\nHint: {self.format_number(self.current_value)}km × 1000 = {self.format_number(self.current_target_value)}m"
            
            self.status_label.config(text=hint_text, fg='#FFB347')
            
            # Wait, then return rocket to base
            self.root.after(3000, return_to_base)
        
        def return_to_base():
            if abs(self.rocket_pos[1] - original_y) > 4:
                if self.rocket_pos[1] < original_y:
                    self.rocket_pos[1] += 4
                else:
                    self.rocket_pos[1] -= 4
                self.rocket_pos[0] = self.canvas_width // 2  # Center again
                self.draw_rocket()
                self.root.after(50, return_to_base)
            else:
                # Landed - clean up markers
                self.canvas.delete("user_path")
                self.canvas.delete("correct_path") 
                self.canvas.delete("arrow")
                
                self.animation_running = False
                self.next_button.config(state='normal')
                self.next_button.focus()
        
        # Start the animation sequence
        launch_to_user_altitude()
    
    def animate(self):
        """Main animation loop for background effects"""
        # Twinkling stars
        for star_data in self.stars:
            star_id, x, y, twinkle_speed = star_data
            brightness = int(128 + 127 * math.sin(time.time() * twinkle_speed))
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            self.canvas.itemconfig(star_id, fill=color, outline=color)
        
        # Draw fireworks if any
        self.draw_fireworks()
        
        self.root.after(100, self.animate)
    
    def update_score_display(self):
        """Update score display"""
        percentage = (self.score / self.total_questions * 100) if self.total_questions > 0 else 0
        self.score_label.config(text=f"🏆 Successful Launches: {self.score}/{self.total_questions} ({percentage:.0f}%)")
    
    def log_attempt(self, question, user_answer, correct_answer, is_correct):
        """Log attempt to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "SUCCESS" if is_correct else "FAILED"
        
        log_entry = f"[{timestamp}] Conversion: {question} | Input: {user_answer} | Target: {self.format_number(correct_answer)} | {result}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Could not write to log: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🚀 ROCKET LAUNCH MISSION CONTROL

🎯 OBJECTIVE:
Master unit conversions between meters and kilometers to program the rocket's navigation computer!

🎮 HOW TO PLAY:
1. Read the mission briefing
2. See the altitude in METERS or KILOMETERS
3. Convert to the requested unit
4. Enter your answer and launch!

💡 CONVERSION GUIDE:
• METERS TO KILOMETERS: divide by 1000
  - 1000m = 1km
  - 2500m = 2.5km
  - 3750m = 3.75km

• KILOMETERS TO METERS: multiply by 1000
  - 1km = 1000m
  - 2.5km = 2500m
  - 0.75km = 750m

📏 PRECISION NOTES:
• Supports up to 5 significant figures
• Range: 0 to 4 kilometers
• Both directions: m↔km and km↔m

🚀 LAUNCH RESULTS:
✅ Correct: Rocket reaches target with fireworks!
❌ Wrong: Rocket shows your path vs correct path with hints

Good luck, Commander! 🌟"""
        
        messagebox.showinfo("Mission Control Manual 📋", help_text)
    
    def exit_game(self):
        """Exit with final mission report"""
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            
            if percentage >= 90:
                message = f"🏆 OUTSTANDING COMMANDER!\n\nMission Success Rate: {percentage:.0f}%\nSuccessful Launches: {self.score}/{self.total_questions}\n\nYou're ready for real space missions! 🚀🌟"
            elif percentage >= 70:
                message = f"🌟 EXCELLENT WORK, COMMANDER!\n\nMission Success Rate: {percentage:.0f}%\nSuccessful Launches: {self.score}/{self.total_questions}\n\nGreat piloting skills! 👨‍🚀"
            elif percentage >= 50:
                message = f"👍 GOOD PROGRESS, COMMANDER!\n\nMission Success Rate: {percentage:.0f}%\nSuccessful Launches: {self.score}/{self.total_questions}\n\nKeep training - you're improving! 🚀"
            else:
                message = f"💪 TRAINING COMPLETE!\n\nMission Success Rate: {percentage:.0f}%\nSuccessful Launches: {self.score}/{self.total_questions}\n\nEvery astronaut starts somewhere! Try again! 🌟"
        else:
            message = "Thanks for visiting Mission Control! 🚀\n\nCome back anytime to launch more rockets! 🌟"
        
        messagebox.showinfo("Mission Control - Final Report 📊", message)
        self.root.destroy()
    
    def run(self):
        """Start the game"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=== Rocket Launch Mission Log ===\n\n")
        
        self.root.mainloop()

if __name__ == "__main__":
    game = RocketLaunchGame()
    game.run()