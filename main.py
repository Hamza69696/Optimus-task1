import tkinter as tk
from tkinter import ttk
import re


class PasswordStrengthAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        self.common_passwords = self.load_common_passwords()

        self.title_label = tk.Label(
            root,
            text="Password Strength Analyzer",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=20)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        self.password_label = tk.Label(
            self.input_frame,
            text="Enter Password:",
            font=("Arial", 12)
        )
        self.password_label.grid(row=0, column=0, padx=10)

        self.password_entry = tk.Entry(
            self.input_frame,
            width=40,
            show="*",
            font=("Arial", 12)
        )
        self.password_entry.grid(row=0, column=1, padx=10)

        self.check_button = tk.Button(
            self.input_frame,
            text="Analyze Password",
            command=self.analyze_password,
            width=18,
            font=("Arial", 11)
        )
        self.check_button.grid(row=0, column=2, padx=10)

        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=15)

        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=450,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.score_label = tk.Label(
            root,
            text="",
            font=("Arial", 12)
        )
        self.score_label.pack()

        self.feedback_title = tk.Label(
            root,
            text="Suggestions",
            font=("Arial", 14, "bold")
        )
        self.feedback_title.pack(pady=10)

        self.feedback_box = tk.Text(
            root,
            width=80,
            height=12,
            font=("Arial", 11)
        )
        self.feedback_box.pack(pady=10)

    def load_common_passwords(self):
        try:
            with open("common_passwords.txt", "r", encoding="utf-8") as file:
                return {line.strip().lower() for line in file}
        except FileNotFoundError:
            return set()

    def analyze_password(self):
        password = self.password_entry.get()

        score = 0
        feedback = []

        if not password:
            self.result_label.config(
                text="Please Enter a Password",
                fg="red"
            )
            self.progress["value"] = 0
            return

        if len(password) >= 8:
            score += 20
        else:
            feedback.append(
                "Use at least 8 characters."
            )

        if len(password) >= 12:
            score += 10

        if re.search(r"[A-Z]", password):
            score += 20
        else:
            feedback.append(
                "Add uppercase letters."
            )

        if re.search(r"[a-z]", password):
            score += 20
        else:
            feedback.append(
                "Add lowercase letters."
            )

        if re.search(r"\d", password):
            score += 15
        else:
            feedback.append(
                "Add numbers."
            )

        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
            score += 15
        else:
            feedback.append(
                "Add special characters."
            )

        if password.lower() in self.common_passwords:
            score -= 40
            feedback.append(
                "This password is commonly used. Choose a unique password."
            )

        score = max(score, 0)

        self.progress["value"] = score
        self.score_label.config(text=f"Strength Score: {score}/100")

        if score < 40:
            self.result_label.config(
                text="Weak Password",
                fg="red"
            )
        elif score < 70:
            self.result_label.config(
                text="Medium Password",
                fg="orange"
            )
        elif score < 90:
            self.result_label.config(
                text="Strong Password",
                fg="green"
            )
        else:
            self.result_label.config(
                text="Very Strong Password",
                fg="darkgreen"
            )

        self.feedback_box.delete("1.0", tk.END)

        if feedback:
            for item in feedback:
                self.feedback_box.insert(
                    tk.END,
                    f"• {item}\n"
                )
        else:
            self.feedback_box.insert(
                tk.END,
                "Excellent password. No improvements required."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthAnalyzer(root)
    root.mainloop()