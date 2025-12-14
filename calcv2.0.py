# Author: Ankit Singh (ankitscse27)
# Version: 2.1.1 - Fixed SyntaxError in _add_button function

import tkinter as tk
import math
import re

# --- Constants for Styling ---
# A modern dark theme with cyan and blue-gray accents.
class Style:
    BG_COLOR = "#1A2226"          # Dark Slate Blue/Gray
    DISPLAY_BG_COLOR = "#232D33"  # Slightly Lighter Slate
    BUTTON_BG_COLOR = "#4A5A63"   # Blue-Gray
    OPERATOR_BG_COLOR = "#26C6DA" # Bright Cyan
    FUNCTION_BG_COLOR = "#37474F" # Darker Blue-Gray
    SPECIAL_BG_COLOR = "#546E7A"  # Muted Blue-Gray
    SECOND_ACTIVE_BG = "#607D8B"  # Highlighted Gray
    WHITE = "#FFFFFF"
    LABEL_COLOR = "#F0F0F0"       # Soft White
    
    # Hover colors for visual feedback
    OPERATOR_HOVER_COLOR = "#80D8FF" # Light Cyan
    BUTTON_HOVER_COLOR = "#607D8B"   # Lighter Blue-Gray
    FUNCTION_HOVER_COLOR = "#546E7A" # Lighter Function Gray
    SPECIAL_HOVER_COLOR = "#78909C"  # Lighter Special Gray

    # Font styles
    LARGE_FONT = ("Arial", 32, "bold") # Reduced size for better fit
    SMALL_FONT = ("Arial", 14)
    BUTTON_FONT = ("Arial", 16, "bold")
    MODE_FONT = ("Arial", 12, "bold")
    AUTHOR_FONT = ("Arial", 9, "italic")
    DISPLAY_LIMIT = 35 # Max characters in the smaller total/history display

class ScientificCalculator:
    """
    An advanced scientific calculator with a modern GUI using Tkinter.
    
    Version 2.1.1: Fixed the SyntaxError in the _add_button helper method.
    """

    def __init__(self, master):
        """Initialize the calculator."""
        self.master = master
        master.title("Engineering Scientific Calculator (v2.1.1)")
        master.geometry("400x700")
        master.configure(bg=Style.BG_COLOR)
        master.minsize(400, 700)

        # --- State Variables ---
        self.expression = ""
        self.is_deg_mode = True
        self.is_second_mode = False
        self.memory = 0.0 # Use float for memory
        self.last_answer = 0.0
        self.toggleable_buttons = []
        self.is_last_input_operator = False

        # --- Safe Evaluation & Display Dictionaries ---
        self.safe_dict = self._create_safe_dict()
        self.DISPLAY_MAP = {'**': '^', '*': '×', '/': '÷', 'sqrt(': '√(', 'cbrt(': '³√(', 'log_y(': 'log(', 'y_root_x(': 'ⁿ√'}
        self.FUNCTIONS = ['sin(', 'cos(', 'tan(', 'log10(', 'log(', 'exp(', 'factorial(', 'sqrt(', 'cbrt(', 'pow(', 'asin(', 'acos(', 'atan(', 'sinh(', 'cosh(', 'tanh(', 'asinh(', 'acosh(', 'atanh(', 'log_y(', 'y_root_x(']
        
        # --- UI Setup ---
        self.display_frame = self._create_display_frame()
        self.buttons_frame = self._create_buttons_frame()
        self.total_label, self.label, self.mode_label = self._create_display_labels()
        self._create_author_label()
        self._configure_grid_weights()
        self.button_definitions = self._get_button_definitions()
        self._create_buttons()
        self._bind_keys()

    def _log_base_y(self, y, x):
        """Calculates log base y of x."""
        try:
            return math.log(x, y)
        except ValueError:
            raise ValueError("Invalid input for log base y: y must be positive and not 1, x must be positive.")
    
    def _xth_root(self, y, x):
        """Calculates the x-th root of y (y^(1/x))."""
        if x == 0:
            raise ZeroDivisionError("Cannot take the 0-th root.")
        if y < 0 and x % 2 == 0:
            raise ValueError("Cannot take an even root of a negative number.")
        # Need to handle negative base with odd exponent for real roots
        if y < 0 and x % 2 != 0:
            return -((-y)**(1/x))
        return y**(1/x)

    def _create_safe_dict(self):
        """Creates the dictionary of allowed functions for safe evaluation, including new functions."""
        safe_dict = {
            'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt, 'cbrt': lambda x: x**(1/3),
            'log10': math.log10, 'exp': math.exp, 'abs': abs,
            'factorial': math.factorial, 'pow': pow, 
            'log': math.log, # Natural log (ln)
            'log_y': self._log_base_y, # New function: log base y of x (log(x, y))
            'y_root_x': self._xth_root, # New function: x-th root of y (y**(1/x))
        }

        # Add trig and inverse trig functions (default is RAD mode versions)
        for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']:
            safe_dict[func] = getattr(math, func)
        
        # Add DEG mode versions
        safe_dict.update({
            'sind': lambda x: math.sin(math.radians(x)),
            'cosd': lambda x: math.cos(math.radians(x)),
            'tand': lambda x: math.tan(math.radians(x)),
            'asind': lambda x: math.degrees(math.asin(x)),
            'acosd': lambda x: math.degrees(math.acos(x)),
            'atand': lambda x: math.degrees(math.atan(x)),
        })
        return safe_dict

    def _configure_grid_weights(self):
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
        # Total/History label
        total_label = tk.Label(self.display_frame, text="", anchor=tk.E,
                               bg=Style.DISPLAY_BG_COLOR, fg=Style.LABEL_COLOR, 
                               padx=10, font=Style.SMALL_FONT)
        total_label.pack(expand=True, fill='both')

        # Main expression/result label
        label = tk.Label(self.display_frame, text="0", anchor=tk.E,
                         bg=Style.DISPLAY_BG_COLOR, fg=Style.WHITE, 
                         padx=10, font=Style.LARGE_FONT)
        label.pack(expand=True, fill='both')

        # Mode and Indicator label
        mode_label = tk.Label(self.display_frame, text="DEG", anchor=tk.W,
                              bg=Style.DISPLAY_BG_COLOR, fg=Style.OPERATOR_BG_COLOR, 
                              padx=10, font=Style.MODE_FONT)
        mode_label.pack(expand=True, fill='x', side='left')
        return total_label, label, mode_label
        
    def _create_author_label(self):
        author_label = tk.Label(self.display_frame, text="Ankit Singh (ankitscse27) v2.1.1", anchor=tk.E,
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
            {'p_text': 'xʸ', 'p_cmd': '**', 's_text': 'ʸ√x', 's_cmd': 'y_root_x(', 'type': 'func', 'row': 1, 'col': 1, 'toggle': True},
            {'p_text': '√x', 'p_cmd': 'sqrt(', 's_text': '³√x', 's_cmd': 'cbrt(', 'type': 'func', 'row': 1, 'col': 2, 'toggle': True},
            {'text': 'x!', 'command': 'factorial(', 'type': 'func', 'row': 1, 'col': 3},
            {'text': 'eˣ', 'command': 'exp(', 'type': 'func', 'row': 1, 'col': 4},
            
            {'p_text': 'sin', 'p_cmd': 'sin(', 's_text': 'sin⁻¹', 's_cmd': 'asin(', 'type': 'func', 'row': 2, 'col': 0, 'toggle': True},
            {'p_text': 'cos', 'p_cmd': 'cos(', 's_text': 'cos⁻¹', 's_cmd': 'acos(', 'type': 'func', 'row': 2, 'col': 1, 'toggle': True},
            {'p_text': 'tan', 'p_cmd': 'tan(', 's_text': 'tan⁻¹', 's_cmd': 'atan(', 'type': 'func', 'row': 2, 'col': 2, 'toggle': True},
            {'p_text': 'log₁₀', 'p_cmd': 'log10(', 's_text': 'log base y', 's_cmd': 'log_y(', 'type': 'func', 'row': 2, 'col': 3, 'toggle': True},
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
            
            {'text': 'e', 'command': 'e', 'type': 'num', 'row': 7, 'col': 0},
            {'text': 'π', 'command': 'pi', 'type': 'num', 'row': 7, 'col': 1},
            {'text': '0', 'command': '0', 'type': 'num', 'row': 7, 'col': 2},
            {'text': '+', 'command': '+', 'type': 'op', 'row': 7, 'col': 3},
            {'text': '-', 'command': '-', 'type': 'op', 'row': 7, 'col': 4},
            
            {'text': '+/–', 'command': self.negate_last_input, 'type': 'spec', 'row': 8, 'col': 0}, # New Negation
            {'text': 'ANS', 'command': self.recall_last_answer, 'type': 'func', 'row': 8, 'col': 1},
            {'text': '.', 'command': '.', 'type': 'num', 'row': 8, 'col': 2},
            {'text': '=', 'command': self.evaluate, 'type': 'op', 'row': 8, 'col': 3, 'colspan': 2},
        ]

    def _create_buttons(self):
        """Create and place all calculator buttons based on the defined layout."""
        for b_info in self.button_definitions:
            self._add_button(b_info)

    def _add_button(self, b_info):
        """Helper method to create and configure a single button. (FIXED SYNTAX ERROR HERE)"""
        bg_color, hover_color = self._get_button_colors(b_info['type'])
        
        is_toggleable = b_info.get('toggle', False)
        text = b_info.get('p_text', b_info.get('text', ''))
        cmd = b_info.get('p_cmd', b_info.get('command', ''))
        
        # Use lambda for simple commands or the callable for complex ones
        action = cmd if callable(cmd) else lambda x=cmd: self.add_to_expression(x)

        button = tk.Button(self.buttons_frame, text=text, bg=bg_color, fg=Style.WHITE,
                           font=Style.BUTTON_FONT, borderwidth=0, command=action)
        
        button.grid(row=b_info['row'], column=b_info['col'], 
                    columnspan=b_info.get('colspan', 1),
                    sticky="nsew", padx=2, pady=2)
        
        # Hover logic: respect the active background of the '2nd' button
        def on_enter(event, h_color=hover_color):
            if event.widget['bg'] != Style.SECOND_ACTIVE_BG:
                event.widget.config(bg=h_color)
        
        def on_leave(event, b_color=bg_color):
            # Only reset if the button is not the active '2nd' button
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
        self.master.bind("p", lambda event: self.add_to_expression('pi'))
        self.master.bind("E", lambda event: self.add_to_expression('e'))
    
    def add_to_expression(self, value):
        """
        Append a value to the current expression.
        Includes logic for implied multiplication and operator sequencing.
        """
        if self.expression == "Error":
            self.expression = ""
        
        operators = ('+', '-', '*', '/', '**', '%')
        
        # Check if the input value is a binary operator
        is_binary_operator = value in operators and value != '-'
        
        # Check if the input value is a function start
        is_function_start = value in self.FUNCTIONS or value == '('
        
        # 1. Implied Multiplication (e.g., 2pi, 3(4+5), e(1), 5sin() )
        requires_multiplication = False
        if self.expression:
            last_char = self.expression[-1]
            
            # Case 1: Digit/Constant followed by constant/function start/parenthesis
            if last_char.isdigit() or last_char in 'pi e':
                if value in 'pi e (' or is_function_start:
                    requires_multiplication = True
            
            # Case 2: Closing parenthesis followed by digit/constant/function start
            elif last_char == ')':
                if value.isdigit() or value in 'pi e' or is_function_start:
                    requires_multiplication = True
            
            # Case 3: Constant followed by a digit
            if value.isdigit() and last_char in 'pi e':
                requires_multiplication = True

        if requires_multiplication:
            self.expression += '*'

        # 2. Operator Sequencing (prevents '++' or '*/')
        if is_binary_operator and self.is_last_input_operator:
            # Replace the last operator with the new one
            # Find the last operator and replace it
            i = len(self.expression) - 1
            while i >= 0 and self.expression[i] in operators and self.expression[i] != '-':
                 i -= 1
            self.expression = self.expression[:i+1] + value
            
        else:
            # Append the new value
            self.expression += str(value)

        # Update operator state: only set True for binary operators
        self.is_last_input_operator = is_binary_operator
        
        # 3. Special handling for multi-input functions
        if value in ('log_y(', 'y_root_x('):
              self.expression += ',' # For functions like log_y(base, value) -> log_y(y, x)
        
        self._update_labels()

    def negate_last_input(self):
        """Toggles the sign of the last number or section of the expression."""
        if not self.expression or self.expression == "Error":
            self.expression = "(-0"
        
        # Find the last number or parenthesized expression
        match = re.search(r'([+\-*/(]|^)([e\d\.]+|pi|ANS)\s*$', self.expression)
        
        if match:
            operator_or_start = match.group(1)
            value = match.group(2)
            
            # Simple case: negate the entire expression if it's currently a single number
            if re.fullmatch(r'^-?\d+\.?\d*$', self.expression):
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
            
            # Complex case: wrap the last value in -()
            else:
                self.expression = self.expression[:match.start(2)] + '(-' + value + ')'
                
        elif self.expression.endswith(')'):
             # Find the opening parenthesis for the closing one
            count = 1
            i = len(self.expression) - 2
            while i >= 0:
                if self.expression[i] == ')':
                    count += 1
                elif self.expression[i] == '(':
                    count -= 1
                if count == 0:
                    break
                i -= 1
            
            # If the expression is already negated, remove the negation: -(...) -> ...
            if i > 1 and self.expression[i-1] == '-' and self.expression[i-2] in '+-*/(':
                 # Remove the '(-' and the trailing ')'
                 self.expression = self.expression[:i-1] + self.expression[i+1:-1]
            else:
                 # Add negation: ...(...) -> ...(-(...)
                 self.expression = self.expression[:i] + '(-' + self.expression[i:]
            
        else:
             # Just add a minus sign if possible
             self.expression += '-'

        self._update_labels()


    def clear(self):
        """Clear the entire expression and reset display."""
        self.expression = ""
        self.total_label.config(text="")
        self.is_last_input_operator = False
        self._update_labels()

    def backspace(self):
        """Remove the last character or clear an error."""
        if self.expression == "Error":
            self.clear()
        elif self.expression:
            last_char = self.expression[-1]
            self.expression = self.expression[:-1]
            
            # Reset operator state if the new last char is NOT an operator
            operators = ('+', '*', '/', '**', '%')
            if not self.expression or self.expression[-1] not in operators:
                 self.is_last_input_operator = False
            self._update_labels()

    def toggle_deg_rad(self):
        """Toggle between Degree and Radian modes."""
        self.is_deg_mode = not self.is_deg_mode
        self._update_labels() # Forces indicator update

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
        """Prepare the expression for safe evaluation, handling degree mode."""
        if self.is_deg_mode:
            # Apply 'd' suffix to all trig/inverse trig functions for DEG mode
            for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                # Use word boundaries to avoid replacing parts of sinh, cosh etc.
                expr = re.sub(r'\b' + func + r'\(', f'{func}d(', expr)
        return expr

    def _format_result(self, result):
        """Formats the numerical result for display, handling large/small numbers."""
        if result is None:
            return "0"
            
        try:
            # Round result to 12 decimal places for precision
            rounded_result = round(result, 12)
            
            # Use scientific notation if the number is very large or very small
            if abs(rounded_result) >= 1e12 or (abs(rounded_result) > 0 and abs(rounded_result) < 1e-6):
                return f"{rounded_result:.4e}"
            
            # Convert to int if it's a whole number
            if rounded_result == int(rounded_result):
                return str(int(rounded_result))
            
            return str(rounded_result)
        except OverflowError:
            return "Overflow"
        except Exception:
            return str(result) # Fallback

    def evaluate(self):
        """Evaluate the full expression using the restricted 'eval'."""
        
        temp_expr = self.expression
        display_expr = self._format_for_display(self.expression)
        
        if not temp_expr or self.is_last_input_operator:
            self.total_label.config(text=display_expr)
            return

        self.total_label.config(text=display_expr + "=")
        self.is_last_input_operator = False
        
        try:
            # --- PARENTHESIS FIX ---
            open_parens = temp_expr.count('(')
            close_parens = temp_expr.count(')')
            
            missing_parens = open_parens - close_parens
            if missing_parens > 0:
                temp_expr += ')' * missing_parens
            # -----------------------
            
            processed_expr = self._preprocess_expression(temp_expr)
            result = eval(processed_expr, {"__builtins__": None}, self.safe_dict)
            
            self.last_answer = result
            self.expression = self._format_result(result)
            
        except (ZeroDivisionError):
            self.expression = "Divide by Zero"
        except (SyntaxError):
            self.expression = "Syntax Error"
        except (NameError, TypeError, ValueError) as e:
            error_msg = str(e).split(':')[-1].strip().split('\n')[0].title()
            self.expression = f"Math Error ({error_msg})"
        except Exception:
            self.expression = "Unknown Error"
        finally:
            self._update_labels()

    def _format_for_display(self, expr):
        """Convert internal expression to a more readable format for display, with limit."""
        display_expr = expr
        
        # 1. Substitute internal code with display symbols
        for op, symbol in self.DISPLAY_MAP.items():
            display_expr = display_expr.replace(op, symbol)
            
        # 2. Add implied multiplication symbols for better readability (2pi -> 2×π)
        # Handle digits before constants/functions
        display_expr = re.sub(r'(?<=\d)(?=[a-zA-Z(])', '×', display_expr)
        
        # Handle constant/RHS-function before constant/LHS-function
        display_expr = re.sub(r'([πe])([a-zA-Z(])', r'\1×\2', display_expr)
        
        # Correctly map the constants after multiplication insertion
        display_expr = display_expr.replace('×pi', 'π').replace('×e', 'e') 
        
        # 3. Limit the length for the history display
        if len(display_expr) > Style.DISPLAY_LIMIT:
            display_expr = "..." + display_expr[-(Style.DISPLAY_LIMIT - 3):]
            
        return display_expr

    def _update_labels(self):
        """Update the display labels and indicators."""
        display_text = self._format_for_display(self.expression)
        
        # 1. Update main display
        self.label.config(text=display_text if self.expression and self.expression != "Error" else "0")
        
        # 2. Clear history if typing a new expression
        if not self.total_label.cget('text').endswith('='):
            self.total_label.config(text=display_text)
            
        # 3. Update indicators (DEG/RAD, M, ANS)
        mode = "DEG" if self.is_deg_mode else "RAD"
        
        indicators = [mode]
        if self.memory != 0.0:
            indicators.append("M")
        if self.last_answer != 0.0:
            indicators.append("ANS")
            
        self.mode_label.config(text=" ".join(indicators))


    # --- Memory and Answer Functions ---
    def memory_clear(self): 
        self.memory = 0.0
        self.total_label.config(text="Memory Cleared")
        self.expression = ""
        self._update_labels()
        
    def memory_recall(self): 
        self.add_to_expression(self._format_result(self.memory))
        
    def recall_last_answer(self): 
        self.add_to_expression(self._format_result(self.last_answer))
        
    def memory_op(self, operation):
        """Generic function to handle M+ and M- operations."""
        original_expression = self.expression
        
        # If the current expression is empty, try to use the last answer
        if not original_expression and self.last_answer != 0.0:
             val_to_add = self.last_answer
        else:
            try:
                # Evaluate the current expression to get the value
                processed_expr = self._preprocess_expression(original_expression)
                # Auto-close parentheses for memory op evaluation
                open_parens = processed_expr.count('(')
                close_parens = processed_expr.count(')')
                processed_expr += ')' * (open_parens - close_parens)
                
                val_to_add = eval(processed_expr, {"__builtins__": None}, self.safe_dict)
            except Exception:
                self.expression = "Error in M-op"
                self._update_labels()
                return
            
        self.memory = operation(self.memory, val_to_add)
        self.total_label.config(text=f"M = {self._format_result(self.memory)}")
        
        # CRITICAL UX CHANGE: Only clear the main display if the expression was evaluated just for M-op
        if original_expression == "":
            pass # Keep what's on the main screen (likely the last result)
        else:
            self.expression = ""
            
        self._update_labels()
            
    def memory_add(self): self.memory_op(lambda m, v: m + v)
    def memory_subtract(self): self.memory_op(lambda m, v: m - v)

# --- Main Execution ---
if __name__ == "__main__":
    window = tk.Tk()
    calculator = ScientificCalculator(window)

    window.mainloop()
