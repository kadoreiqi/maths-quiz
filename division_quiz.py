import tkinter as tk
import random


class DivisionQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Division Quiz – 2–12 Times Tables")
        self.master.configure(bg="#f0f8ff")  # light blue-ish background

        # Game state
        self.current_dividend = None
        self.current_divisor = None
        self.current_answer = None
        self.score = 0
        self.questions_asked = 0           # how many questions have been shown
        self.questions_answered = 0        # how many questions the child actually answered
        self.answered_correctly_this_question = False
        self.answered_this_question = False  # at least one valid numeric answer given

        # ---------- Fonts ----------
        self.title_font = ("Arial", 22, "bold")
        self.question_font = ("Arial", 24, "bold")
        self.normal_font = ("Arial", 16)
        self.small_font = ("Arial", 12)

        # ---------- Title ----------
        self.title_label = tk.Label(
            master,
            text="Division Practice Game",
            font=self.title_font,
            bg="#f0f8ff"
        )
        self.title_label.pack(pady=(15, 5))

        self.subtitle_label = tk.Label(
            master,
            text="Practice 2–12 times tables using division!",
            font=self.normal_font,
            bg="#f0f8ff"
        )
        self.subtitle_label.pack(pady=(0, 15))

        # ---------- Score ----------
        self.score_label = tk.Label(
            master,
            text="Score: 0 / 0",
            font=self.normal_font,
            bg="#f0f8ff"
        )
        self.score_label.pack()

        # ---------- Question area ----------
        question_frame = tk.Frame(master, bg="#f0f8ff")
        question_frame.pack(pady=20)

        self.question_number_label = tk.Label(
            question_frame,
            text="Question: 1",
            font=self.normal_font,
            bg="#f0f8ff"
        )
        self.question_number_label.pack()

        self.question_label = tk.Label(
            question_frame,
            text="",
            font=self.question_font,
            bg="#f0f8ff"
        )
        self.question_label.pack(pady=10)

        # ---------- Answer entry ----------
        answer_frame = tk.Frame(master, bg="#f0f8ff")
        answer_frame.pack(pady=10)

        answer_label = tk.Label(
            answer_frame,
            text="Your answer:",
            font=self.normal_font,
            bg="#f0f8ff"
        )
        answer_label.grid(row=0, column=0, padx=5)

        self.answer_entry = tk.Entry(
            answer_frame,
            font=self.normal_font,
            width=5,
            justify="center"
        )
        self.answer_entry.grid(row=0, column=1, padx=5)

        # ---------- Buttons (Check + Next only) ----------
        button_frame = tk.Frame(master, bg="#f0f8ff")
        button_frame.pack(pady=15)

        self.check_button = tk.Button(
            button_frame,
            text="Check Answer",
            font=self.normal_font,
            command=self.check_answer,
            width=12
        )
        self.check_button.grid(row=0, column=0, padx=10, pady=5)

        # Next Question starts DISABLED
        self.next_button = tk.Button(
            button_frame,
            text="Next Question",
            font=self.normal_font,
            command=self.new_question,
            width=12,
            state=tk.DISABLED
        )
        self.next_button.grid(row=0, column=1, padx=10, pady=5)

        # ---------- Feedback & Hint ----------
        self.feedback_label = tk.Label(
            master,
            text="",
            font=self.normal_font,
            bg="#f0f8ff"
        )
        self.feedback_label.pack(pady=5)

        # Hint is always visible (no button)
        self.hint_label = tk.Label(
            master,
            text="",
            font=self.normal_font,
            fg="#444444",
            bg="#f0f8ff"
        )
        self.hint_label.pack(pady=5)

        # ---------- Info for kids ----------
        self.info_label = tk.Label(
            master,
            text="Tip: Think about multiplication!\n"
                 "Example: 9 ÷ 3 = ?  →  What times 3 equals 9?",
            font=self.small_font,
            bg="#f0f8ff"
        )
        self.info_label.pack(pady=(10, 15))

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

        # Clear entry and feedback
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        self.feedback_label.config(text="", fg="black")

        # Always show hint for this question
        self.hint_label.config(
            text=f"Hint: What times {self.current_divisor} equals {self.current_dividend}?"
        )

        # Lock Next Question until they give a CORRECT answer
        self.next_button.config(state=tk.DISABLED)

        self.update_score_label()

    def update_score_label(self):
        # Score out of the number of questions the child has attempted
        self.score_label.config(
            text=f"Score: {self.score} / {self.questions_answered}"
        )

    def check_answer(self):
        user_input = self.answer_entry.get().strip()

        if not user_input:
            self.feedback_label.config(
                text="Please type an answer first.",
                fg="red"
            )
            self.next_button.config(state=tk.DISABLED)
            return

        if not user_input.isdigit():
            self.feedback_label.config(
                text="Please enter a whole number.",
                fg="red"
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
                self.answered_correctly_this_question = True

            self.feedback_label.config(
                text=f"✅ Correct! {self.current_answer} × {self.current_divisor} = {self.current_dividend}",
                fg="green"
            )
            # NOW allow moving to the next question
            self.next_button.config(state=tk.NORMAL)
        else:
            self.feedback_label.config(
                text="❌ Not quite. Try again!",
                fg="red"
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
