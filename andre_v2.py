import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import math
from collections import deque

class KidsConversionGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Distance Converter Adventure! 🌟")
        self.root.geometry("850x750")
        self.root.configure(bg='#FFE4E1')
        
        # Game state
        self.score = 0
        self.total_questions = 0
        self.current_question = ""
        self.current_answer = 0.0
        self.current_unit_from = ""
        self.current_unit_to = ""
        self.current_sigfigs = 3
        self.prev_conversion_type = None
        self.recent_q = deque(maxlen=20)  # remember more recent questions
        self.log_file = "kids_conversion_log.txt"
        
        # New interactive features
        self.streak = 0
        self.best_streak = 0
        self.hints_used = 0
        self.hint_available = True
        self.difficulty_level = 1  # 1-3
        self.achievements = []
        
        # Colors
        self.colors = {
            'bg': '#FFE4E1',
            'primary': '#FF69B4',
            'secondary': '#98FB98',
            'success': '#32CD32',
            'error': '#FF6B6B',
            'text': '#2F4F4F',
            'button': '#87CEEB',
            'hint': '#FFD700',
            'streak': '#FF8C00'
        }
        
        # Fun messages
        self.correct_messages = [
            "🎉 AWESOME! You're a math wizard!",
            "⭐ FANTASTIC! That's exactly right!",
            "🌟 BRILLIANT! You're on fire!",
            "🚀 AMAZING! You're crushing it!",
            "💫 SPECTACULAR! Keep it up!",
            "🏆 PERFECT! You're unstoppable!",
            "✨ INCREDIBLE! You got it!"
        ]
        
        self.encouragement_messages = [
            "Don't worry! Every mistake is a chance to learn! 💪",
            "Almost there! You're getting closer! 🌈",
            "Nice try! Let's learn from this! 📚",
            "Keep going! Practice makes perfect! 🎯",
            "Great effort! You're improving! ⭐",
            "No worries! You'll get the next one! 🌟"
        ]
        
        # Animation variables
        self.star_positions = []
        self.create_stars()
        
        self.setup_ui()
        self.new_question()
        
    def create_stars(self):
        """Create random star positions for background animation"""
        for _ in range(25):
            x = random.randint(50, 800)
            y = random.randint(50, 700)
            size = random.randint(1, 3)
            self.star_positions.append([x, y, size, random.uniform(0, 2*math.pi)])
    
    # --------- number helpers ---------
    def round_sig(self, x, sig):
        """Round to a number of significant figures (1–4)."""
        if x == 0:
            return 0.0
        if sig < 1:
            sig = 1
        if sig > 6:
            sig = 6
        return float(f"{x:.{sig}g}")

    def format_number(self, num):
        """Format number (no trailing zeros; avoid sci-notation for our ranges)."""
        if abs(num - int(num)) < 1e-12:
            return str(int(num))
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        return formatted
    
    # --------- enhanced question generation ---------
    def get_difficulty_ranges(self):
        """Get value ranges based on current difficulty level"""
        if self.difficulty_level == 1:
            # Easy: nice round numbers
            km_range = (1, 100)
            m_range = (1000, 10000)
        elif self.difficulty_level == 2:
            # Medium: wider range
            km_range = (1, 500)
            m_range = (1000, 30000)
        else:
            # Hard: full range with decimals
            km_range = (0.5, 999)
            m_range = (500, 50000)
        
        return km_range, m_range
    
    def generate_question_once(self, force_type=None):
        """Generate one candidate question with better variation."""
        # Decide conversion type with better alternation
        if force_type is not None:
            conversion_type = force_type
        else:
            choices = ["km_to_m", "m_to_km"]
            if self.prev_conversion_type in choices:
                other = "m_to_km" if self.prev_conversion_type == "km_to_m" else "km_to_m"
                # Strong preference for alternating
                conversion_type = random.choices([other, self.prev_conversion_type], weights=[0.85, 0.15])[0]
            else:
                conversion_type = random.choice(choices)

        # Varied sig figs (1-4) with preference for 2-3
        sig_figs = random.choices([1, 2, 3, 4], weights=[1, 3, 3, 2])[0]
        
        # Get difficulty-based ranges
        km_range, m_range = self.get_difficulty_ranges()

        # Fun question templates
        km_templates = [
            "🚀 The spaceship traveled {val} kilometers.\nHow many meters is that?",
            "🌙 The moon rover drove {val} km across the surface.\nConvert to meters!",
            "✈️ The airplane flew {val} kilometers.\nWhat's that in meters?",
            "🏃 The marathon runner completed {val} km.\nHow many meters did they run?",
            "🚂 The train traveled {val} kilometers.\nExpress this in meters!",
            "🎈 The hot air balloon drifted {val} km.\nHow many meters is that?"
        ]
        
        m_templates = [
            "🌟 The rocket flew {val} meters into the sky.\nHow many kilometers is that?",
            "🏊 The swimmer completed {val} meters.\nConvert to kilometers!",
            "🚴 The cyclist rode {val} meters.\nWhat's that in kilometers?",
            "🎯 The arrow flew {val} meters.\nExpress this in kilometers!",
            "🦘 The kangaroo hopped {val} meters total.\nHow many km did it hop?",
            "⛷️ The skier descended {val} meters.\nConvert to kilometers!"
        ]

        if conversion_type == "km_to_m":
            raw = random.uniform(*km_range)
            # Add some variety: sometimes use nice round numbers
            if random.random() < 0.3 and sig_figs <= 2:
                raw = round(raw / 10) * 10  # Round to nearest 10
            
            km_value = self.round_sig(raw, sig_figs)
            template = random.choice(km_templates)
            question = template.format(val=self.format_number(km_value))
            correct_answer = km_value * 1000
            unit_from, unit_to = "km", "m"
            value_key = f"{conversion_type}:{self.format_number(km_value)}"

        else:  # m_to_km
            raw = random.uniform(*m_range)
            # Sometimes use multiples of 1000 for easier division
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
        """Generate a non-repeating, robust question (up to 100 tries)."""
        for attempt in range(100):
            q = self.generate_question_once()
            question, correct_answer, unit_from, unit_to, sig_figs, conversion_type, value_key = q
            
            # More strict anti-repeat logic
            if value_key not in self.recent_q:
                # Avoid immediate same direction (first 10 attempts)
                if attempt < 10 and self.prev_conversion_type == conversion_type:
                    continue
                return q
        
        # If still failing, force alternate direction
        alternate = "m_to_km" if self.prev_conversion_type == "km_to_m" else "km_to_m"
        return self.generate_question_once(force_type=alternate)

    def new_question(self):
        """Generate and display a new question"""
        (self.current_question,
         self.current_answer,
         self.current_unit_from,
         self.current_unit_to,
         self.current_sigfigs,
         conversion_type,
         value_key) = self.generate_question()
        
        self.prev_conversion_type = conversion_type
        self.recent_q.append(value_key)
        
        # Auto-adjust difficulty based on performance
        if self.total_questions > 0 and self.total_questions % 10 == 0:
            accuracy = (self.score / self.total_questions) * 100
            if accuracy >= 85 and self.difficulty_level < 3:
                self.difficulty_level += 1
                self.show_notification(f"🎊 Level Up! Difficulty increased to {self.difficulty_level}!")
            elif accuracy < 50 and self.difficulty_level > 1:
                self.difficulty_level -= 1
                self.show_notification(f"💪 Taking it easier! Difficulty adjusted to {self.difficulty_level}")

        self.question_label.config(text=self.current_question)
        self.answer_var.set("")
        self.result_label.config(text="")
        
        # Reset hint availability
        self.hint_available = True
        self.hint_button.config(state='normal', bg=self.colors['hint'])
        
        # Reset buttons
        self.check_button.config(state='normal')
        self.next_button.config(state='disabled')
        
        # Focus on entry
        self.answer_entry.focus()
    
    # --------- UI ---------
    def setup_ui(self):
        """Create the main user interface"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=15)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(
            title_frame, 
            text="🚀 Distance Converter Adventure! 🌟",
            font=('Comic Sans MS', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Help the space explorer convert distances!",
            font=('Comic Sans MS', 12),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        subtitle_label.pack()
        
        # Score Frame with streak
        self.score_frame = tk.Frame(self.root, bg=self.colors['secondary'], pady=10)
        self.score_frame.pack(fill='x', padx=20, pady=5)
        
        self.score_label = tk.Label(
            self.score_frame,
            text="⭐ Score: 0/0 (0%)",
            font=('Comic Sans MS', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['secondary']
        )
        self.score_label.pack()
        
        self.streak_label = tk.Label(
            self.score_frame,
            text="🔥 Streak: 0 | Best: 0",
            font=('Comic Sans MS', 12),
            fg=self.colors['streak'],
            bg=self.colors['secondary']
        )
        self.streak_label.pack()
        
        # Question Frame
        question_frame = tk.Frame(self.root, bg='white', pady=20, padx=20)
        question_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Animated spaceship emoji
        spaceship_label = tk.Label(
            question_frame,
            text="🚀",
            font=('Arial', 40),
            bg='white'
        )
        spaceship_label.pack(pady=5)
        
        self.question_label = tk.Label(
            question_frame,
            text="Loading question...",
            font=('Comic Sans MS', 18, 'bold'),
            fg=self.colors['text'],
            bg='white',
            wraplength=650,
            justify='center'
        )
        self.question_label.pack(pady=15)
        
        # Input Frame
        input_frame = tk.Frame(question_frame, bg='white')
        input_frame.pack(pady=15)
        
        tk.Label(
            input_frame,
            text="Your Answer:",
            font=('Comic Sans MS', 14, 'bold'),
            fg=self.colors['text'],
            bg='white'
        ).pack()
        
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(
            input_frame,
            textvariable=self.answer_var,
            font=('Comic Sans MS', 18),
            width=20,
            justify='center',
            bd=3,
            relief='ridge'
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())
        
        # Buttons Frame
        button_frame = tk.Frame(question_frame, bg='white')
        button_frame.pack(pady=15)
        
        self.hint_button = tk.Button(
            button_frame,
            text="💡 Hint",
            font=('Comic Sans MS', 12, 'bold'),
            bg=self.colors['hint'],
            fg='white',
            padx=15,
            pady=8,
            command=self.show_hint,
            relief='raised',
            bd=3
        )
        self.hint_button.pack(side='left', padx=5)
        
        self.check_button = tk.Button(
            button_frame,
            text="🎯 Check Answer!",
            font=('Comic Sans MS', 14, 'bold'),
            bg=self.colors['button'],
            fg='white',
            padx=20,
            pady=10,
            command=self.check_answer,
            relief='raised',
            bd=3
        )
        self.check_button.pack(side='left', padx=10)
        
        self.next_button = tk.Button(
            button_frame,
            text="➡️ Next Question",
            font=('Comic Sans MS', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.new_question,
            relief='raised',
            bd=3,
            state='disabled'
        )
        self.next_button.pack(side='left', padx=10)
        
        # Result Frame
        self.result_frame = tk.Frame(question_frame, bg='white')
        self.result_frame.pack(pady=15)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=('Comic Sans MS', 16, 'bold'),
            bg='white',
            wraplength=700,
            justify='center'
        )
        self.result_label.pack()
        
        # Bottom Frame
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=10)
        bottom_frame.pack(fill='x')
        
        help_button = tk.Button(
            bottom_frame,
            text="❓ Help",
            font=('Comic Sans MS', 11),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            padx=15,
            pady=5,
            command=self.show_help,
            relief='raised',
            bd=2
        )
        help_button.pack(side='left', padx=20)
        
        achievements_button = tk.Button(
            bottom_frame,
            text="🏆 Achievements",
            font=('Comic Sans MS', 11),
            bg='#FFD700',
            fg=self.colors['text'],
            padx=15,
            pady=5,
            command=self.show_achievements,
            relief='raised',
            bd=2
        )
        achievements_button.pack(side='left', padx=5)
        
        exit_button = tk.Button(
            bottom_frame,
            text="🚪 Exit Game",
            font=('Comic Sans MS', 11),
            bg=self.colors['error'],
            fg='white',
            padx=15,
            pady=5,
            command=self.exit_game,
            relief='raised',
            bd=2
        )
        exit_button.pack(side='right', padx=20)
        
        # Focus on entry
        self.answer_entry.focus()
    
    # --------- interactive features ---------
    def show_hint(self):
        """Show a helpful hint"""
        if not self.hint_available:
            return
        
        self.hints_used += 1
        self.hint_available = False
        self.hint_button.config(state='disabled', bg='#CCCCCC')
        
        if self.current_unit_to == "m":
            hint = f"💡 Hint: To convert km to m, multiply by 1000!\n\nSo {self.format_number(float(self.current_question.split()[3]))} × 1000 = ?"
        else:
            hint = f"💡 Hint: To convert m to km, divide by 1000!\n\nSo {self.format_number(float(self.current_question.split()[3]))} ÷ 1000 = ?"
        
        messagebox.showinfo("💡 Helpful Hint!", hint)
    
    def show_notification(self, message):
        """Show a brief notification"""
        notification = tk.Toplevel(self.root)
        notification.title("Notification")
        notification.geometry("300x100")
        notification.configure(bg='#FFD700')
        
        label = tk.Label(
            notification,
            text=message,
            font=('Comic Sans MS', 12, 'bold'),
            bg='#FFD700',
            fg='white',
            wraplength=280
        )
        label.pack(expand=True)
        
        notification.after(2000, notification.destroy)
    
    def check_achievements(self):
        """Check and award achievements"""
        new_achievements = []
        
        if self.streak >= 5 and "5 Streak" not in self.achievements:
            new_achievements.append("🔥 5 in a Row!")
            self.achievements.append("5 Streak")
        
        if self.streak >= 10 and "10 Streak" not in self.achievements:
            new_achievements.append("🌟 Perfect 10 Streak!")
            self.achievements.append("10 Streak")
        
        if self.score >= 20 and "20 Correct" not in self.achievements:
            new_achievements.append("⭐ 20 Correct Answers!")
            self.achievements.append("20 Correct")
        
        if self.total_questions >= 50 and "50 Questions" not in self.achievements:
            new_achievements.append("🎯 50 Questions Attempted!")
            self.achievements.append("50 Questions")
        
        if self.total_questions > 0:
            accuracy = (self.score / self.total_questions) * 100
            if accuracy == 100 and self.total_questions >= 10 and "Perfect" not in self.achievements:
                new_achievements.append("💎 Perfect Score!")
                self.achievements.append("Perfect")
        
        for achievement in new_achievements:
            self.show_notification(f"🏆 Achievement Unlocked!\n{achievement}")
    
    def show_achievements(self):
        """Display achievements"""
        if not self.achievements:
            message = "🏆 No achievements yet!\n\nKeep playing to unlock achievements:\n\n" \
                     "🔥 5 in a Row\n🌟 Perfect 10 Streak\n⭐ 20 Correct Answers\n" \
                     "🎯 50 Questions Attempted\n💎 Perfect Score (10+ questions)"
        else:
            message = f"🏆 Your Achievements ({len(self.achievements)}):\n\n"
            achievement_names = {
                "5 Streak": "🔥 5 in a Row!",
                "10 Streak": "🌟 Perfect 10 Streak!",
                "20 Correct": "⭐ 20 Correct Answers!",
                "50 Questions": "🎯 50 Questions Attempted!",
                "Perfect": "💎 Perfect Score!"
            }
            for ach in self.achievements:
                message += f"✓ {achievement_names.get(ach, ach)}\n"
        
        messagebox.showinfo("🏆 Achievements", message)
    
    # --------- checking logic ---------
    def tolerance_from_sigfigs(self, true_value, sigfigs):
        """Set a forgiving tolerance based on displayed significant figures."""
        if true_value == 0:
            return 1e-12
        magnitude = 10 ** (math.floor(math.log10(abs(true_value))) - sigfigs + 1)
        tol = 0.5 * magnitude
        return max(tol, 1e-9)

    def check_answer(self):
        """Check the user's answer"""
        user_input = self.answer_var.get().strip()
        
        if not user_input:
            messagebox.showwarning("Oops! 🤔", "Please enter an answer first!")
            return
        
        try:
            user_answer = float(user_input)
        except ValueError:
            messagebox.showerror("Invalid Input! 😵", "Please enter a number only!\n\nFor example: 1500 or 2.5")
            return
        
        # Check if correct within tolerance
        tolerance = self.tolerance_from_sigfigs(self.current_answer, self.current_sigfigs)
        is_correct = abs(user_answer - self.current_answer) <= tolerance
        
        self.total_questions += 1
        
        if is_correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            
            # Random encouraging message
            message = random.choice(self.correct_messages)
            if self.streak >= 3:
                message += f"\n🔥 {self.streak} in a row!"
            
            self.result_label.config(text=message, fg=self.colors['success'])
            self.animate_success()
            self.check_achievements()
        else:
            self.streak = 0
            
            # ALWAYS show correct answer clearly
            correct = self.format_number(self.current_answer)
            tip = "Multiply by 1000" if self.current_unit_to == "m" else "Divide by 1000"
            encouragement = random.choice(self.encouragement_messages)
            
            self.result_label.config(
                text=(
                    f"{encouragement}\n\n"
                    f"✅ Correct answer: {correct} {self.current_unit_to}\n\n"
                    f"💡 Remember: {tip}\n"
                    f"   to convert {self.current_unit_from} → {self.current_unit_to}"
                ),
                fg=self.colors['error']
            )
            self.animate_wrong()
        
        # Update displays
        self.update_score_display()
        self.update_streak_display()
        
        # Log attempt
        self.log_attempt(self.current_question, user_input, self.current_answer, is_correct)
        
        # Enable next button, disable check button
        self.check_button.config(state='disabled')
        self.next_button.config(state='normal')
        self.next_button.focus()
    
    def animate_success(self):
        """Success animation with color flash"""
        original_bg = self.result_frame.cget('bg')
        colors = [self.colors['success'], '#90EE90', self.colors['success'], original_bg]
        
        def flash(index=0):
            if index < len(colors):
                self.result_frame.config(bg=colors[index])
                self.root.after(150, lambda: flash(index + 1))
        
        flash()
    
    def animate_wrong(self):
        """Gentle animation for incorrect answer"""
        original_bg = self.result_frame.cget('bg')
        self.result_frame.config(bg='#FFB6C1')
        self.root.after(200, lambda: self.result_frame.config(bg=original_bg))
    
    def update_score_display(self):
        """Update the score display with encouragement"""
        if self.total_questions == 0:
            percentage = 0
        else:
            percentage = (self.score / self.total_questions) * 100
        
        score_text = f"⭐ Score: {self.score}/{self.total_questions} ({percentage:.0f}%)"
        
        if percentage >= 90:
            score_text += " 🏆 AMAZING!"
        elif percentage >= 80:
            score_text += " 🌟 EXCELLENT!"
        elif percentage >= 70:
            score_text += " 💫 GREAT!"
        elif percentage >= 60:
            score_text += " 👍 GOOD!"
        elif percentage >= 50:
            score_text += " 💪 KEEP GOING!"
        else:
            score_text += " 🌈 LEARNING!"
        
        self.score_label.config(text=score_text)
    
    def update_streak_display(self):
        """Update streak display"""
        self.streak_label.config(
            text=f"🔥 Streak: {self.streak} | Best: {self.best_streak} | Level: {self.difficulty_level}"
        )
    
    def log_attempt(self, question, user_answer, correct_answer, is_correct):
        """Log attempt to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "CORRECT" if is_correct else "INCORRECT"
        clean_question = question.replace('\n', ' ')
        
        log_entry = (f"[{timestamp}] Q: {clean_question} | "
                    f"User: {user_answer} | Correct: {self.format_number(correct_answer)} | "
                    f"{result} | Streak: {self.streak} | Level: {self.difficulty_level}\n")
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Could not write to log: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🚀 How to Play:

1. Read the distance conversion question
2. Type your answer in the box
3. Click 'Check Answer' or press Enter
4. Use hints if you need help (💡 button)
5. Track your streak and achievements!

💡 Quick Reference:
• 1 kilometer = 1,000 meters
• km → m: multiply by 1000
• m → km: divide by 1000

Examples:
• 2.5 km = 2,500 m
• 5,000 m = 5 km

🎯 Features:
• Your difficulty adjusts automatically
• Build streaks for bonus achievements
• Track your progress over time

Have fun learning! 🌟"""
        
        messagebox.showinfo("Help - How to Play! 🎮", help_text)
    
    def exit_game(self):
        """Exit the game with final stats"""
        if self.total_questions > 0:
            final_percentage = (self.score / self.total_questions) * 100
            
            stats = (f"📊 Final Stats:\n"
                    f"   Score: {self.score}/{self.total_questions} ({final_percentage:.0f}%)\n"
                    f"   Best Streak: {self.best_streak}\n"
                    f"   Hints Used: {self.hints_used}\n"
                    f"   Level Reached: {self.difficulty_level}\n"
                    f"   Achievements: {len(self.achievements)}\n\n")
            
            if final_percentage >= 90:
                message = f"🏆 INCREDIBLE!\n\n{stats}You're a distance conversion superstar! 🌟"
            elif final_percentage >= 75:
                message = f"🌟 EXCELLENT!\n\n{stats}You're doing amazing! Keep it up! 💫"
            elif final_percentage >= 60:
                message = f"👍 GOOD WORK!\n\n{stats}You're improving steadily! 💪"
            else:
                message = f"💪 GREAT EFFORT!\n\n{stats}Every question helps you learn more! 🌈"
        else:
            message = "Thanks for trying the Distance Converter Adventure! 🚀\n\nCome back anytime to practice!"
        
        messagebox.showinfo("Thanks for Playing! 👋", message)
        self.root.destroy()
    
    def run(self):
        """Start the game"""
        # Initialize log file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=== Kids Distance Conversion Game Log ===\n\n")
        
        self.root.mainloop()

if __name__ == "__main__":
    game = KidsConversionGame()
    game.run()