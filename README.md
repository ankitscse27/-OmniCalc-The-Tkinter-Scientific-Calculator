OmniCalc: The Tkinter Scientific Calculator
OmniCalc is a sleek, feature-rich scientific calculator built with Python and Tkinter. Designed with a modern dark-mode UI, it's perfect for students and professionals who need a powerful yet intuitive tool for advanced calculations.

✨ Key Features
🔢 Standard Arithmetic: Addition, subtraction, multiplication, and division.

🔬 Scientific Functions:

Powers & Roots: xʸ, x², x³, √x, ³√x

Trigonometry: sin, cos, tan with DEG and RAD mode switching.

Inverse & Hyperbolic: sin⁻¹, cos⁻¹, tan⁻¹ and sinh, cosh, tanh available via the 2nd key.

📜 Logarithms & Constants: log₁₀, natural log (ln), eˣ, and the constants π and e.

🧮 Advanced Operations: Factorial (x!), percentage (%), and an ANS key to recall the last result.

🧠 Memory Functions: MC, MR, M+, M- to store and manipulate values.

🛡️ Safe Evaluation: Uses a restricted eval() with a custom dictionary of safe functions to prevent malicious code execution.

🎨 Modern UI/UX:

A visually appealing dark theme with responsive button-hover effects.

A clear, multi-line display showing both the current expression and the final result.

Responsive layout that adapts to window resizing.

⌨️ Keyboard Support: Full keyboard bindings for a faster workflow.

🛠️ Technologies Used
Language: Python 3

GUI Framework: Tkinter (standard library)

Modules: math, re

🚀 Getting Started
To run this calculator on your local machine, follow these simple steps.

Prerequisites
You need to have Python 3 installed. Tkinter is included with most Python installations, so no external libraries are needed.

Installation & Execution
Clone the repository:

Bash

git clone https://github.com/ankitscse27/-OmniCalc-The-Tkinter-Scientific-Calculator.git
Navigate to the project directory:

Bash

cd OmniCalc-The-Tkinter-Scientific-Calculator
Run the script:

Bash

python main.py
(Note: Replace main.py with the actual name of your Python file.)

The calculator window should now appear on your screen!

🔎 Code Overview
The code is neatly organized within the ScientificCalculator class for clarity and encapsulation.

Style (Inner Class): Centralizes all styling constants (colors, fonts). This makes it incredibly easy to change the application's theme.

__init__(self, master): The constructor initializes the main window, sets up state variables (like expression, is_deg_mode), and calls the methods to build the UI.

UI Creation (_create... methods): The UI is logically divided into a display_frame and a buttons_frame. The _get_button_definitions() method defines the entire layout in a single, easy-to-read list of dictionaries, making modifications straightforward.

Core Logic (evaluate, _preprocess_expression): evaluate() is the heart of the calculation, using a safe eval() with a predefined dictionary of math functions to ensure security. The _preprocess_expression() method intelligently handles DEG/RAD mode conversions before evaluation.

Functionality (toggle_..., memory_...): toggle_second_mode() dynamically changes the text and command of multiple buttons, effectively doubling their functionality. Memory and other utility functions provide the complete calculator experience.

⌨️ Keyboard Shortcuts
For efficiency, the calculator can be operated entirely with your keyboard:
Key(s)	Action
0-9, .	Enter numbers
+, -, /, *	Basic arithmetic operators
(, )	Add parentheses
Enter / Return	Calculate the result (=)
Backspace	Delete the last character
Escape	Clear the entire input (C)


👤 Author
Ankit Singh

GitHub: @ankitscse27

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
