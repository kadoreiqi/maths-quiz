import tkinter as tk
import random


class DivisionQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Division Quiz Adventure! 🌟")
        self.master.geometry("700x750")
        
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
        info_frame.pack(pady=(10, 15), padx=30, fill=tk.X)
        
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

    def new_question(self):
        self.current_dividend, self.current_divisor, self.current_answer = self.generate_question()
        self.questions_asked += 1
        self.answered_correctly_this_question = False
        self.answered_this_question = False

        # Update question display
        self.question_number_label.config(text=f"Question: {self.questions_asked}")
        self.question_label.config(
            text=f"{self.current_dividend} ÷ {self.current_divisor} = ?"
        )
        
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

        if not user_input:
            self.feedback_label.config(
                text="⚠️ Please type an answer first!",
                fg="#FF4500",
                bg="#FFDAB9"
            )
            self.next_button.config(state=tk.DISABLED)
            return

        if not user_input.isdigit():
            self.feedback_label.config(
                text="⚠️ Please enter a whole number!",
                fg="#FF4500",
                bg="#FFDAB9"
            )
            self.next_button.config(state=tk.DISABLED)
            return

        user_answer = int(user_input)

        # First valid numeric answer for this question → count it as "answered"
        if not self.answered_this_question:
            self.questions_answered += 1
            self.answered_this_question = True

        if user_answer == self.current_answer:
            # Only count the first correct attempt for this question toward score
            if not self.answered_correctly_this_question:
                self.score += 1
                self.streak += 1
                self.answered_correctly_this_question = True
            
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