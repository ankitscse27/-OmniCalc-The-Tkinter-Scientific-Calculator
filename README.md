# -OmniCalc-The-Tkinter-Scientific-Calculator
OmniCalc: The sleek, dark-mode scientific calculator for students and pros. Built with Python, it masters advanced trig, logs, and more with a secure engine and full keyboard support

🚀 Engineering Scientific Calculator 🚀
A feature-rich, modern scientific calculator built with Python and Tkinter. This project provides a fully functional calculator with a sleek, dark-themed user interface, responsive design, and robust error handling.

(To create a GIF like this, you can use a free tool like ScreenToGif or LICEcap. Upload the GIF to a site like Imgur and paste the link here.)

✨ Key Features
This calculator goes beyond the basics, offering a wide range of scientific and engineering functions:

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
You need to have Python 3 installed. You can download it from python.org. Tkinter is included with most Python installations, so no external libraries are needed.

Installation & Execution
Clone the repository:

Bash

git clone https://github.com/your-username/your-repository-name.git
Navigate to the project directory:

Bash

cd your-repository-name
Run the script:

Bash

python calculator_script_name.py
(Replace calculator_script_name.py with the actual name of your Python file.)

And that's it! The calculator window should now appear on your screen.

🔎 Code Overview
The code is organized within a single class, ScientificCalculator, for clarity and encapsulation.

Style (Inner Class):

Centralizes all styling constants (colors, fonts). This makes it incredibly easy to change the theme of the entire application without hunting through the code.

__init__(self, master) (Constructor):

Initializes the main window, sets up state variables (like expression, is_deg_mode), and calls the methods to build the UI.

UI Creation (_create_... methods):

The UI is logically divided into a display_frame and a buttons_frame.

_get_button_definitions() defines the entire button layout in a single, easy-to-read list of dictionaries. This approach makes modifying the layout straightforward.

Buttons are created dynamically based on this list, with hover effects bound to each one for better user feedback.

Core Logic (evaluate, _preprocess_expression):

evaluate() is the heart of the calculation. It uses a safe eval() by providing a safe_dict containing only allowed mathematical functions from the math library. This is a critical security feature.

_preprocess_expression() intelligently handles DEG/RAD conversions by swapping functions like sin with sind (a custom lambda for degree calculations) before evaluation.

Functionality (toggle_..., memory_...):

toggle_second_mode() dynamically changes the text and command of multiple buttons, effectively doubling their functionality without cluttering the UI.

Memory and utility functions (clear, backspace) provide the complete calculator experience.

⌨️ Keyboard Shortcuts
For efficiency, the calculator can be operated using your keyboard:

Key(s)	Action
0-9, .	Enter numbers
+, -, /	Basic arithmetic operators
*	Multiplication (×)
( )	Add parentheses
Enter	Calculate the result (=)
Backspace	Delete last character
Escape	Clear the entire input

Export to Sheets
👤 Author
Ankit Singh

GitHub: @ankitscse27

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
