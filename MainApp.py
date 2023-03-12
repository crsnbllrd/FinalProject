import os
import tkinter as tk
from PIL import ImageTk, Image
from calc import Calculator
from test3 import Converter

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Application")
        
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load images of calculator and converter from the current directory
        calculator_image = Image.open(os.path.join(current_dir, "calculator.png"))
        calculator_image = calculator_image.resize((50, 50), Image.ANTIALIAS)
        self.calculator_icon = ImageTk.PhotoImage(calculator_image)
        
        converter_image = Image.open(os.path.join(current_dir, "converter.png"))
        converter_image = converter_image.resize((50, 50), Image.ANTIALIAS)
        self.converter_icon = ImageTk.PhotoImage(converter_image)
        
        # Create buttons to open calculator and converter classes
        self.calculator_button = tk.Button(self.master, text="Calculator", image=self.calculator_icon, compound=tk.LEFT, command=self.open_calculator)
        self.calculator_button.pack(side=tk.TOP, padx=10, pady=10)
        
        self.converter_button = tk.Button(self.master, text="Converter", image=self.converter_icon, compound=tk.LEFT, command=self.open_converter)
        self.converter_button.pack(side=tk.TOP, padx=10, pady=10)
    
    def open_calculator(self):
        # Create a new calculator window
        calculator_window = tk.Toplevel(self.master)
        calculator_app = Calculator(calculator_window)
    
    def open_converter(self):
        # Create a new converter window
        converter_window = tk.Toplevel(self.master)
        converter_app = Converter(converter_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
