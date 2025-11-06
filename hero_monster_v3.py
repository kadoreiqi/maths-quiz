import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import math
from collections import deque

class BattleConverterGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚔️ Math Battle Arena! 🐉")
        self.root.geometry("900x850")
        self.root.configure(bg='#1a1a2e')
        
        # Game state
        self.score = 0
        self.total_questions = 0
        self.current_question = ""
        self.current_answer = 0.0
        self.current_unit_from = ""
        self.current_unit_to = ""
        self.current_sigfigs = 3
        self.prev_conversion_type = None
        self.recent_q = deque(maxlen=20)
        self.log_file = "battle_log.txt"
        
        self.streak = 0
        self.best_streak = 0
        self.hints_used = 0
        self.hint_available = True
        self.difficulty_level = 1

        # Battle system
        self.level = 1
        self.hero_max_hp = 100
        self.hero_hp = self.hero_max_hp
        self.base_monster_hp = 60
        self.monster_max_hp = self.base_monster_hp
        self.monster_hp = self.monster_max_hp
        self.hero_damage = 15
        self.monster_damage = 12
        
        # Enhanced monster system
        self.monster_types = [
            {"name": "Slime", "emoji": "🟢", "color": "#90EE90"},
            {"name": "Bat", "emoji": "🦇", "color": "#8B4513"},
            {"name": "Goblin", "emoji": "👹", "color": "#DAA520"},
            {"name": "Dragon", "emoji": "🐉", "color": "#FF4500"},
            {"name": "Demon", "emoji": "😈", "color": "#8B0000"},
            {"name": "Golem", "emoji": "🗿", "color": "#808080"},
            {"name": "Hydra", "emoji": "🐍", "color": "#9370DB"}
        ]
        self.current_monster = random.choice(self.monster_types)
        
        # Animation variables
        self.attack_animation_id = None
        self.shake_animation_id = None
        self.particle_ids = []
        self.hero_x = 150
        self.hero_y = 150
        self.monster_x = 650
        self.monster_y = 150
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'secondary_bg': '#16213e',
            'primary': '#e94560',
            'secondary': '#0f3460',
            'success': '#00ff88',
            'error': '#ff3366',
            'text': '#ffffff',
            'gold': '#ffd700',
            'battle_bg': '#2d2d44'
        }
        
        self.setup_ui()
        self.new_question()
        self.animate_idle()
        
    def round_sig(self, x, sig):
        if x == 0:
            return 0.0
        if sig < 1:
            sig = 1
        if sig > 6:
            sig = 6
        return float(f"{x:.{sig}g}")

    def format_number(self, num):
        if abs(num - int(num)) < 1e-12:
            return str(int(num))
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        return formatted
    
    def get_difficulty_ranges(self):
        if self.difficulty_level == 1:
            km_range = (1, 100)
            m_range = (1000, 10000)
        elif self.difficulty_level == 2:
            km_range = (1, 500)
            m_range = (1000, 30000)
        else:
            km_range = (0.5, 999)
            m_range = (500, 50000)
        return km_range, m_range
    
    def generate_question_once(self, force_type=None):
        if force_type is not None:
            conversion_type = force_type
        else:
            choices = ["km_to_m", "m_to_km"]
            if self.prev_conversion_type in choices:
                other = "m_to_km" if self.prev_conversion_type == "km_to_m" else "km_to_m"
                conversion_type = random.choices([other, self.prev_conversion_type], weights=[0.85, 0.15])[0]
            else:
                conversion_type = random.choice(choices)

        sig_figs = random.choices([1, 2, 3, 4], weights=[1, 3, 3, 2])[0]
        km_range, m_range = self.get_difficulty_ranges()

        km_templates = [
            "🚀 Spaceship traveled {val} km",
            "✈️ Jet flew {val} kilometers",
            "🏃 Runner completed {val} km",
            "🚂 Train moved {val} kilometers",
            "🎈 Balloon drifted {val} km"
        ]
        m_templates = [
            "🌟 Rocket ascended {val} meters",
            "🏊 Swimmer covered {val} m",
            "🚴 Cyclist rode {val} meters",
            "⛷️ Skier descended {val} m",
            "🦘 Kangaroo hopped {val} meters"
        ]

        if conversion_type == "km_to_m":
            raw = random.uniform(*km_range)
            if random.random() < 0.3 and sig_figs <= 2:
                raw = round(raw / 10) * 10
            km_value = self.round_sig(raw, sig_figs)
            template = random.choice(km_templates)
            question = template.format(val=self.format_number(km_value))
            correct_answer = km_value * 1000
            unit_from, unit_to = "km", "m"
            value_key = f"{conversion_type}:{self.format_number(km_value)}"
        else:
            raw = random.uniform(*m_range)
            if random.random() < 0.25 and sig_figs <= 3:
                raw = round(raw / 1000) * 1000
            m_value = self.round_sig(raw, sig_figs)
            template = random.choice(m_templates)
            question = template.format(val=self.format_number(m_value))
            correct_answer = m_value / 1000
            unit_from, unit_to = "m", "km"
            value_key = f"{conversion_type}:{self.format_number(m_value)}"

        return question, correct_answer, unit_from, unit_to, sig_figs, conversion_type, value_key

    def generate_question(self):
        for attempt in range(100):
            q = self.generate_question_once()
            question, correct_answer, unit_from, unit_to, sig_figs, conversion_type, value_key = q
            if value_key not in self.recent_q:
                if attempt < 10 and self.prev_conversion_type == conversion_type:
                    continue
                return q
        alternate = "m_to_km" if self.prev_conversion_type == "km_to_m" else "km_to_m"
        return self.generate_question_once(force_type=alternate)

    def new_question(self):
        (self.current_question,
         self.current_answer,
         self.current_unit_from,
         self.current_unit_to,
         self.current_sigfigs,
         conversion_type,
         value_key) = self.generate_question()
        
        self.prev_conversion_type = conversion_type
        self.recent_q.append(value_key)
        
        if self.total_questions > 0 and self.total_questions % 10 == 0:
            accuracy = (self.score / self.total_questions) * 100
            if accuracy >= 85 and self.difficulty_level < 3:
                self.difficulty_level += 1
                self.show_floating_text("⬆️ LEVEL UP!", self.root.winfo_width()//2, 200, '#ffd700')
            elif accuracy < 50 and self.difficulty_level > 1:
                self.difficulty_level -= 1

        self.question_label.config(text=self.current_question)
        target_text = f"Convert to {self.current_unit_to.upper()}"
        self.target_label.config(text=target_text)
        self.answer_var.set("")
        self.result_label.config(text="")
        
        # Clear the top banner when moving to a new question
        self.set_top_banner("")
        
        self.hint_available = True
        self.hint_button.config(state='normal', bg=self.colors['gold'])
        self.check_button.config(state='normal')
        self.next_button.config(state='disabled')
        self.answer_entry.focus()
    
    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=10)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(
            title_frame, 
            text="⚔️ MATH BATTLE ARENA ⚔️",
            font=('Arial Black', 26, 'bold'),
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # >>> TOP BANNER for Correct Answer <<<
        self.top_banner = tk.Label(
            self.root,
            text="",
            font=('Arial', 18, 'bold'),
            fg='#111111',
            bg=self.colors['bg'],
            pady=8
        )
        self.top_banner.pack(fill='x', padx=20)

        # Score Frame
        score_frame = tk.Frame(self.root, bg=self.colors['secondary'], pady=8)
        score_frame.pack(fill='x', padx=20, pady=5)
        
        score_left = tk.Frame(score_frame, bg=self.colors['secondary'])
        score_left.pack(side='left', padx=20)
        
        self.score_label = tk.Label(
            score_left,
            text="⭐ 0/0",
            font=('Arial', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['secondary']
        )
        self.score_label.pack()
        
        score_right = tk.Frame(score_frame, bg=self.colors['secondary'])
        score_right.pack(side='right', padx=20)
        
        self.streak_label = tk.Label(
            score_right,
            text="🔥 0",
            font=('Arial', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['secondary']
        )
        self.streak_label.pack()

        # Battle Canvas
        self.battle_canvas = tk.Canvas(
            self.root,
            width=850,
            height=250,
            bg=self.colors['battle_bg'],
            highlightthickness=2,
            highlightbackground=self.colors['primary']
        )
        self.battle_canvas.pack(padx=20, pady=10)
        
        # Draw battlefield
        self.draw_battlefield()
        
        # Battle Info Frame
        battle_info = tk.Frame(self.root, bg=self.colors['secondary_bg'], pady=5)
        battle_info.pack(fill='x', padx=20, pady=5)
        
        # Hero side
        hero_frame = tk.Frame(battle_info, bg=self.colors['secondary_bg'])
        hero_frame.pack(side='left', expand=True, fill='x', padx=10)
        
        tk.Label(
            hero_frame,
            text="🧙‍♂️ HERO",
            font=('Arial', 12, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['secondary_bg']
        ).pack(anchor='w')
        
        self.hero_hp_label = tk.Label(
            hero_frame,
            text=f"❤️ {self.hero_hp}/{self.hero_max_hp}",
            font=('Arial', 11),
            fg=self.colors['text'],
            bg=self.colors['secondary_bg']
        )
        self.hero_hp_label.pack(anchor='w')
        
        self.hero_hp_bar = ttk.Progressbar(
            hero_frame,
            orient='horizontal',
            length=350,
            mode='determinate',
            maximum=self.hero_max_hp
        )
        self.hero_hp_bar['value'] = self.hero_hp
        self.hero_hp_bar.pack(fill='x', pady=2)
        
        # Level display center
        level_frame = tk.Frame(battle_info, bg=self.colors['secondary_bg'])
        level_frame.pack(side='left', padx=20)
        
        self.level_label = tk.Label(
            level_frame,
            text=f"⚔️\nLV {self.level}",
            font=('Arial', 16, 'bold'),
            fg=self.colors['gold'],
            bg=self.colors['secondary_bg']
        )
        self.level_label.pack()
        
        # Monster side
        monster_frame = tk.Frame(battle_info, bg=self.colors['secondary_bg'])
        monster_frame.pack(side='right', expand=True, fill='x', padx=10)
        
        self.monster_name_label = tk.Label(
            monster_frame,
            text=f"{self.current_monster['emoji']} {self.current_monster['name'].upper()}",
            font=('Arial', 12, 'bold'),
            fg=self.current_monster['color'],
            bg=self.colors['secondary_bg']
        )
        self.monster_name_label.pack(anchor='e')
        
        self.monster_hp_label = tk.Label(
            monster_frame,
            text=f"❤️ {self.monster_hp}/{self.monster_max_hp}",
            font=('Arial', 11),
            fg=self.colors['text'],
            bg=self.colors['secondary_bg']
        )
        self.monster_hp_label.pack(anchor='e')
        
        self.monster_hp_bar = ttk.Progressbar(
            monster_frame,
            orient='horizontal',
            length=350,
            mode='determinate',
            maximum=self.monster_max_hp
        )
        self.monster_hp_bar['value'] = self.monster_hp
        self.monster_hp_bar.pack(fill='x', pady=2)

        # Question Frame
        question_frame = tk.Frame(self.root, bg=self.colors['secondary'], pady=15, padx=20)
        question_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.question_label = tk.Label(
            question_frame,
            text="Loading...",
            font=('Arial', 20, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['secondary'],
            wraplength=700
        )
        self.question_label.pack(pady=10)
        
        self.target_label = tk.Label(
            question_frame,
            text="Convert to M",
            font=('Arial', 14),
            fg=self.colors['gold'],
            bg=self.colors['secondary']
        )
        self.target_label.pack(pady=5)
        
        # Input Frame
        input_frame = tk.Frame(question_frame, bg=self.colors['secondary'])
        input_frame.pack(pady=10)
        
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(
            input_frame,
            textvariable=self.answer_var,
            font=('Arial', 22, 'bold'),
            width=18,
            justify='center',
            bd=3,
            relief='solid',
            bg='#ffffff',
            fg='#000000'
        )
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())
        
        # Buttons Frame
        button_frame = tk.Frame(question_frame, bg=self.colors['secondary'])
        button_frame.pack(pady=10)
        
        self.hint_button = tk.Button(
            button_frame,
            text="💡",
            font=('Arial', 16, 'bold'),
            bg=self.colors['gold'],
            fg='white',
            padx=15,
            pady=5,
            command=self.show_hint,
            relief='raised',
            bd=3,
            cursor='hand2'
        )
        self.hint_button.pack(side='left', padx=5)
        
        self.check_button = tk.Button(
            button_frame,
            text="⚔️ ATTACK!",
            font=('Arial', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=30,
            pady=10,
            command=self.check_answer,
            relief='raised',
            bd=4,
            cursor='hand2'
        )
        self.check_button.pack(side='left', padx=10)
        
        self.next_button = tk.Button(
            button_frame,
            text="NEXT ➡️",
            font=('Arial', 16, 'bold'),
            bg=self.colors['success'],
            fg='white',
            padx=30,
            pady=10,
            command=self.new_question,
            relief='raised',
            bd=4,
            state='disabled',
            cursor='hand2'
        )
        self.next_button.pack(side='left', padx=10)
        
        # Result Frame
        self.result_label = tk.Label(
            question_frame,
            text="",
            font=('Arial', 13, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            wraplength=700
        )
        self.result_label.pack(pady=10)
        
        # Help button at bottom
        help_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=5)
        help_frame.pack(fill='x')
        
        help_button = tk.Button(
            help_frame,
            text="❓",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            padx=15,
            pady=5,
            command=self.show_help,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        help_button.pack(side='left', padx=20)
        
        self.answer_entry.focus()

    def draw_battlefield(self):
        # Ground
        self.battle_canvas.create_rectangle(
            0, 200, 850, 250,
            fill='#3d5a46',
            outline=''
        )
        # Hero
        self.hero_sprite = self.battle_canvas.create_text(
            self.hero_x, self.hero_y,
            text="🧙‍♂️",
            font=('Arial', 60),
            tags='hero'
        )
        # Monster
        self.monster_sprite = self.battle_canvas.create_text(
            self.monster_x, self.monster_y,
            text=self.current_monster['emoji'],
            font=('Arial', 70),
            tags='monster'
        )
    
    def animate_idle(self):
        if hasattr(self, 'hero_sprite'):
            offset = math.sin(self.root.winfo_width() * 0.05) * 2
            self.battle_canvas.coords(self.hero_sprite, self.hero_x, self.hero_y + offset)
        if hasattr(self, 'monster_sprite'):
            offset = math.cos(self.root.winfo_width() * 0.05) * 2
            self.battle_canvas.coords(self.monster_sprite, self.monster_x, self.monster_y + offset)
        self.root.after(50, self.animate_idle)
    
    def animate_hero_attack(self):
        steps = 10
        dx = (self.monster_x - self.hero_x) * 0.6 / steps
        def move_forward(step=0):
            if step < steps:
                self.battle_canvas.move('hero', dx, 0)
                self.root.after(30, lambda: move_forward(step + 1))
            else:
                self.create_impact_effect(self.monster_x - 50, self.monster_y)
                self.root.after(100, move_back)
        def move_back(step=0):
            if step < steps:
                self.battle_canvas.move('hero', -dx, 0)
                self.root.after(30, lambda: move_back(step + 1))
        move_forward()
    
    def animate_monster_attack(self):
        steps = 8
        dx = (self.hero_x - self.monster_x) * 0.5 / steps
        def move_forward(step=0):
            if step < steps:
                self.battle_canvas.move('monster', dx, 0)
                self.root.after(40, lambda: move_forward(step + 1))
            else:
                self.shake_screen()
                self.create_impact_effect(self.hero_x + 30, self.hero_y)
                self.root.after(100, move_back)
        def move_back(step=0):
            if step < steps:
                self.battle_canvas.move('monster', -dx, 0)
                self.root.after(40, lambda: move_back(step + 1))
        move_forward()
    
    def create_impact_effect(self, x, y):
        colors = ['#ff0000', '#ff6600', '#ffff00', '#ffffff']
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            color = random.choice(colors)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            particle = self.battle_canvas.create_oval(
                x-4, y-4, x+4, y+4,
                fill=color,
                outline=''
            )
            self.animate_particle(particle, dx, dy, 15)
    
    def animate_particle(self, particle, dx, dy, steps):
        def move(step=0):
            if step < steps:
                try:
                    self.battle_canvas.move(particle, dx, dy)
                    self.root.after(30, lambda: move(step + 1))
                except:
                    pass
            else:
                try:
                    self.battle_canvas.delete(particle)
                except:
                    pass
        move()
    
    def shake_screen(self):
        shake_amount = 8
        shakes = 6
        def shake(count=0):
            if count < shakes:
                offset = shake_amount if count % 2 == 0 else -shake_amount
                try:
                    self.battle_canvas.move('hero', offset, 0)
                    self.battle_canvas.move('monster', -offset, 0)
                except:
                    pass
                self.root.after(50, lambda: shake(count + 1))
            else:
                try:
                    hero_coords = self.battle_canvas.coords(self.hero_sprite)
                    monster_coords = self.battle_canvas.coords(self.monster_sprite)
                    self.battle_canvas.coords(self.hero_sprite, self.hero_x, hero_coords[1])
                    self.battle_canvas.coords(self.monster_sprite, self.monster_x, monster_coords[1])
                except:
                    pass
        shake()
    
    def show_floating_text(self, text, x, y, color):
        label = self.battle_canvas.create_text(
            x, y,
            text=text,
            font=('Arial', 24, 'bold'),
            fill=color,
            tags='floating'
        )
        def float_up(step=0):
            if step < 20:
                self.battle_canvas.move(label, 0, -3)
                try:
                    self.battle_canvas.itemconfig(label, font=('Arial', max(12, 24 - step), 'bold'))
                except:
                    pass
                self.root.after(50, lambda: float_up(step + 1))
            else:
                try:
                    self.battle_canvas.delete(label)
                except:
                    pass
        float_up()
    
    def show_hint(self):
        if not self.hint_available:
            return
        self.hints_used += 1
        self.hint_available = False
        self.hint_button.config(state='disabled', bg='#666666')
        if self.current_unit_to == "m":
            hint = "💡 To convert km → m: multiply by 1000"
        else:
            hint = "💡 To convert m → km: divide by 1000"
        messagebox.showinfo("💡 Hint", hint)

    # ------- TOP BANNER CONTROL -------
    def set_top_banner(self, text: str, bg=None, fg=None):
        if text:
            self.top_banner.config(
                text=text,
                bg=bg if bg is not None else self.colors['gold'],
                fg=fg if fg is not None else '#111111'
            )
        else:
            # Clear to background color and empty text
            self.top_banner.config(text="", bg=self.colors['bg'], fg=self.colors['text'])

    # ------- Optional: forbid padded zeros like 3.0, 2.50, 0005 -------
    def _has_unnecessary_zeros(self, s: str) -> bool:
        s = s.strip()
        if not s:
            return False
        if s[0] in "+-":
            s = s[1:]
        if "e" in s.lower():
            return False
        if s.startswith("0") and len(s) > 1 and not s.startswith("0."):
            return True
        if "." in s:
            int_part, frac_part = s.split(".", 1)
            if len(frac_part) > 0 and set(frac_part) == {"0"}:
                return True
            if len(frac_part) > 1 and frac_part.endswith("0"):
                return True
        return False
    
    def tolerance_from_sigfigs(self, true_value, sigfigs):
        if true_value == 0:
            return 1e-12
        magnitude = 10 ** (math.floor(math.log10(abs(true_value))) - sigfigs + 1)
        tol = 0.5 * magnitude
        return max(tol, 1e-9)

    def check_answer(self):
        user_input = self.answer_var.get().strip()
        if not user_input:
            messagebox.showwarning("⚠️", "Enter an answer first!")
            return

        # Optional formatting rule (remove if not needed)
        if self._has_unnecessary_zeros(user_input):
            messagebox.showerror(
                "🛑 Formatting",
                "Please avoid unnecessary zeros.\n"
                "Examples not allowed: 3.0, 2.50, 0005, 0.00\n"
                "Use the simplest form (e.g., 3, 2.5, 5, 0)."
            )
            return

        try:
            user_answer = float(user_input)
        except ValueError:
            messagebox.showerror("❌", "Please enter a number only!")
            return
        
        tolerance = self.tolerance_from_sigfigs(self.current_answer, self.current_sigfigs)
        is_correct = abs(user_answer - self.current_answer) <= tolerance
        self.total_questions += 1
        
        if is_correct:
            # Clear any previous top banner
            self.set_top_banner("")
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            
            dmg = self.calculate_hero_damage()
            self.monster_hp = max(0, self.monster_hp - dmg)
            
            # Animate attack
            self.animate_hero_attack()
            self.show_floating_text(f"-{dmg}", self.monster_x, self.monster_y - 40, '#ff3366')
            
            message = "⚔️ CRITICAL HIT!"
            if self.streak >= 3:
                message += f" 🔥 {self.streak} COMBO!"
            self.result_label.config(text=message, fg=self.colors['success'])
            
        else:
            self.streak = 0
            dmg = self.calculate_monster_damage()
            self.hero_hp = max(0, self.hero_hp - dmg)
            
            # Animate counter-attack
            self.root.after(800, self.animate_monster_attack)
            self.root.after(800, lambda: self.show_floating_text(f"-{dmg}", self.hero_x, self.hero_y - 40, '#ff3366'))
            
            correct = self.format_number(self.current_answer)
            tip = "× 1000" if self.current_unit_to == "m" else "÷ 1000"

            # >>> Show CORRECT ANSWER on TOP banner <<<
            self.set_top_banner(f"✅ Correct answer: {correct} {self.current_unit_to}")

            # Also keep bottom details
            message = f"❌ Wrong!\n💡 Use: {tip}"
            self.result_label.config(text=message, fg=self.colors['error'])
        
        self.update_displays()
        self.log_attempt(self.current_question, user_input, self.current_answer, is_correct)
        
        if self.monster_hp <= 0:
            self.root.after(1200, self.on_monster_defeated)
        elif self.hero_hp <= 0:
            self.root.after(1200, self.on_hero_defeated)
        else:
            self.check_button.config(state='disabled')
            self.next_button.config(state='normal')
            self.next_button.focus()
    
    def calculate_hero_damage(self):
        return self.hero_damage + (self.level - 1) * 2 + min(self.streak, 5)

    def calculate_monster_damage(self):
        return self.monster_damage + (self.level - 1) * 2

    def update_displays(self):
        # HP bars
        self.hero_hp_label.config(text=f"❤️ {self.hero_hp}/{self.hero_max_hp}")
        self.hero_hp_bar['maximum'] = self.hero_max_hp
        self.hero_hp_bar['value'] = self.hero_hp
        
        self.monster_hp_label.config(text=f"❤️ {self.monster_hp}/{self.monster_max_hp}")
        self.monster_hp_bar['maximum'] = self.monster_max_hp
        self.monster_hp_bar['value'] = self.monster_hp
        
        # Score
        percentage = (self.score / self.total_questions * 100) if self.total_questions else 0
        self.score_label.config(text=f"⭐ {self.score}/{self.total_questions} ({percentage:.0f}%)")
        
        # Streak
        self.streak_label.config(text=f"🔥 {self.streak} | Best: {self.best_streak}")
        
        # Level
        self.level_label.config(text=f"⚔️\nLV {self.level}")

    def on_monster_defeated(self):
        for _ in range(20):
            x = self.monster_x + random.randint(-30, 30)
            y = self.monster_y + random.randint(-30, 30)
            self.create_impact_effect(x, y)
        self.show_floating_text("💀 DEFEATED!", self.monster_x, self.monster_y, '#ff0000')
        
        self.level += 1
        self.monster_max_hp = int(self.base_monster_hp * (1.25 ** (self.level - 1)))
        self.monster_hp = self.monster_max_hp
        
        # New monster
        self.current_monster = random.choice(self.monster_types)
        
        # Heal hero
        heal = 25
        self.hero_hp = min(self.hero_max_hp, self.hero_hp + heal)
        
        if self.level % 3 == 0:
            self.hero_damage += 2
        
        # Redraw monster sprite
        self.battle_canvas.delete(self.monster_sprite)
        self.monster_sprite = self.battle_canvas.create_text(
            self.monster_x, self.monster_y,
            text=self.current_monster['emoji'],
            font=('Arial', 70),
            tags='monster'
        )
        
        self.monster_name_label.config(
            text=f"{self.current_monster['emoji']} {self.current_monster['name'].upper()}",
            fg=self.current_monster['color']
        )
        
        self.update_displays()
        self.result_label.config(
            text=f"🏆 VICTORY! Level {self.level}!\n💚 Recovered {heal} HP",
            fg=self.colors['gold']
        )
        
        self.check_button.config(state='disabled')
        self.next_button.config(state='normal')
        self.next_button.focus()

    def on_hero_defeated(self):
        for _ in range(15):
            x = self.hero_x + random.randint(-20, 20)
            y = self.hero_y + random.randint(-20, 20)
            self.create_impact_effect(x, y)
        self.show_floating_text("💀 DEFEATED!", self.hero_x, self.hero_y, '#ff0000')
        
        percentage = (self.score / self.total_questions * 100) if self.total_questions else 0
        stats = (f"⚔️ GAME OVER ⚔️\n\n"
                f"📊 Final Stats:\n"
                f"Score: {self.score}/{self.total_questions} ({percentage:.0f}%)\n"
                f"Best Streak: {self.best_streak}\n"
                f"Level Reached: {self.level}\n"
                f"Hints Used: {self.hints_used}\n\n"
                f"Thanks for playing!")
        messagebox.showinfo("💀 Defeated", stats)
        self.root.destroy()
    
    def log_attempt(self, question, user_answer, correct_answer, is_correct):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "✓" if is_correct else "✗"
        clean_question = question.replace('\n', ' ')
        log_entry = (f"[{timestamp}] {result} Q: {clean_question} | "
                    f"User: {user_answer} | Correct: {self.format_number(correct_answer)} | "
                    f"Streak: {self.streak} | Lv {self.level} | "
                    f"Hero {self.hero_hp}/{self.hero_max_hp} | "
                    f"Monster {self.monster_hp}/{self.monster_max_hp}\n")
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Log error: {e}")
    
    def show_help(self):
        help_text = """⚔️ BATTLE INSTRUCTIONS ⚔️

🎯 OBJECTIVE:
Convert distances correctly to attack the monster!
Defeat all monsters to level up!

⚔️ COMBAT:
• Correct answer = You attack the monster
• Wrong answer = Monster attacks you
• Build combos for bonus damage!

💡 CONVERSION:
• km → m: multiply by 1,000
• m → km: divide by 1,000

Example:
5 km = 5 × 1000 = 5000 m
3000 m = 3000 ÷ 1000 = 3 km

🔥 TIPS:
• Use hints wisely (💡 button)
• Build streaks for extra damage
• Watch your HP!
• Press Enter to submit

Good luck, warrior! ⚔️"""
        messagebox.showinfo("❓ Help", help_text)
    
    def run(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=== Battle Arena Log ===\n\n")
        self.root.mainloop()

if __name__ == "__main__":
    game = BattleConverterGame()
    game.run()
