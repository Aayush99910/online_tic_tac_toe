# 🎮 Online Tic-Tac-Toe Game

A real-time, online Tic-Tac-Toe game built using C++, Python (FastAPI), and WebSockets.  
The core game logic is implemented in C++, exposed to Python via Pybind11, and will be integrated with FastAPI for real-time online play.

---

## 🚀 Features (Current & Upcoming)

- ✅ C++-based Game Logic – Fast and efficient game mechanics
- ✅ Pybind11 Integration – Use C++ code in Python seamlessly
- 🛠️ FastAPI Backend (Coming Soon) – To manage game sessions and API requests
- 🛠️ WebSockets (Coming Soon) – For real-time multiplayer gameplay
- 🛠️ Frontend (Coming Soon) – Simple UI for player interactions

---

## 📂 Project Structure

```bash
📦 project-root
├── 📁 .vscode             # Editor configurations (for VS Code)
├── 📁 py_code             # Python-related files
│   └── main.py            # (Upcoming) FastAPI server
├── 📁 src                 # C++ game logic and bindings
│   ├── build/             # Compiled binaries (ignored in Git)
│   ├── gamelogic.cpp      # Core game logic (C++)
│   ├── gamelogic.h        # Header file for game logic
│   ├── CMakeLists.txt     # CMake configuration for building C++ code
│   ├── pyproject.toml     # Python project configuration
│   └── main.py            # Pybind11 main script for C++-Python binding
├── 📁 frontend            # (Upcoming) Frontend files
│   ├── index.html         # Game UI
│   ├── styles.css         # Styling
│   └── script.js          # Handles frontend logic
├── 📄 requirements.txt    # Python dependencies
├── 📄 README.md           # Project documentation (this file)
```

---

## 🛠️ Technologies Used

**Current:**
- C++ – Implements game logic
- Pybind11 – Bridges C++ and Python

**Planned:**
- FastAPI – For API requests and game session management
- WebSockets – For real-time multiplayer updates
- HTML, CSS, JavaScript (React optional) – Frontend interface

---

## 🎲 How It Works (So Far)

1. **Game Logic (C++)** – `gamelogic.cpp` implements Tic-Tac-Toe rules.
2. **C++ ↔ Python Binding (Pybind11)** – `setup.py` compiles and exposes C++ functions to Python.
3. **Testing the Game** – The compiled module allows running game logic in Python.
4. **(Next Steps)** – FastAPI and WebSockets for real-time play.

---

## 🏗️ Setup & Installation

### 🔹 Clone the Repository

```bash
git clone https://github.com/Aayush99910/online_tic_tac_toe
cd online_tic_tac_toe
```

### 🔹 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 Build C++ Code and Pybind Module

```bash
cd src
python main.py build_ext --inplace
```

(FastAPI and WebSockets setup will be added later)

---

## 🎯 Planned Features

- 📌 FastAPI Backend – Serve game sessions and handle requests.
- 📌 WebSockets – Enable real-time gameplay updates.
- 📌 Frontend UI – Minimal interface to interact with the game.

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-branch
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to your fork

```bash
git push origin feature-branch
```

5. Open a Pull Request

---

## 📝 License

This project is open-source under the MIT License.  
Feel free to modify and use it!

---

# 🎉 Happy Coding & Have Fun Playing Tic-Tac-Toe! 🎉
