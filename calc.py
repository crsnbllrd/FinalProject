import tkinter as tk
import re

# Initialize values for color and fonts
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

# Initialize the calculator
class Calculator:
    def __init__(self, master):
        # Initialize values
        self.window = master
        self.window.geometry("400x700")
        self.window.resizable(1, 1)
        self.window.title("Calculator - Carson Ballard")
        # Set the expressions to be clear and create frames
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+",}
        self.buttons_frame = self.create_buttons_frame()
        # Create buttons
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    # Keep track of user keystrokes and input them to the calculator
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<Escape>", lambda event: self.clear())
        self.window.bind("<Delete>", lambda event: self.clear())
        self.window.bind("<^>", lambda event: self.add_exponent())
        self.window.bind("<%>", lambda event: self.modulo())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        self.window.bind("<(>", lambda event: self.add_open_parentheses())
        self.window.bind("<)>", lambda event: self.add_closed_parentheses())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
    # Define a function to create buttons
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_last_answer_button()
        self.create_exponent_button()
        self.create_modulo_button()
        self.create_parentheses_buttons()
    # Define a function to create labels
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label
    # Define a function to create display frame
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY, borderwidth= 1, relief= "solid")
        frame.pack(expand=True, fill="both")
        return frame
    # Add current input to the expression
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    # Create digit buttons
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=1, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
        # Define a function to add an operator to the expression
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
    # Define a function to create operation buttons
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=1, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1
    # Define a function to backspace
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()
        # Define a function to clear the calculator
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        # Create the clear button
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)
        # Add functionality for exponents
    def add_exponent(self):
        self.current_expression = self.current_expression + "**"
        self.update_label()
        # Add functionality for square roots
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()
        # Add square root button
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)
        # Square root function
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()
        # Add button for modulo
    def create_modulo_button(self):
        button = tk.Button(self.buttons_frame, text="mod", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.modulo)
        button.grid(row=5, column=2, sticky=tk.NSEW)
        # Modulo function
    def modulo(self):
        self.current_expression += "%"
        self.update_label()
        # Create sqrt button
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)
        # Evaluate the current expression and print result
    def evaluate(self):
        self.total_expression += self.current_expression
        self.total_expression = re.sub(r'(\d+)\(', r'\g<1>*(', self.total_expression)
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.last_answer = self.current_expression
            self.update_label()
        # Creare buttons for parentheses
    def create_parentheses_buttons(self):
        open_button = tk.Button(self.buttons_frame, text="(", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=1, command=self.add_open_parentheses)
        closed_button = tk.Button(self.buttons_frame, text=")", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=1, command=self.add_closed_parentheses)
        open_button.grid(row=6, column=1, sticky=tk.NSEW)
        closed_button.grid(row=6, column=2, sticky=tk.NSEW)
    
    def add_open_parentheses(self):
        self.current_expression += "("
        self.update_label()
    
    def add_closed_parentheses(self):
        self.current_expression += ")"
        self.update_label()
    # Create exponent button
    def create_exponent_button(self):
        button = tk.Button(self.buttons_frame, text="^", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.add_exponent)
        button.grid(row=5, column=1, sticky=tk.NSEW)
        # Create equals button
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
        # Create frame for the buttons
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
        # Update the label showing the expression
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])
        # Create function for last answer
    def last_answer(self):
        self.current_expression = self.last_answer
        self.update_label()
    # Create button for last answer
    def create_last_answer_button(self):
        button = tk.Button(self.buttons_frame, text="Ans", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=1, command=self.last_answer)
        button.grid(row=5, column=3, columnspan=2, rowspan=2, sticky=tk.NSEW)
    # Run the calculator
    def run(self):
        self.window.mainloop()
    
if __name__ == "__main__":
    calc = Calculator()
    calc.run()