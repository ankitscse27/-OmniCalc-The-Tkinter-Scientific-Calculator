# Author: Ankit Singh (ankitscse27)

import tkinter as tk
import math
import re

# --- Constants for Styling ---
# A modern dark theme with cyan and blue-gray accents.
class Style:
    BG_COLOR = "#1A2226"             # Dark Slate Blue/Gray
    DISPLAY_BG_COLOR = "#232D33"     # Slightly Lighter Slate
    BUTTON_BG_COLOR = "#4A5A63"      # Blue-Gray
    OPERATOR_BG_COLOR = "#26C6DA"    # Bright Cyan
    FUNCTION_BG_COLOR = "#37474F"    # Darker Blue-Gray
    SPECIAL_BG_COLOR = "#546E7A"     # Muted Blue-Gray
    SECOND_ACTIVE_BG = "#607D8B"     # Highlighted Gray
    WHITE = "#FFFFFF"
    LABEL_COLOR = "#F0F0F0"          # Soft White
    
    # Hover colors for visual feedback
    OPERATOR_HOVER_COLOR = "#80D8FF" # Light Cyan
    BUTTON_HOVER_COLOR = "#607D8B"   # Lighter Blue-Gray
    FUNCTION_HOVER_COLOR = "#546E7A" # Lighter Function Gray
    SPECIAL_HOVER_COLOR = "#78909C"  # Lighter Special Gray

    # Font styles
    LARGE_FONT = ("Arial", 36, "bold")
    SMALL_FONT = ("Arial", 14)
    BUTTON_FONT = ("Arial", 16, "bold")
    MODE_FONT = ("Arial", 12, "bold")
    AUTHOR_FONT = ("Arial", 9, "italic")

class ScientificCalculator:
    """
    An advanced scientific calculator with a modern GUI using Tkinter.
    
    Features:
    - Standard arithmetic operations (+, -, ×, ÷)
    - Power (xʸ), square (x²), cube (x³), square root (√x)
    - Trigonometric functions (sin, cos, tan) with DEG/RAD modes
    - A '2nd' key for inverse (sin⁻¹, cos⁻¹, tan⁻¹) and hyperbolic functions
    - Logarithms (log₁₀, ln), factorial (x!), and memory functions
    - Constants (π, e), and an ANS key to recall the last result
    - A safe evaluation method to prevent malicious code execution
    - An intuitive display with user-friendly symbols and auto-clearing of errors
    - Responsive UI with keyboard bindings
    """

    def __init__(self, master):
        """Initialize the calculator."""
        self.master = master
        master.title("Engineering Scientific Calculator")
        master.geometry("400x700")
        master.configure(bg=Style.BG_COLOR)
        master.minsize(400, 700)

        # --- State Variables ---
        self.expression = ""
        self.is_deg_mode = True
        self.is_second_mode = False
        self.memory = 0
        self.last_answer = 0
        self.toggleable_buttons = []

        # --- Safe Evaluation & Display Dictionaries ---
        self.safe_dict = self._create_safe_dict()
        self.DISPLAY_MAP = {'**': '^', '*': '×', '/': '÷', 'sqrt(': '√('}
        
        # --- UI Setup ---
        self.display_frame = self._create_display_frame()
        self.buttons_frame = self._create_buttons_frame()
        self.total_label, self.label, self.mode_label = self._create_display_labels()
        self._create_author_label()
        self._configure_grid_weights()
        self.button_definitions = self._get_button_definitions()
        self._create_buttons()
        self._bind_keys()

    def _create_safe_dict(self):
        """Creates the dictionary of allowed functions for safe evaluation."""
        return {
            'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt, 'cbrt': lambda x: x**(1/3),
            'log': math.log, 'log10': math.log10, 'exp': math.exp, 'abs': abs,
            'factorial': math.factorial, 'pow': pow, 'sin': math.sin, 'cos': math.cos,
            'tan': math.tan, 'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sind': lambda x: math.sin(math.radians(x)),
            'cosd': lambda x: math.cos(math.radians(x)),
            'tand': lambda x: math.tan(math.radians(x)),
            'asind': lambda x: math.degrees(math.asin(x)),
            'acosd': lambda x: math.degrees(math.acos(x)),
            'atand': lambda x: math.degrees(math.atan(x)),
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh, 'asinh': math.asinh,
            'acosh': math.acosh, 'atanh': math.atanh,
        }

    def _configure_grid_weights(self):
        """Configure the root window's grid to be responsive."""
        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=5)
        self.master.columnconfigure(0, weight=1)

    def _create_display_frame(self):
        """Create the frame for the calculator display."""
        frame = tk.Frame(self.master, bg=Style.DISPLAY_BG_COLOR, bd=5, relief=tk.RIDGE)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        return frame

    def _create_buttons_frame(self):
        """Create the frame for the calculator buttons."""
        frame = tk.Frame(self.master, bg=Style.BG_COLOR)
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(9):
            frame.rowconfigure(i, weight=1)
        for i in range(5):
            frame.columnconfigure(i, weight=1)
        return frame

    def _create_display_labels(self):
        """Create the labels for showing the expression and result."""
        total_label = tk.Label(self.display_frame, text="", anchor=tk.E,
                               bg=Style.DISPLAY_BG_COLOR, fg=Style.LABEL_COLOR, 
                               padx=10, font=Style.SMALL_FONT)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text="0", anchor=tk.E,
                         bg=Style.DISPLAY_BG_COLOR, fg=Style.WHITE, 
                         padx=10, font=Style.LARGE_FONT)
        label.pack(expand=True, fill='both')

        mode_label = tk.Label(self.display_frame, text="DEG", anchor=tk.W,
                              bg=Style.DISPLAY_BG_COLOR, fg=Style.OPERATOR_BG_COLOR, 
                              padx=10, font=Style.MODE_FONT)
        mode_label.pack(expand=True, fill='x', side='left')
        return total_label, label, mode_label
        
    def _create_author_label(self):
        """Create the author credit label in the display."""
        author_label = tk.Label(self.display_frame, text="Ankit Singh (ankitscse27)", anchor=tk.E,
                                bg=Style.DISPLAY_BG_COLOR, fg=Style.FUNCTION_BG_COLOR, 
                                padx=10, font=Style.AUTHOR_FONT)
        author_label.pack(expand=True, fill='x', side='right')

    def _get_button_definitions(self):
        """Returns a list of dictionaries defining all buttons."""
        return [
            {'text': '2nd', 'command': self.toggle_second_mode, 'type': 'func', 'row': 0, 'col': 0, 'id': '2nd'},
            {'text': 'DEG', 'command': self.toggle_deg_rad, 'type': 'func', 'row': 0, 'col': 1, 'id': 'deg'},
            {'text': '(', 'command': '(', 'type': 'func', 'row': 0, 'col': 2},
            {'text': ')', 'command': ')', 'type': 'func', 'row': 0, 'col': 3},
            {'text': '%', 'command': '/100', 'type': 'func', 'row': 0, 'col': 4},
            {'p_text': 'x²', 'p_cmd': '**2', 's_text': 'x³', 's_cmd': '**3', 'type': 'func', 'row': 1, 'col': 0, 'toggle': True},
            {'text': 'xʸ', 'command': '**', 'type': 'func', 'row': 1, 'col': 1},
            {'p_text': '√x', 'p_cmd': 'sqrt(', 's_text': '³√x', 's_cmd': 'cbrt(', 'type': 'func', 'row': 1, 'col': 2, 'toggle': True},
            {'text': 'x!', 'command': 'factorial(', 'type': 'func', 'row': 1, 'col': 3},
            {'text': 'eˣ', 'command': 'exp(', 'type': 'func', 'row': 1, 'col': 4},
            {'p_text': 'sin', 'p_cmd': 'sin(', 's_text': 'sin⁻¹', 's_cmd': 'asin(', 'type': 'func', 'row': 2, 'col': 0, 'toggle': True},
            {'p_text': 'cos', 'p_cmd': 'cos(', 's_text': 'cos⁻¹', 's_cmd': 'acos(', 'type': 'func', 'row': 2, 'col': 1, 'toggle': True},
            {'p_text': 'tan', 'p_cmd': 'tan(', 's_text': 'tan⁻¹', 's_cmd': 'atan(', 'type': 'func', 'row': 2, 'col': 2, 'toggle': True},
            {'text': 'log₁₀', 'command': 'log10(', 'type': 'func', 'row': 2, 'col': 3},
            {'text': 'ln', 'command': 'log(', 'type': 'func', 'row': 2, 'col': 4},
            {'p_text': 'sinh', 'p_cmd': 'sinh(', 's_text': 'sinh⁻¹', 's_cmd': 'asinh(', 'type': 'func', 'row': 3, 'col': 0, 'toggle': True},
            {'p_text': 'cosh', 'p_cmd': 'cosh(', 's_text': 'cosh⁻¹', 's_cmd': 'acosh(', 'type': 'func', 'row': 3, 'col': 1, 'toggle': True},
            {'p_text': 'tanh', 'p_cmd': 'tanh(', 's_text': 'tanh⁻¹', 's_cmd': 'atanh(', 'type': 'func', 'row': 3, 'col': 2, 'toggle': True},
            {'text': 'MC', 'command': self.memory_clear, 'type': 'func', 'row': 3, 'col': 3},
            {'text': 'MR', 'command': self.memory_recall, 'type': 'func', 'row': 3, 'col': 4},
            {'text': '7', 'command': '7', 'type': 'num', 'row': 4, 'col': 0},
            {'text': '8', 'command': '8', 'type': 'num', 'row': 4, 'col': 1},
            {'text': '9', 'command': '9', 'type': 'num', 'row': 4, 'col': 2},
            {'text': 'M+', 'command': self.memory_add, 'type': 'func', 'row': 4, 'col': 3},
            {'text': 'M-', 'command': self.memory_subtract, 'type': 'func', 'row': 4, 'col': 4},
            {'text': '4', 'command': '4', 'type': 'num', 'row': 5, 'col': 0},
            {'text': '5', 'command': '5', 'type': 'num', 'row': 5, 'col': 1},
            {'text': '6', 'command': '6', 'type': 'num', 'row': 5, 'col': 2},
            {'text': 'DEL', 'command': self.backspace, 'type': 'spec', 'row': 5, 'col': 3},
            {'text': 'C', 'command': self.clear, 'type': 'spec', 'row': 5, 'col': 4},
            {'text': '1', 'command': '1', 'type': 'num', 'row': 6, 'col': 0},
            {'text': '2', 'command': '2', 'type': 'num', 'row': 6, 'col': 1},
            {'text': '3', 'command': '3', 'type': 'num', 'row': 6, 'col': 2},
            {'text': '×', 'command': '*', 'type': 'op', 'row': 6, 'col': 3},
            {'text': '÷', 'command': '/', 'type': 'op', 'row': 6, 'col': 4},
            {'text': '0', 'command': '0', 'type': 'num', 'row': 7, 'col': 0, 'colspan': 2},
            {'text': '.', 'command': '.', 'type': 'num', 'row': 7, 'col': 2},
            {'text': '+', 'command': '+', 'type': 'op', 'row': 7, 'col': 3},
            {'text': '-', 'command': '-', 'type': 'op', 'row': 7, 'col': 4},
            {'text': 'e', 'command': 'e', 'type': 'num', 'row': 8, 'col': 0},
            {'text': 'π', 'command': 'pi', 'type': 'num', 'row': 8, 'col': 1},
            {'text': 'ANS', 'command': self.recall_last_answer, 'type': 'func', 'row': 8, 'col': 2},
            {'text': '=', 'command': self.evaluate, 'type': 'op', 'row': 8, 'col': 3, 'colspan': 2},
        ]

    def _create_buttons(self):
        """Create and place all calculator buttons based on the defined layout."""
        for b_info in self.button_definitions:
            self._add_button(b_info)

    def _add_button(self, b_info):
        """Helper method to create and configure a single button."""
        bg_color, hover_color = self._get_button_colors(b_info['type'])
        
        is_toggleable = b_info.get('toggle', False)
        text = b_info.get('p_text', b_info.get('text', ''))
        cmd = b_info.get('p_cmd', b_info.get('command', ''))
        
        action = cmd if callable(cmd) else lambda x=cmd: self.add_to_expression(x)

        button = tk.Button(self.buttons_frame, text=text, bg=bg_color, fg=Style.WHITE,
                           font=Style.BUTTON_FONT, borderwidth=0, command=action)
        
        button.grid(row=b_info['row'], column=b_info['col'], 
                    columnspan=b_info.get('colspan', 1),
                    sticky="nsew", padx=2, pady=2)
        
        def on_enter(event, h_color=hover_color):
            if event.widget['bg'] != Style.SECOND_ACTIVE_BG:
                event.widget.config(bg=h_color)
        
        def on_leave(event, b_color=bg_color):
            if event.widget['bg'] != Style.SECOND_ACTIVE_BG:
                event.widget.config(bg=b_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        if is_toggleable:
            self.toggleable_buttons.append((button, b_info))

        if 'id' in b_info:
            setattr(self, f"btn_{b_info['id']}", button)


    def _get_button_colors(self, btn_type):
        """Returns the background and hover color based on button type."""
        if btn_type == 'op': return Style.OPERATOR_BG_COLOR, Style.OPERATOR_HOVER_COLOR
        if btn_type == 'num': return Style.BUTTON_BG_COLOR, Style.BUTTON_HOVER_COLOR
        if btn_type == 'func': return Style.FUNCTION_BG_COLOR, Style.FUNCTION_HOVER_COLOR
        if btn_type == 'spec': return Style.SPECIAL_BG_COLOR, Style.SPECIAL_HOVER_COLOR
        return Style.BUTTON_BG_COLOR, Style.BUTTON_HOVER_COLOR

    def _bind_keys(self):
        """Bind keyboard keys to calculator functions for usability."""
        self.master.bind("<Return>", lambda event: self.evaluate())
        self.master.bind("<BackSpace>", lambda event: self.backspace())
        self.master.bind("<Escape>", lambda event: self.clear())
        for key in "1234567890.+-/()":
            self.master.bind(key, lambda event, digit=key: self.add_to_expression(digit))
        self.master.bind("*", lambda event: self.add_to_expression('*'))
    
    def add_to_expression(self, value):
        """Append a value to the current expression, clearing errors first."""
        if self.expression == "Error":
            self.expression = ""
        self.expression += str(value)
        self._update_labels()

    def clear(self):
        """Clear the entire expression and reset display."""
        self.expression = ""
        self.total_label.config(text="")
        self._update_labels()

    def backspace(self):
        """Remove the last character or clear an error."""
        if self.expression == "Error":
            self.clear()
        else:
            self.expression = self.expression[:-1]
            self._update_labels()

    def toggle_deg_rad(self):
        """Toggle between Degree and Radian modes."""
        self.is_deg_mode = not self.is_deg_mode
        mode = "DEG" if self.is_deg_mode else "RAD"
        self.btn_deg.config(text=mode)
        self.mode_label.config(text=mode)

    def toggle_second_mode(self):
        """Toggle the second function set for applicable buttons."""
        self.is_second_mode = not self.is_second_mode
        bg = Style.SECOND_ACTIVE_BG if self.is_second_mode else Style.FUNCTION_BG_COLOR
        self.btn_2nd.config(bg=bg)

        for button, b_info in self.toggleable_buttons:
            if self.is_second_mode:
                text, cmd = b_info['s_text'], b_info['s_cmd']
            else:
                text, cmd = b_info['p_text'], b_info['p_cmd']
            
            action = cmd if callable(cmd) else lambda x=cmd: self.add_to_expression(x)
            button.config(text=text, command=action)

    def _preprocess_expression(self, expr):
        """Prepare the expression for safe evaluation."""
        if self.is_deg_mode:
            for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                expr = re.sub(r'\b' + func + r'\(', f'{func}d(', expr)
        return expr

    def evaluate(self):
        """Evaluate the full expression using the restricted 'eval'."""
        display_expr = self._format_for_display(self.expression)
        self.total_label.config(text=display_expr + "=")
        try:
            processed_expr = self._preprocess_expression(self.expression)
            result = eval(processed_expr, {"__builtins__": None}, self.safe_dict)
            self.last_answer = result
            
            if result == int(result):
                result = int(result)
            self.expression = str(round(result, 10))
        except (ZeroDivisionError, SyntaxError, NameError, TypeError, ValueError):
            self.expression = "Error"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.expression = "Error"
        finally:
            self._update_labels()

    def _format_for_display(self, expr):
        """Convert internal expression to a more readable format for display."""
        for op, symbol in self.DISPLAY_MAP.items():
            expr = expr.replace(op, symbol)
        return expr

    def _update_labels(self):
        """Update the display labels with the current expression."""
        display_text = self._format_for_display(self.expression)
        self.label.config(text=display_text if self.expression else "0")
        if self.expression != "Error":
             self.total_label.config(text=display_text)

    # --- Memory and Answer Functions ---
    def memory_clear(self): self.memory = 0
    def memory_recall(self): self.add_to_expression(str(self.memory))
    def recall_last_answer(self): self.add_to_expression(str(self.last_answer))
    def memory_op(self, operation):
        """Generic function to handle M+ and M- operations."""
        try:
            current_val = float(eval(self.expression, {"__builtins__": None}, self.safe_dict))
            self.memory = operation(self.memory, current_val)
        except:
            self.expression = "Error"
            self._update_labels()
    def memory_add(self): self.memory_op(lambda m, v: m + v)
    def memory_subtract(self): self.memory_op(lambda m, v: m - v)

# --- Main Execution ---
if __name__ == "__main__":
    window = tk.Tk()
    calculator = ScientificCalculator(window)
    window.mainloop()