import ast
import operator
import tkinter as tk
from tkinter import messagebox


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculate(expression):
    """Evaluate an arithmetic expression containing only supported operators."""
    expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Ekspresi tidak valid")

    return evaluate(tree)


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Sederhana")
        self.root.resizable(False, False)
        self.expression = tk.StringVar(value="0")
        self.just_calculated = False

        display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            readonlybackground="white",
            width=16,
            bd=8,
        )
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            ("AC", 1, 0, self.clear),
            ("⌫", 1, 1, self.backspace),
            ("(", 1, 2, lambda: self.press("(")),
            (")", 1, 3, lambda: self.press(")")),
            ("7", 2, 0, lambda: self.press("7")),
            ("8", 2, 1, lambda: self.press("8")),
            ("9", 2, 2, lambda: self.press("9")),
            ("÷", 2, 3, lambda: self.press("÷")),
            ("4", 3, 0, lambda: self.press("4")),
            ("5", 3, 1, lambda: self.press("5")),
            ("6", 3, 2, lambda: self.press("6")),
            ("×", 3, 3, lambda: self.press("×")),
            ("1", 4, 0, lambda: self.press("1")),
            ("2", 4, 1, lambda: self.press("2")),
            ("3", 4, 2, lambda: self.press("3")),
            ("−", 4, 3, lambda: self.press("−")),
            ("0", 5, 0, lambda: self.press("0")),
            (".", 5, 1, lambda: self.press(".")),
            ("=", 5, 2, self.result),
            ("+", 5, 3, lambda: self.press("+")),
        ]

        for label, row, column, command in buttons:
            tk.Button(
                root,
                text=label,
                font=("Arial", 18),
                width=4,
                height=2,
                command=command,
            ).grid(row=row, column=column, padx=4, pady=4, sticky="nsew")

    def press(self, value):
        current = self.expression.get()
        if current == "Error" or self.just_calculated:
            current = "0" if value in "+−×÷" else ""
            self.just_calculated = False

        if value == "(" and current == "0":
            current = ""
        elif value.isdigit() or value == ".":
            if current == "0":
                current = ""
        self.expression.set(current + value)

    def clear(self):
        self.expression.set("0")
        self.just_calculated = False

    def backspace(self):
        current = self.expression.get()
        if current == "Error" or self.just_calculated:
            self.clear()
            return
        self.expression.set(current[:-1] or "0")

    def result(self):
        try:
            value = calculate(self.expression.get())
            self.expression.set(f"{value:.12g}" if isinstance(value, float) else str(value))
            self.just_calculated = True
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            self.expression.set("Error")
            self.just_calculated = True


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
