# OmniCalc: The Tkinter Scientific Calculator 🚀

A sleek, feature-rich scientific calculator built with **Python 3** and the standard **Tkinter** framework. Designed with a modern, responsive **dark-mode UI**, OmniCalc is a powerful yet intuitive tool perfect for students, engineers, and professionals requiring advanced calculation capabilities.



---

## ✨ Features at a Glance

OmniCalc provides a comprehensive set of functions while prioritizing user experience and security.

### 🔬 Scientific & Advanced Mathematics

| Category | Functions |
| :--- | :--- |
| **Basic Arithmetic** | Addition ($+$), Subtraction ($-$), Multiplication ($\times$), Division ($\div$) |
| **Powers & Roots** | $x^y$, $x^2$, $x^3$, $\sqrt{x}$, $\sqrt[3]{x}$, $e^x$, **$y^{1/x}$ (x-th root of y)** |
| **Trigonometry** | $\sin$, $\cos$, $\tan$, and their **Inverse** ($\sin^{-1}, \cos^{-1}, \tan^{-1}$) and **Hyperbolic** ($\sinh, \cosh, \tanh$) counterparts. |
| **Logarithms** | $\log_{10}$, $\ln$ (Natural Logarithm), **$\log_y(x)$ (Log base y of x)** |
| **Modes** | Toggle between **DEG** (Degrees) and **RAD** (Radians) for trigonometric calculations. |
| **Constants** | $\pi$, $e$ |
| **Utility** | Factorial ($x!$), Percentage ($\%$), **Negation ($\pm$)**, and an **ANS** key to recall the last result. |

### 🧠 Memory Management
Full memory functionality including:
* **MC** (Memory Clear)
* **MR** (Memory Recall)
* **M+** (Memory Add)
* **M-** (Memory Subtract)

### 🎨 Modern UI/UX & Workflow
* **Dark Mode Theme:** Visually appealing, professional, and easy on the eyes.
* **Multi-Line Display:** Clearly separates the current expression from the final, evaluated result.
* **Responsive Layout:** Adapts dynamically to window resizing.
* **Dynamic Indicators (M/ANS/DEG/RAD):** Provides clear visual cues on the current mode and active memory/answer status.
* **Full Keyboard Support:** Dedicated keyboard bindings for a faster, professional workflow.
* **Auto-Parenthesis Closing:** Automatically closes unmatched parentheses upon evaluation.
* **Implied Multiplication:** Automatically inserts the multiplication operator (`*`) between numbers and functions (e.g., `2sin(30)`).

### 🛡️ Secure Evaluation
Calculations are performed using a **restricted `eval()`** method paired with a carefully curated dictionary of safe mathematical functions (`math` module). This approach prevents the execution of malicious code, enhancing application security.

---

## 💻 Technologies & Architecture

### Stack
* **Language:** Python 3
* **GUI Framework:** Tkinter (Standard Library)
* **Core Modules:** `math`, `re` (Regular Expressions)

### Code Overview
The architecture is designed for clarity, maintainability, and extensibility, encapsulated within the `ScientificCalculator` class.

| Component | Responsibility | Key Design Feature |
| :--- | :--- | :--- |
| **`Style` Class** | Centralizes all application constants (colors, fonts, padding). | Facilitates **rapid theme switching** and styling consistency. |
| **UI Creation** | Defines the layout of the display and all button elements. | Uses a single, declarative list of dictionaries (`_get_button_definitions`) for easy layout modification. |
| **Core Logic** | Handles input processing, DEG/RAD mode conversion, and evaluation. | `evaluate()` ensures security via restricted function access and includes **auto-parentheses fix**. |
| **Functionality** | Implements utility features like memory and mode toggles. | `toggle_second_mode()` dynamically changes button commands and labels, effectively doubling the functionality. |

---

## 🛠️ Getting Started

### Prerequisites
Ensure you have **Python 3** installed. **Tkinter** is included by default with most Python distributions, so **no external packages are required**.

### Installation and Execution

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ankitscse27/-OmniCalc-The-Tkinter-Scientific-Calculator.git](https://github.com/ankitscse27/-OmniCalc-The-Tkinter-Scientific-Calculator.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd OmniCalc-The-Tkinter-Scientific-Calculator
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```
    *The calculator window will launch immediately.*

---

## ⌨️ Keyboard Shortcuts

Maximize your productivity with a complete set of keyboard bindings:

| Key(s) | Action |
| :--- | :--- |
| **0-9, .** | Enter number and decimal |
| **+, -, /, \*** | Basic arithmetic operators |
| **(, )** | Add parentheses |
| **Enter / Return** | Calculate the result **(=)** |
| **Backspace** | Delete the last character |
| **Escape** | Clear the entire input **(C)** |

---

## 🤝 Contribution & License

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/ankitscse27/-OmniCalc-The-Tkinter-Scientific-Calculator/issues) if you want to contribute.

### Author
* **Ankit Singh**
* GitHub: [@ankitscse27](https://github.com/ankitscse27)

### License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.
