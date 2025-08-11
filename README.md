# 🖼️ Python GUI Code Copier

A modern, minimalist, cross-platform desktop application that provides a fast and intuitive graphical interface to select multiple code files, copy their combined content, and streamline your coding workflow.

---

## ✨ Features

-   **Modern Themed Interface:** A clean, visually appealing UI with themed widgets and a modern color palette that looks great on any OS.
-   **Sticky Checkbox Selection:** Visually select multiple files. Your selections are remembered even as you navigate between different folders.
-   **Smart Ignore Toggle 🙈:** Automatically hides common junk folders and files (like `.git`, `__pycache__`, `.venv`). You can toggle this on or off with a single click.
-   **Live File Filter 🔎:** Instantly filter the files in the current directory just by typing in the search box.
-   **Live Status Bar 📊:** A handy status bar at the bottom always shows you a live count of how many files you have selected in total.
-   **Full Selection Control ✅:**
    *   **Select/Deselect Displayed:** Quickly select or deselect all files currently visible in the list.
    *   **Clear All Selections:** A powerful global "reset" button that deselects every file you've chosen, across all directories.
-   **Instant Refresh 🔄:** A refresh button to instantly re-scan the current directory for any newly created or renamed files.
-   **Intuitive Directory Navigation:**
    *   Click `[ folder_name ]` to drill down into subdirectories.
    *   Click `[ .. ] Go Up` to ascend to the parent directory.
    *   Use the **"Change Dir..."** button for direct folder selection.

---

## 🛠️ Tech Stack

-   **Python 3:** The core programming language.
-   **Tkinter (`ttk`)**: Python's standard library for building a modern, themed graphical user interface.
-   **`os` module:** Used for interacting with the operating system to list directory contents and construct file paths.
-   **`pyperclip`:** A cross-platform Python module for copying text to the system clipboard.

---
## 🚀 Getting Started

To run this project on your machine, follow these steps.

### 1. System Prerequisites

-   **Python 3.6+**
-   **Tkinter:** This is usually included with Python. If not, install it with your system's package manager.
    -   **Arch Linux:** `sudo pacman -S python tk`
    -   **Debian/Ubuntu:** `sudo apt update && sudo apt install python3-tk`
    -   **Fedora/CentOS:** `sudo dnf install python3-tkinter`

### 2. Project Setup

1.  **Clone this repository:**
```bash
git clone https://github.com/GlebGoodkovsky/gui-code-copier.git
cd gui-code-copier
```

2.  **Create and Activate a Virtual Environment:** This is highly recommended to keep project dependencies separate from your system.
```bash
# Create the environment
python -m venv .venv
    
# Activate it (on Linux/macOS)
source .venv/bin/activate
```

Your terminal prompt should now start with `(.venv)`.

3.  **Install Dependencies using `requirements.txt`:** This command reads the `requirements.txt` file and automatically installs all necessary Python packages.
```bash
pip install -r requirements.txt
```

---

## 📚 Usage

1.  **Make sure your virtual environment is active.** (Your prompt should show `(.venv)`).
2.  **Run the GUI script:**
    ```bash
    python gui_copycode.py
    ```
3.  A GUI window will appear.
    *   Use the GUI buttons or your mouse to navigate and select files.
    *   Use the **Filter** box to quickly find files in the current directory.
    *   Use the **Select/Deselect** buttons for bulk actions.
    *   Click **"Copy ALL Selected Code 📋"** to copy everything to your clipboard!

### Deactivating the Virtual Environment

When you're done using the script, you can exit the virtual environment:
```bash
deactivate
```

```
## ⚠️ Troubleshooting

- Window doesn't appear / Tkinter error:

Ensure the tk package (or its equivalent for your OS/distro, e.g., python3-tk on Debian/Ubuntu) is installed system-wide.

Verify Python's Tkinter support by opening a Python interpreter (python) and typing import tkinter. If it gives an error, Tkinter setup is incomplete.

-   **"ModuleNotFoundError: No module named 'pyperclip'":** Make sure your virtual environment is active *before* you run the `pip install` command and *before* you run the script.
-   **Clipboard Error on Linux:** You may need a clipboard utility. Install one with your package manager:
    -   For X11 (most systems): `sudo pacman -S xclip` or `sudo apt install xclip`
    -   For Wayland: `sudo pacman -S wl-clipboard` or `sudo apt install wl-clipboard`

## 🤝 Contributing

Suggestions, bug reports, and pull requests are warmly welcome! Please feel free to open an issue to discuss features or submit changes.

## A Note on the Learning Process

This project was created as a hands-on exercise to develop a user-friendly desktop application for a common coding task. It demonstrates core concepts of GUI development (Tkinter), file system interaction (os module), and persistent selection logic. The goal was to create a simple, understandable, yet fully functional program that solves a real problem. I used an AI assistant as a tool to help write and, more importantly, explain the code, using it as a learning partner to grasp fundamentals step-by-step.
