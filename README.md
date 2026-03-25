Markdown
# Logic Suite Pro | Methodology PS#08

An interactive Digital Logic Simulator ecosystem built to visualize binary arithmetic and electronic signal propagation. This project features a high-fidelity Half-Adder simulation and a custom "Pro Designer" sandbox.

## 🚀 Key Features
- **Half-Adder Simulator:** Real-time verification of Sum ($A \oplus B$) and Carry ($A \cdot B$) logic.
- **Pro Designer Mode:** A virtual breadboard to drag, drop, and wire AND, OR, XOR, and NOT gates.
- **Neon Signal Flow:** Dynamic visual feedback where active signals (1) glow in Cyan and inactive signals (0) remain Gray.
- **Hybrid Architecture:** Accessible via a standalone Desktop App (Pygame) or a Localhost Web Suite (Flask).

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Web Framework:** Flask
- **Graphics Engines:** Pygame (Desktop), Tailwind CSS & HTML5 Canvas (Web)
- **Logic Engine:** Native bitwise operations for 100% mathematical accuracy.

## ⚙️ Environment Setup & Installation
To run this project, ensure your Python `Scripts` folder is added to your System Environment Variables (PATH).

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Logic-Suite-Pro.git](https://github.com/YOUR_USERNAME/Logic-Suite-Pro.git)
   cd Logic-Suite-Pro
Install Dependencies:

Bash
pip install flask pygame
Run the Web Suite:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000.

📐 Methodology & System Model
The solution is modeled as a State-Driven Directed Graph. Gates act as nodes, while wires represent edges carrying binary states. The visualization approach utilizes a high-contrast "Neon" aesthetic to ensure information retention and clear logical flow during demonstrations.

👥 Team Methodology PS#08
M J Devesh (RA2511003010324)

Amitabh J (RA2511003010316)

Mrithula JP (RA2511053010151)