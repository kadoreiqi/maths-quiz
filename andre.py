import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import math

class KidsConversionGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Distance Converter Adventure! 🌟")
        self.root.geometry("800x700")
        self.root.configure(bg='#FFE4E1')
        
        # Game state
        self.score = 0
        self.total_questions = 0
        self.current_question = ""
        self.current_answer = 0
        self.current_unit_from = ""
        self.current_unit_to = ""
        self.log_file = "kids_conversion_log.txt"
        
        # Colors
        self.colors = {
            'bg': '#FFE4E1',
            'primary': '#FF69B4',
            'secondary': '#98FB98',
            'success': '#32CD32',
            'error': '#FF6B6B',
            'text': '#2F4F4F',
            'button': '#87CEEB'
        }
        
        # Animation variables
        self.star_positions = []
        self.create_stars()
        
        self.setup_ui()
        self.new_question()
        
    def create_stars(self):
        """Create random star positions for background animation"""
        for _ in range(20):
            x = random.randint(50, 750)
            y = random.randint(50, 650)
            size = random.randint(1, 3)
            self.star_positions.append([x, y, size, random.uniform(0, 2*math.pi)])
    
    def setup_ui(self):
        """Create the main user interface"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=20)
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
        
        # Score Frame
        self.score_frame = tk.Frame(self.root, bg=self.colors['secondary'], pady=10)
        self.score_frame.pack(fill='x', padx=20, pady=10)
        
        self.score_label = tk.Label(
            self.score_frame,
            text="⭐ Score: 0/0 (0%)",
            font=('Comic Sans MS', 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['secondary']
        )
        self.score_label.pack()
        
        # Question Frame
        question_frame = tk.Frame(self.root, bg='white', pady=20, padx=20)
        question_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Spaceship emoji
        spaceship_label = tk.Label(
            question_frame,
            text="🚀",
            font=('Arial', 40),
            bg='white'
        )
        spaceship_label.pack(pady=10)
        
        self.question_label = tk.Label(
            question_frame,
            text="Loading question...",
            font=('Comic Sans MS', 18, 'bold'),
            fg=self.colors['text'],
            bg='white',
            wraplength=600
        )
        self.question_label.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(question_frame, bg='white')
        input_frame.pack(pady=20)
        
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
            font=('Comic Sans MS', 16),
            width=20,
            justify='center',
            bd=3,
            relief='ridge'
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())
        
        # Buttons Frame
        button_frame = tk.Frame(question_frame, bg='white')
        button_frame.pack(pady=20)
        
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
        self.result_frame.pack(pady=20)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=('Comic Sans MS', 16, 'bold'),
            bg='white'
        )
        self.result_label.pack()
        
        # Bottom Frame
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=10)
        bottom_frame.pack(fill='x')
        
        exit_button = tk.Button(
            bottom_frame,
            text="🚪 Exit Game",
            font=('Comic Sans MS', 12),
            bg=self.colors['error'],
            fg='white',
            padx=15,
            pady=5,
            command=self.exit_game,
            relief='raised',
            bd=2
        )
        exit_button.pack(side='right', padx=20)
        
        help_button = tk.Button(
            bottom_frame,
            text="❓ Help",
            font=('Comic Sans MS', 12),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            padx=15,
            pady=5,
            command=self.show_help,
            relief='raised',
            bd=2
        )
        help_button.pack(side='left', padx=20)
        
        # Focus on entry
        self.answer_entry.focus()
    
    def format_number(self, num):
        """Format number to remove trailing zeros"""
        formatted = f"{num:.10f}"
        formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    
    def generate_question(self):
        """Generate a random conversion question"""
        conversion_type = random.choice(["km_to_m", "m_to_km"])
        
        if conversion_type == "km_to_m":
            base = random.uniform(1, 999)
            sig_figs = random.randint(1, 4)  # Slightly easier for kids
            km_value = round(base, max(0, sig_figs - len(str(int(base)))))
            
            question = f"🚀 The spaceship traveled {self.format_number(km_value)} kilometers.\nHow many meters is that?"
            correct_answer = km_value * 1000
            unit_from = "km"
            unit_to = "m"
            
        else:
            base = random.uniform(1000, 50000)  # Smaller numbers for kids
            sig_figs = random.randint(1, 4)
            m_value = round(base, max(0, sig_figs - len(str(int(base)))))
            
            question = f"🌟 The rocket flew {self.format_number(m_value)} meters.\nHow many kilometers is that?"
            correct_answer = m_value / 1000
            unit_from = "m"
            unit_to = "km"
            
        return question, correct_answer, unit_from, unit_to
    
    def new_question(self):
        """Generate and display a new question"""
        self.current_question, self.current_answer, self.current_unit_from, self.current_unit_to = self.generate_question()
        
        self.question_label.config(text=self.current_question)
        self.answer_var.set("")
        self.result_label.config(text="")
        
        # Reset buttons
        self.check_button.config(state='normal')
        self.next_button.config(state='disabled')
        
        # Focus on entry
        self.answer_entry.focus()
    
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
        
        # Check if correct
        tolerance = abs(self.current_answer) * 1e-9 + 1e-12
        is_correct = abs(user_answer - self.current_answer) <= tolerance
        
        self.total_questions += 1
        
        if is_correct:
            self.score += 1
            self.result_label.config(
                text="🎉 AWESOME! You got it right! 🌟",
                fg=self.colors['success']
            )
            self.animate_success()
        else:
            self.result_label.config(
                text=f"🤗 Not quite! The answer is {self.format_number(self.current_answer)} {self.current_unit_to}\nKeep trying - you're learning! 💪",
                fg=self.colors['error']
            )
        
        # Update score
        self.update_score_display()
        
        # Log attempt
        self.log_attempt(self.current_question, user_input, self.current_answer, is_correct)
        
        # Enable next button, disable check button
        self.check_button.config(state='disabled')
        self.next_button.config(state='normal')
        self.next_button.focus()
    
    def animate_success(self):
        """Simple success animation"""
        original_bg = self.result_frame.cget('bg')
        self.result_frame.config(bg=self.colors['success'])
        self.root.after(200, lambda: self.result_frame.config(bg=original_bg))
    
    def update_score_display(self):
        """Update the score display"""
        if self.total_questions == 0:
            percentage = 0
        else:
            percentage = (self.score / self.total_questions) * 100
        
        score_text = f"⭐ Score: {self.score}/{self.total_questions} ({percentage:.0f}%)"
        
        if percentage >= 90:
            score_text += " 🏆 AMAZING!"
        elif percentage >= 70:
            score_text += " 🌟 GREAT JOB!"
        elif percentage >= 50:
            score_text += " 👍 GOOD WORK!"
        else:
            score_text += " 💪 KEEP GOING!"
        
        self.score_label.config(text=score_text)
    
    def log_attempt(self, question, user_answer, correct_answer, is_correct):
        """Log attempt to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "CORRECT" if is_correct else "INCORRECT"
        
        # Clean question text for logging
        clean_question = question.replace('\n', ' ')
        
        log_entry = f"[{timestamp}] Q: {clean_question} | User: {user_answer} | Correct: {self.format_number(correct_answer)} | {result}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Could not write to log: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🚀 How to Play:

1. Look at the question about distances
2. Type your answer in the box
3. Click 'Check Answer' or press Enter
4. See if you got it right!
5. Click 'Next Question' to continue

💡 Tips:
• 1 kilometer = 1000 meters
• To convert km to m: multiply by 1000
• To convert m to km: divide by 1000

Examples:
• 2 km = 2000 m
• 3000 m = 3 km

Have fun learning! 🌟"""
        
        messagebox.showinfo("Help - How to Play! 🎮", help_text)
    
    def exit_game(self):
        """Exit the game with final score"""
        if self.total_questions > 0:
            final_percentage = (self.score / self.total_questions) * 100
            
            if final_percentage >= 90:
                message = f"🏆 INCREDIBLE! You got {self.score}/{self.total_questions} correct ({final_percentage:.0f}%)!\n\nYou're a distance conversion superstar! 🌟"
            elif final_percentage >= 70:
                message = f"🌟 EXCELLENT! You got {self.score}/{self.total_questions} correct ({final_percentage:.0f}%)!\n\nGreat job learning! 👏"
            elif final_percentage >= 50:
                message = f"👍 GOOD WORK! You got {self.score}/{self.total_questions} correct ({final_percentage:.0f}%)!\n\nYou're getting better! Keep practicing! 💪"
            else:
                message = f"💪 You tried hard! You got {self.score}/{self.total_questions} correct ({final_percentage:.0f}%)!\n\nEvery mistake helps you learn! Try again soon! 🌈"
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