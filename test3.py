import tkinter as tk
from tkinter import ttk
import pint
from PIL import Image, ImageTk



class Converter:
    """ICONS = {
        "meter": "length.png",
        "centimeter": "length.png",
        "kilometer": "length.png",
        "celsius": "temperature.png",
        "fahrenheit": "temperature.png",
        "grams": "eright.png",
        "kilograms": "weight.png",
        "mile": "length.png",
        "yard": "length.png",
        "ounce": "weight.png",
        "pound": "weight.png",
    } """

    def __init__(self, master):
        self.master = master
        master.geometry("600x300")
        master.title("Converter - Carson Ballard")

        left_frame = tk.Frame(master, height=1, width=1, bg="black")
        left_frame.pack(side=tk.LEFT, expand=True, fill="both")
        
        
        self.units = [
            "meter",
            "centimeter",
            "kilometer",
            "celsius",
            "fahrenheit",
            "grams",
            "kilograms",
            "mile",
            "yard",
            "ounce",
            "pound",
        ]
        
    
        
        input_label = tk.Label(left_frame, text="Enter units to convert: ")
        input_label.pack(side=tk.TOP)

        self.input_field_left = tk.Text(left_frame, height=3, width=30)
        self.input_field_left.pack(side=tk.TOP)

        self.left_clicked = tk.StringVar()
        self.left_clicked.set(self.units[0])

        self.right_clicked = tk.StringVar()
        self.right_clicked.set(self.units[0])

        self.ureg = pint.UnitRegistry()

        self.ureg.define("meter = [length]")
        self.ureg.define("centimeter = 0.01 * meter")
        self.ureg.define("kilometer = 1000 * meter")
        self.ureg.define("celsius = [temperature]")
        self.ureg.define("fahrenheit = [temperature]")
        self.ureg.define("gram = [mass]")
        self.ureg.define("kilogram = 1000 * gram")
        self.ureg.define("mile = 1609.34 * meter")
        self.ureg.define("yard = 0.9144 * meter")
        self.ureg.define("ounce = 28.3495 * gram")
        self.ureg.define("pound = 16 * ounce")

        output_text = tk.Label(master, height=3, width=30, text="output")
        output_text.pack(side=tk.TOP, expand=True, fill="both")
        self.output_text = output_text

        convert_button = tk.Button(master, text="Convert", height=3, width=10, command=self.convert)
        convert_button.pack(side=tk.BOTTOM, expand=True, fill="x")

        clear_button = tk.Button(master, text="Clear", height=3, width=10, command=self.clear)
        clear_button.pack(side=tk.BOTTOM, expand=True, fill="x")

        dropdown_left = tk.OptionMenu(left_frame, self.left_clicked, *self.units)
        dropdown_left.pack(side=tk.TOP)

        dropdown_right = tk.OptionMenu(master, self.right_clicked, *self.units)
        dropdown_right.pack(side=tk.BOTTOM)

    def convert(self):
        input_value = self.input_field_left.get("1.0", "end-1c")

        try:
            value = float(input_value)
        except ValueError:
            self.output_text.config(text="Invalid input: " + input_value)
            return

        try:
            result = value * self.ureg(self.left_clicked.get()).to(self.right_clicked.get())
        except pint.errors.UndefinedUnitError:
            self.output_text.config(
                text="Invalid units: " + self.left_clicked.get() + " or " + self.right_clicked.get()
            )
            return

        self.output_text.config(text=result.magnitude)

    def clear(self):
        self.input_field_left.delete("1.0", tk.END)
        self.output_text.config(text="output")        
        
if __name__ == "__main__":
    conv = Convertor()
    conv.run()