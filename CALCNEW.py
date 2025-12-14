import tkinter as tk
import math
import re
import operator
# from PIL import Image, ImageTk # REMOVED: No longer needed as logo/image functionality is removed

# --- 1. Model: Core Logic and State Management (Unchanged) ---

class CalculatorCore:
    """Handles all mathematical state, evaluation, and mode processing."""
    
    def __init__(self):
        self.expression = ""
        self.total_history = ""
        self.is_deg_mode = True
        self.is_second_mode = False
        self.memory = 0.0
        self.last_answer = 0.0
        self.safe_dict = self._create_safe_dict()
        
        self.DISPLAY_MAP = {'**': '^', '*': '×', '/': '÷', 'sqrt(': '√(', 'cbrt(': '³√('}
        self.DISPLAY_FUNCTIONS = ['sin(', 'cos(', 'tan(', 'log10(', 'log(', 'exp(', 'factorial(', 'sqrt(', 'cbrt(', 'pow(', 'asin(', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']

    def _create_safe_dict(self):
        """Creates the dictionary of allowed functions for safe evaluation."""
        safe_dict = {
            'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt, 
            'cbrt': lambda x: x**(1/3),
            'log': math.log, 'log10': math.log10, 'exp': math.exp, 'abs': abs,
            'factorial': math.factorial, 'pow': pow, 
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh, 
            'asinh': math.asinh, 'acosh': math.acosh, 'atanh': math.atanh,
        }

        for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
            safe_dict[func] = getattr(math, func)
        
        safe_dict.update({
            'sind': lambda x: math.sin(math.radians(x)),
            'cosd': lambda x: math.cos(math.radians(x)),
            'tand': lambda x: math.tan(math.radians(x)),
            'asind': lambda x: math.degrees(math.asin(x)),
            'acosd': lambda x: math.degrees(math.acos(x)),
            'atand': lambda x: math.degrees(math.atan(x)),
        })
        return safe_dict

    def add_to_expression(self, value):
        if self.expression == "Error": self.expression = ""
        if value == 'π': value = 'pi'
        elif value == 'e': value = 'e'
        self.expression += str(value)

    def clear(self):
        self.expression = ""
        self.total_history = ""

    def backspace(self):
        if self.expression == "Error": self.clear()
        else: self.expression = self.expression[:-1]

    def toggle_deg_rad(self):
        self.is_deg_mode = not self.is_deg_mode
        return "DEG" if self.is_deg_mode else "RAD"

    def toggle_second_mode(self):
        self.is_second_mode = not self.is_second_mode
        return self.is_second_mode

    def memory_clear(self):
        self.memory = 0.0

    def memory_recall(self):
        self.add_to_expression(str(self.memory))

    def recall_last_answer(self):
        self.add_to_expression(str(self.last_answer))

    def memory_op(self, op_func):
        try:
            current_val = float(eval(self._preprocess_expression(self.expression), {"__builtins__": None}, self.safe_dict))
            self.memory = op_func(self.memory, current_val)
        except:
            self.expression = "Error"
            
    def memory_add(self): 
        self.memory_op(operator.add)
        self.clear() 
        
    def memory_subtract(self): 
        self.memory_op(operator.sub)
        self.clear() 

    def _preprocess_expression(self, expr):
        open_count = expr.count('(')
        close_count = expr.count(')')
        expr += ')' * (open_count - close_count)

        if self.is_deg_mode:
            for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                expr = re.sub(r'\b' + func + r'\(', f'{func}d(', expr)
        
        expr = expr.replace('pi', str(math.pi))
        expr = expr.replace('e', str(math.e))

        return expr

    def evaluate(self):
        self.total_history = self._format_for_display(self.expression) + "="
        
        try:
            processed_expr = self._preprocess_expression(self.expression)
            result = eval(processed_expr, {"__builtins__": None}, self.safe_dict)
            self.last_answer = result
            
            if result == int(result):
                result = int(result)
            
            self.expression = str(round(result, 10))
            
        except Exception:
            self.expression = "Error"
        
        return self.expression, self.total_history

    def _format_for_display(self, expr):
        display_expr = expr
        for op, symbol in self.DISPLAY_MAP.items():
            display_expr = display_expr.replace(op, symbol)
        
        if self.is_deg_mode:
            display_expr = display_expr.replace('sind(', 'sin(')
            display_expr = display_expr.replace('cosd(', 'cos(')
            display_expr = display_expr.replace('tand(', 'tan(')
            display_expr = display_expr.replace('asind(', 'sin⁻¹(')
            display_expr = display_expr.replace('acosd(', 'cos⁻¹(')
            display_expr = display_expr.replace('atand(', 'tan⁻¹(')

        return display_expr

# --- 2. View: Tkinter UI and Styling (MODIFIED) ---

class Style:
    """Centralized styling constants for the GUI - GREEN/GOLD THEME."""
    BG_COLOR = "#2C3E50"          # Dark Blue-Gray (Deep Slate)
    DISPLAY_BG_COLOR = "#34495E"  # Slightly Lighter Slate
    BUTTON_BG_COLOR = "#5D6D7E"   # Muted Blue-Gray
    OPERATOR_BG_COLOR = "#F4D03F" # Bright Gold/Yellow
    FUNCTION_BG_COLOR = "#27AE60" # Emerald Green
    SPECIAL_BG_COLOR = "#7D92A0"  # Soft Gray
    SECOND_ACTIVE_BG = "#16A085"  # Dark Teal
    WHITE = "#FFFFFF"
    LABEL_COLOR = "#ECF0F1"       # Light Gray (for history/small text)
    
    OPERATOR_HOVER_COLOR = "#F7DC6F" # Lighter Gold
    BUTTON_HOVER_COLOR = "#7E8C9A"   # Lighter Muted Gray
    FUNCTION_HOVER_COLOR = "#2ECC71" # Lighter Green
    SPECIAL_HOVER_COLOR = "#95A5A6"  # Lighter Soft Gray

    LARGE_FONT = ("Arial", 36, "bold")
    SMALL_FONT = ("Arial", 14)
    BUTTON_FONT = ("Arial", 16, "bold")
    MODE_FONT = ("Arial", 12, "bold")
    AUTHOR_FONT = ("Arial", 9, "italic")

class ScientificCalculator(tk.Frame):
    """The Tkinter GUI class (View)."""

    def __init__(self, master, core):
        tk.Frame.__init__(self, master)
        self.master = master
        self.core = core 
        self.toggleable_buttons = []
        # self.github_logo = None # REMOVED: Logo variable no longer needed

        master.title("OmniCalc: Scientific Calculator (Green/Gold)")
        master.geometry("400x700")
        master.configure(bg=Style.BG_COLOR)
        master.minsize(400, 700)

        self._configure_grid_weights()
        
        # UI Component Creation
        self.display_frame = self._create_display_frame()
        self.buttons_frame = self._create_buttons_frame()
        self.total_label, self.label, self.mode_label = self._create_display_labels()
        # self._create_author_label() # REMOVED: Logo/Author label creation no longer needed
        
        # Button Creation
        self.button_definitions = self._get_button_definitions()
        self._create_buttons()
        self.update_display() 
        self._bind_keys()

    # --- UI Creation Helper Methods (Restored/Modified) ---

    def _configure_grid_weights(self):
        """Configure the root window's grid to be responsive."""
        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=5)
        self.master.columnconfigure(0, weight=1)

    def _create_display_frame(self):
        frame = tk.Frame(self.master, bg=Style.DISPLAY_BG_COLOR, bd=5, relief=tk.RIDGE)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        return frame

    def _create_buttons_frame(self):
        frame = tk.Frame(self.master, bg=Style.BG_COLOR)
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(9):
            frame.rowconfigure(i, weight=1)
        for i in range(5):
            frame.columnconfigure(i, weight=1)
        return frame

    def _create_display_labels(self):
        """Create the labels for showing the expression and result."""
        
        # 1. Total/History Label
        total_label = tk.Label(self.display_frame, text="", anchor=tk.E,
                               bg=Style.DISPLAY_BG_COLOR, fg=Style.LABEL_COLOR, 
                               padx=10, font=Style.SMALL_FONT)
        total_label.pack(expand=True, fill='x')
        
        # 2. Main Expression/Result Label
        label = tk.Label(self.display_frame, text="0", anchor=tk.E,
                         bg=Style.DISPLAY_BG_COLOR, fg=Style.WHITE, 
                         padx=10, font=Style.LARGE_FONT)
        label.pack(expand=True, fill='both')

        # 3. Mode/Status Frame (Bottom of display)
        status_frame = tk.Frame(self.display_frame, bg=Style.DISPLAY_BG_COLOR)
        status_frame.pack(expand=True, fill='x')

        mode_label = tk.Label(status_frame, text="DEG", anchor=tk.W,
                              bg=Style.DISPLAY_BG_COLOR, fg=Style.OPERATOR_BG_COLOR, 
                              padx=10, font=Style.MODE_FONT)
        mode_label.pack(side='left', padx=(0, 10))
        
        return total_label, label, mode_label
        
    # def _create_author_label(self): # REMOVED: This method is entirely gone
    #     """The logic for the GitHub logo and author label is removed."""
    #     pass
            
    # --- Button Definitions and Creation (Unchanged) ---

    def _get_button_definitions(self):
        """Returns a list of dictionaries defining all buttons."""
        return [
            # Buttons with direct method calls
            {'text': '2nd', 'command': self._toggle_2nd_mode_ui, 'type': 'func', 'row': 0, 'col': 0, 'id': '2nd'},
            {'text': 'DEG', 'command': self._toggle_deg_rad_ui, 'type': 'func', 'row': 0, 'col': 1, 'id': 'deg'},
            {'text': 'MC', 'command': self._mem_clear_ui, 'type': 'func', 'row': 3, 'col': 3},
            {'text': 'MR', 'command': self._mem_recall_ui, 'type': 'func', 'row': 3, 'col': 4},
            {'text': 'M+', 'command': self._mem_add_ui, 'type': 'func', 'row': 4, 'col': 3},
            {'text': 'M-', 'command': self._mem_sub_ui, 'type': 'func', 'row': 4, 'col': 4},
            {'text': 'DEL', 'command': self._backspace_ui, 'type': 'spec', 'row': 5, 'col': 3},
            {'text': 'C', 'command': self._clear_ui, 'type': 'spec', 'row': 5, 'col': 4},
            {'text': 'ANS', 'command': self._recall_ans_ui, 'type': 'func', 'row': 8, 'col': 2},
            {'text': '=', 'command': self._evaluate_ui, 'type': 'op', 'row': 8, 'col': 3, 'colspan': 2},
            
            # Buttons with simple string inputs
            {'text': '(', 'command_str': '(', 'type': 'func', 'row': 0, 'col': 2},
            {'text': ')', 'command_str': ')', 'type': 'func', 'row': 0, 'col': 3},
            {'text': '%', 'command_str': '/100', 'type': 'func', 'row': 0, 'col': 4},
            {'text': 'xʸ', 'command_str': '**', 'type': 'func', 'row': 1, 'col': 1},
            {'text': 'x!', 'command_str': 'factorial(', 'type': 'func', 'row': 1, 'col': 3},
            {'text': 'eˣ', 'command_str': 'exp(', 'type': 'func', 'row': 1, 'col': 4},
            {'text': 'log₁₀', 'command_str': 'log10(', 'type': 'func', 'row': 2, 'col': 3},
            {'text': 'ln', 'command_str': 'log(', 'type': 'func', 'row': 2, 'col': 4},
            {'text': '7', 'command_str': '7', 'type': 'num', 'row': 4, 'col': 0},
            {'text': '8', 'command_str': '8', 'type': 'num', 'row': 4, 'col': 1},
            {'text': '9', 'command_str': '9', 'type': 'num', 'row': 4, 'col': 2},
            {'text': '4', 'command_str': '4', 'type': 'num', 'row': 5, 'col': 0},
            {'text': '5', 'command_str': '5', 'type': 'num', 'row': 5, 'col': 1},
            {'text': '6', 'command_str': '6', 'type': 'num', 'row': 5, 'col': 2},
            {'text': '1', 'command_str': '1', 'type': 'num', 'row': 6, 'col': 0},
            {'text': '2', 'command_str': '2', 'type': 'num', 'row': 6, 'col': 1},
            {'text': '3', 'command_str': '3', 'type': 'num', 'row': 6, 'col': 2},
            {'text': '×', 'command_str': '*', 'type': 'op', 'row': 6, 'col': 3},
            {'text': '÷', 'command_str': '/', 'type': 'op', 'row': 6, 'col': 4},
            {'text': '0', 'command_str': '0', 'type': 'num', 'row': 7, 'col': 0, 'colspan': 2},
            {'text': '.', 'command_str': '.', 'type': 'num', 'row': 7, 'col': 2},
            {'text': '+', 'command_str': '+', 'type': 'op', 'row': 7, 'col': 3},
            {'text': '-', 'command_str': '-', 'type': 'op', 'row': 7, 'col': 4},
            {'text': 'e', 'command_str': 'e', 'type': 'num', 'row': 8, 'col': 0},
            {'text': 'π', 'command_str': 'π', 'type': 'num', 'row': 8, 'col': 1},
            
            # Toggleable buttons
            {'p_text': 'x²', 'p_cmd': '**2', 's_text': 'x³', 's_cmd': '**3', 'type': 'func', 'row': 1, 'col': 0, 'toggle': True},
            {'p_text': '√x', 'p_cmd': 'sqrt(', 's_text': '³√x', 's_cmd': 'cbrt(', 'type': 'func', 'row': 1, 'col': 2, 'toggle': True},
            {'p_text': 'sin', 'p_cmd': 'sin(', 's_text': 'sin⁻¹', 's_cmd': 'asin(', 'type': 'func', 'row': 2, 'col': 0, 'toggle': True},
            {'p_text': 'cos', 'p_cmd': 'cos(', 's_text': 'cos⁻¹', 's_cmd': 'acos(', 'type': 'func', 'row': 2, 'col': 1, 'toggle': True},
            {'p_text': 'tan', 'p_cmd': 'tan(', 's_text': 'tan⁻¹', 's_cmd': 'atan(', 'type': 'func', 'row': 2, 'col': 2, 'toggle': True},
            {'p_text': 'sinh', 'p_cmd': 'sinh(', 's_text': 'sinh⁻¹', 's_cmd': 'asinh(', 'type': 'func', 'row': 3, 'col': 0, 'toggle': True},
            {'p_text': 'cosh', 'p_cmd': 'cosh(', 's_text': 'cosh⁻¹', 's_cmd': 'acosh(', 'type': 'func', 'row': 3, 'col': 1, 'toggle': True},
            {'p_text': 'tanh', 'p_cmd': 'tanh(', 's_text': 'tanh⁻¹', 's_cmd': 'atanh(', 'type': 'func', 'row': 3, 'col': 2, 'toggle': True},
        ]

    def _create_buttons(self):
        for b_info in self.button_definitions:
            self._add_button(b_info)

    def _add_button(self, b_info):
        """Helper method to create and configure a single button."""
        bg_color, hover_color = self._get_button_colors(b_info['type'])
        
        # 1. Determine the command for the button
        if 'command' in b_info:
            action = b_info['command']
            text = b_info['text']
        elif 'command_str' in b_info:
            action = lambda val=b_info['command_str']: self._input(val)
            text = b_info['text']
        elif b_info.get('toggle', False):
            action = lambda val=b_info['p_cmd']: self._input(val)
            text = b_info['p_text']
        else:
            raise ValueError(f"Button definition missing command/command_str/p_cmd: {b_info}")
        
        button = tk.Button(self.buttons_frame, text=text, 
                           bg=bg_color, fg=Style.WHITE,
                           font=Style.BUTTON_FONT, borderwidth=0, command=action)
        
        button.grid(row=b_info['row'], column=b_info['col'], 
                    columnspan=b_info.get('colspan', 1),
                    sticky="nsew", padx=2, pady=2)
        
        # Hover logic
        def on_enter(event, h_color=hover_color):
            if event.widget['bg'] != Style.SECOND_ACTIVE_BG:
                event.widget.config(bg=h_color)
        
        def on_leave(event, b_color=bg_color):
            if event.widget['bg'] != Style.SECOND_ACTIVE_BG:
                event.widget.config(bg=b_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        if b_info.get('toggle', False):
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
        key_map = {
            '<Return>': self._evaluate_ui, '<BackSpace>': self._backspace_ui, '<Escape>': self._clear_ui,
            '1': lambda: self._input('1'), '2': lambda: self._input('2'), '3': lambda: self._input('3'), 
            '4': lambda: self._input('4'), '5': lambda: self._input('5'), '6': lambda: self._input('6'), 
            '7': lambda: self._input('7'), '8': lambda: self._input('8'), '9': lambda: self._input('9'), 
            '0': lambda: self._input('0'), '.': lambda: self._input('.'), '+': lambda: self._input('+'), 
            '-': lambda: self._input('-'), '/': lambda: self._input('/'), '(': lambda: self._input('('), 
            ')': lambda: self._input(')'), '*': lambda: self._input('*')
        }
        for key, func in key_map.items():
            self.master.bind(key, lambda event, f=func: f())

    # --- UI Update and Interaction Methods (Intermediary/Controller) ---

    def update_display(self):
        display_text = self.core._format_for_display(self.core.expression)
        self.label.config(text=display_text if self.core.expression else "0")
        self.total_label.config(text=self.core.total_history)
        self.mode_label.config(text="DEG" if self.core.is_deg_mode else "RAD")

    def _input(self, value):
        self.core.add_to_expression(value)
        self.update_display()
        
    def _clear_ui(self):
        self.core.clear()
        self.update_display()

    def _backspace_ui(self):
        self.core.backspace()
        self.update_display()
        
    def _evaluate_ui(self):
        self.core.evaluate()
        self.update_display()

    def _recall_ans_ui(self):
        self.core.recall_last_answer()
        self.update_display()

    def _mem_clear_ui(self):
        self.core.memory_clear()
    
    def _mem_recall_ui(self):
        self.core.memory_recall()
        self.update_display()

    def _mem_add_ui(self):
        self.core.memory_add()
        self.update_display()

    def _mem_sub_ui(self):
        self.core.memory_subtract()
        self.update_display()

    def _toggle_deg_rad_ui(self):
        mode = self.core.toggle_deg_rad()
        self.btn_deg.config(text=mode)
        self.mode_label.config(text=mode)
    
    def _toggle_2nd_mode_ui(self):
        is_second = self.core.toggle_second_mode()
        bg = Style.SECOND_ACTIVE_BG if is_second else Style.FUNCTION_BG_COLOR
        self.btn_2nd.config(bg=bg)

        for button, b_info in self.toggleable_buttons:
            if is_second:
                text, cmd_str = b_info['s_text'], b_info['s_cmd']
            else:
                text, cmd_str = b_info['p_text'], b_info['p_cmd']
            
            action = lambda val=cmd_str: self._input(val)
            button.config(text=text, command=action)


# --- Main Execution ---
if __name__ == "__main__":
    
    window = tk.Tk()
    calculator_core = CalculatorCore()
    calculator_app = ScientificCalculator(window, calculator_core)
    window.mainloop()
