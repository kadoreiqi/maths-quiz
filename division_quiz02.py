import tkinter as tk
import random
import csv
import os
from datetime import datetime
from tkinter import scrolledtext


class DivisionQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Division Quiz Adventure! 🌟")
        self.master.geometry("900x800")
        
        # Colorful gradient background
        self.master.configure(bg="#FF6B9D")

        # Game state
        self.current_dividend = None
        self.current_divisor = None
        self.current_answer = None
        self.score = 0
        self.questions_asked = 0
        self.questions_answered = 0
        self.answered_correctly_this_question = False
        self.answered_this_question = False
        self.streak = 0  # Track correct answers in a row
        self.session_start_time = datetime.now()
        self.attempts_for_current_question = 0
        
        # Logging to CSV file
        self.log_file = "division_quiz_log.csv"
        self.init_log_file()
        
        # Activity log for display
        self.activity_log = []
        
        # Encouraging messages
        self.correct_messages = [
            "🌟 Amazing!", "🎉 Fantastic!", "⭐ Brilliant!", "🚀 Superstar!",
            "💫 Incredible!", "🏆 Perfect!", "✨ Wonderful!", "🎯 Bull's eye!",
            "🦸 You're a math hero!", "🌈 Outstanding!"
        ]
        self.try_again_messages = [
            "💪 Keep trying!", "🤔 Think it through!", "🎯 Almost there!",
            "🌟 You can do it!", "💡 Try again!", "🔍 Check your work!"
        ]

        # ---------- Fonts ----------
        self.title_font = ("Comic Sans MS", 28, "bold")
        self.question_font = ("Arial", 36, "bold")
        self.normal_font = ("Arial", 14)
        self.small_font = ("Arial", 11)

        # ---------- Header Frame ----------
        header_frame = tk.Frame(master, bg="#FF1493", height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = tk.Label(
            header_frame,
            text="🎮 Division Adventure! 🌟",
            font=self.title_font,
            bg="#FF1493",
            fg="white"
        )
        self.title_label.pack(pady=(10, 0))

        self.subtitle_label = tk.Label(
            header_frame,
            text="✨ Master the 2-12 times tables with division! ✨",
            font=self.normal_font,
            bg="#FF1493",
            fg="white"
        )
        self.subtitle_label.pack(pady=(0, 10))

        # ---------- Score & Streak ----------
        score_frame = tk.Frame(master, bg="#FFB6C1", bd=3, relief=tk.RAISED)
        score_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.score_label = tk.Label(
            score_frame,
            text="🏆 Score: 0 / 0",
            font=("Arial", 16, "bold"),
            bg="#FFB6C1",
            fg="#8B008B"
        )
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.streak_label = tk.Label(
            score_frame,
            text="🔥 Streak: 0",
            font=("Arial", 16, "bold"),
            bg="#FFB6C1",
            fg="#FF4500"
        )
        self.streak_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # ---------- Question area ----------
        question_outer_frame = tk.Frame(master, bg="#FF6B9D")
        question_outer_frame.pack(pady=20)
        
        question_frame = tk.Frame(
            question_outer_frame, 
            bg="#87CEEB", 
            bd=5, 
            relief=tk.RIDGE,
            padx=30,
            pady=20
        )
        question_frame.pack()

        self.question_number_label = tk.Label(
            question_frame,
            text="Question: 1",
            font=("Arial", 14, "bold"),
            bg="#87CEEB",
            fg="#00008B"
        )
        self.question_number_label.pack()

        self.question_label = tk.Label(
            question_frame,
            text="",
            font=self.question_font,
            bg="#87CEEB",
            fg="#000080"
        )
        self.question_label.pack(pady=15)

        # ---------- Answer entry ----------
        answer_frame = tk.Frame(master, bg="#98FB98", bd=4, relief=tk.GROOVE)
        answer_frame.pack(pady=15, padx=40, fill=tk.X)

        answer_label = tk.Label(
            answer_frame,
            text="✏️ Your answer:",
            font=("Arial", 16, "bold"),
            bg="#98FB98",
            fg="#006400"
        )
        answer_label.grid(row=0, column=0, padx=10, pady=15)

        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Arial", 24, "bold"),
            width=8,
            justify="center",
            bg="#FFFACD",
            fg="#000000",
            bd=3,
            relief=tk.SUNKEN
        )
        self.answer_entry.grid(row=0, column=1, padx=10, pady=15)

        # ---------- Buttons ----------
        button_frame = tk.Frame(master, bg="#FF6B9D")
        button_frame.pack(pady=15)

        self.check_button = tk.Button(
            button_frame,
            text="✓ Check Answer",
            font=("Arial", 14, "bold"),
            command=self.check_answer,
            width=14,
            bg="#32CD32",
            fg="white",
            activebackground="#228B22",
            bd=3,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.check_button.grid(row=0, column=0, padx=15, pady=5)

        self.next_button = tk.Button(
            button_frame,
            text="➤ Next Question",
            font=("Arial", 14, "bold"),
            command=self.new_question,
            width=14,
            state=tk.DISABLED,
            bg="#4169E1",
            fg="white",
            activebackground="#1E90FF",
            bd=3,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.next_button.grid(row=0, column=1, padx=15, pady=5)

        # ---------- Feedback & Hint ----------
        feedback_frame = tk.Frame(master, bg="#FFDAB9", bd=3, relief=tk.SUNKEN, height=60)
        feedback_frame.pack(pady=10, padx=30, fill=tk.X)
        feedback_frame.pack_propagate(False)
        
        self.feedback_label = tk.Label(
            feedback_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#FFDAB9"
        )
        self.feedback_label.pack(expand=True)

        # ---------- Always-visible Hint ----------
        hint_frame = tk.Frame(master, bg="#FFFFE0", bd=3, relief=tk.GROOVE)
        hint_frame.pack(pady=10, padx=30, fill=tk.X)
        
        self.hint_label = tk.Label(
            hint_frame,
            text="",
            font=("Arial", 15, "bold"),
            fg="#8B4513",
            bg="#FFFFE0",
            padx=10,
            pady=10
        )
        self.hint_label.pack()

        # ---------- Info for kids ----------
        info_frame = tk.Frame(master, bg="#E6E6FA", bd=2, relief=tk.RIDGE)
        info_frame.pack(pady=(10, 10), padx=30, fill=tk.X)
        
        self.info_label = tk.Label(
            info_frame,
            text="💭 Tip: Think about multiplication!\n"
                 "Example: 9 ÷ 3 = ?  →  What times 3 equals 9?",
            font=("Arial", 12),
            bg="#E6E6FA",
            fg="#4B0082",
            padx=10,
            pady=10
        )
        self.info_label.pack()

        # ---------- Activity Log Section ----------
        log_outer_frame = tk.Frame(master, bg="#FF6B9D")
        log_outer_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        log_header = tk.Label(
            log_outer_frame,
            text="📊 Activity Log",
            font=("Arial", 14, "bold"),
            bg="#9370DB",
            fg="white",
            pady=5
        )
        log_header.pack(fill=tk.X)
        
        # Scrolled text widget for the log
        self.log_text = scrolledtext.ScrolledText(
            log_outer_frame,
            font=("Courier", 9),
            bg="#F5F5DC",
            fg="#000000",
            height=8,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons for log management
        log_button_frame = tk.Frame(log_outer_frame, bg="#FF6B9D")
        log_button_frame.pack(pady=5)
        
        self.export_button = tk.Button(
            log_button_frame,
            text="📂 Show CSV Location",
            font=("Arial", 11, "bold"),
            command=self.export_log,
            bg="#9370DB",
            fg="white",
            activebackground="#8A2BE2",
            bd=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_log_button = tk.Button(
            log_button_frame,
            text="🗑️ Clear Display",
            font=("Arial", 11, "bold"),
            command=self.clear_log,
            bg="#DC143C",
            fg="white",
            activebackground="#B22222",
            bd=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.clear_log_button.pack(side=tk.LEFT, padx=5)
        
        # Initialize log with session start
        self.add_to_log(f"📅 Session started at {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.add_to_log("=" * 80)

        # Press Enter to check answer
        self.master.bind("<Return>", lambda event: self.check_answer())

        # Start with the first question
        self.new_question()

    def generate_question(self, min_factor=2, max_factor=12):
        """
        Generate a division question from 2–12 times tables.

        Pick a and b (2–12), then:
            dividend = a * b
            divisor  = b
            answer   = a

        So question is: dividend ÷ divisor = ?
        """
        a = random.randint(min_factor, max_factor)
        b = random.randint(min_factor, max_factor)
        dividend = a * b
        divisor = b
        answer = a
        return dividend, divisor, answer

    def animate_correct(self):
        """Create a celebration animation for correct answers"""
        colors = ["#FFD700", "#FF69B4", "#00FF00", "#FF1493", "#00BFFF"]
        
        def flash(count=0):
            if count < 6:
                self.feedback_label.config(bg=colors[count % len(colors)])
                self.master.after(100, lambda: flash(count + 1))
            else:
                self.feedback_label.config(bg="#FFDAB9")
        
        flash()
    
    def bounce_question(self):
        """Make the question bounce when showing new question"""
        original_size = 36
        
        def bounce(step=0, growing=True):
            if step < 8:
                if growing:
                    size = original_size + step * 2
                else:
                    size = original_size + (8 - step) * 2
                
                self.question_label.config(font=("Arial", size, "bold"))
                
                if step == 4:
                    growing = False
                
                next_step = step + 1 if growing else step + 1
                self.master.after(50, lambda: bounce(next_step, growing))
            else:
                self.question_label.config(font=("Arial", original_size, "bold"))
        
        bounce()

    def init_log_file(self):
        """Create log file with header if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "datetime",
                    "question_number",
                    "dividend",
                    "divisor",
                    "correct_answer",
                    "user_input",
                    "valid_input",
                    "is_correct",
                    "attempt_number_for_question",
                    "questions_answered_so_far",
                    "score_so_far",
                    "streak"
                ])

    def log_attempt_to_csv(self, user_input, valid_input, is_correct):
        """
        Log a single attempt to CSV file.

        - user_input: raw string from the entry box.
        - valid_input: True/False.
        - is_correct: True/False/None (None for invalid numeric state).
        """
        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")

        if is_correct is None:
            correct_str = ""
        else:
            correct_str = "yes" if is_correct else "no"

        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                self.questions_asked,
                self.current_dividend,
                self.current_divisor,
                self.current_answer,
                user_input,
                "yes" if valid_input else "no",
                correct_str,
                self.attempts_for_current_question,
                self.questions_answered,
                self.score,
                self.streak
            ])

    def add_to_log(self, message):
        """Add a message to the activity log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        self.log_text.config(state=tk.DISABLED)
        
    def log_attempt_to_display(self, question, user_answer, correct_answer, is_correct, is_first_attempt):
        """Log each answer attempt to the display"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = "✓ CORRECT" if is_correct else "✗ INCORRECT"
        
        # Format log message
        attempt_type = "[1st Attempt]" if is_first_attempt else "[Retry]"
        log_message = (f"[{timestamp}] Q{self.questions_asked}: {question} | "
                      f"Answer: {user_answer} | {result} {attempt_type} | "
                      f"Score: {self.score}/{self.questions_answered} | Streak: {self.streak}")
        
        self.add_to_log(log_message)
    
    
    def export_log(self):
        """Show the location of the CSV log file"""
        from tkinter import messagebox
        
        try:
            filepath = os.path.abspath(self.log_file)
            
            if os.path.exists(filepath):
                # Show success message box with file location
                messagebox.showinfo(
                    "Log File Location", 
                    f"CSV log file is saved at:\n\n{filepath}\n\nThis file is automatically updated with each attempt."
                )
                self.add_to_log(f"ℹ️ CSV log file location: {filepath}")
            else:
                messagebox.showwarning(
                    "Log File Not Found",
                    "No log file has been created yet. Answer some questions first!"
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error accessing log file: {str(e)}"
            )

    
    
    def clear_log(self):
        """Clear the activity log display only (CSV file remains)"""
        from tkinter import messagebox
        
        # Ask for confirmation
        response = messagebox.askyesno(
            "Clear Display Log",
            "This will clear the display log only.\nThe CSV file will remain intact.\n\nContinue?"
        )
        
        if response:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)
            
            self.add_to_log(f"📅 Display cleared at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.add_to_log("=" * 80)
            self.add_to_log(f"ℹ️ CSV log file continues at: {os.path.abspath(self.log_file)}")
            
            self.feedback_label.config(
                text="🗑️ Display log cleared!",
                fg="#FF8C00",
                bg="#FFDAB9"
            )

    def new_question(self):
        self.current_dividend, self.current_divisor, self.current_answer = self.generate_question()
        self.questions_asked += 1
        self.answered_correctly_this_question = False
        self.answered_this_question = False
        self.attempts_for_current_question = 0

        # Update question display
        self.question_number_label.config(text=f"Question: {self.questions_asked}")
        question_text = f"{self.current_dividend} ÷ {self.current_divisor} = ?"
        self.question_label.config(text=question_text)
        
        # Log new question
        self.add_to_log(f"\n🎯 Question {self.questions_asked}: {question_text}")
        
        # Always show hint for every question
        self.hint_label.config(
            text=f"💡 Hint: What times {self.current_divisor} equals {self.current_dividend}?"
        )
        
        # Bounce animation for new question
        self.bounce_question()

        # Clear entry and feedback
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        self.feedback_label.config(text="", fg="black", bg="#FFDAB9")

        # Lock Next Question until they give a CORRECT answer
        self.next_button.config(state=tk.DISABLED)

        self.update_score_label()

    def update_score_label(self):
        # Score out of the number of questions the child has attempted
        self.score_label.config(
            text=f"🏆 Score: {self.score} / {self.questions_answered}"
        )
        self.streak_label.config(
            text=f"🔥 Streak: {self.streak}"
        )

    def check_answer(self):
        user_input = self.answer_entry.get().strip()

        # Empty input → not counted as attempt, no log
        if not user_input:
            self.feedback_label.config(
                text="⚠️ Please type an answer first!",
                fg="#FF4500",
                bg="#FFDAB9"
            )
            self.next_button.config(state=tk.DISABLED)
            return

        # Count this as an attempt for this question
        self.attempts_for_current_question += 1

        # Non-numeric input → log as invalid attempt
        if not user_input.isdigit():
            self.feedback_label.config(
                text="⚠️ Please enter a whole number!",
                fg="#FF4500",
                bg="#FFDAB9"
            )
            self.next_button.config(state=tk.DISABLED)
            # Log to CSV
            self.log_attempt_to_csv(user_input=user_input, valid_input=False, is_correct=None)
            return

        user_answer = int(user_input)
        
        # Determine if this is the first attempt for this question
        is_first_attempt = not self.answered_this_question

        # First valid numeric answer for this question → count it as "answered"
        if not self.answered_this_question:
            self.questions_answered += 1
            self.answered_this_question = True

        # Create question string for logging
        question_str = f"{self.current_dividend} ÷ {self.current_divisor} = ?"

        if user_answer == self.current_answer:
            # Only count the first correct attempt for this question toward score
            if not self.answered_correctly_this_question:
                self.score += 1
                self.streak += 1
                self.answered_correctly_this_question = True
            
            # Log to CSV
            self.log_attempt_to_csv(user_input=user_input, valid_input=True, is_correct=True)
            
            # Log to display
            self.log_attempt_to_display(question_str, user_answer, self.current_answer, True, is_first_attempt)
            
            # Random encouraging message
            message = random.choice(self.correct_messages)
            
            # Extra praise for streaks
            streak_bonus = ""
            if self.streak >= 5:
                streak_bonus = f" 🔥 {self.streak} in a row! ON FIRE! 🔥"
            elif self.streak >= 3:
                streak_bonus = f" ⚡ {self.streak} streak! Keep going! ⚡"

            self.feedback_label.config(
                text=f"{message} {self.current_answer} × {self.current_divisor} = {self.current_dividend}{streak_bonus}",
                fg="#006400",
                bg="#FFDAB9"
            )
            
            # Celebration animation
            self.animate_correct()
            
            # NOW allow moving to the next question
            self.next_button.config(state=tk.NORMAL)
        else:
            # Reset streak on wrong answer
            self.streak = 0
            
            # Log to CSV
            self.log_attempt_to_csv(user_input=user_input, valid_input=True, is_correct=False)
            
            # Log to display
            self.log_attempt_to_display(question_str, user_answer, self.current_answer, False, is_first_attempt)
            
            message = random.choice(self.try_again_messages)
            self.feedback_label.config(
                text=f"{message}",
                fg="#DC143C",
                bg="#FFDAB9"
            )
            # Keep Next disabled until they get it right
            self.next_button.config(state=tk.DISABLED)

        self.update_score_label()


def main():
    root = tk.Tk()
    app = DivisionQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()