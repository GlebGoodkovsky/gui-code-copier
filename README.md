# 🖼️ Python GUI Code Copier

A minimalist, cross-platform desktop application that provides an intuitive graphical interface to select multiple code files from any project directory and copy their combined content (with filename headers) to your system's clipboard. Perfect for compiling code snippets for documentation, notes, or sharing.

---

## ✨ Features

-   **Graphical Interface:** Easy-to-use window with mouse-clickable elements and checkboxes.
-   **Checkbox Selection:** Visually select multiple files from the currently displayed directory.
-   **Sticky Selections:** Selected files remain marked even when navigating to different folders and returning.
-   **Directory Navigation (within GUI):**
    *   Click on `[ folder_name ]` to drill down into subdirectories.
    *   Click `[ .. ] Go Up` to ascend to the parent directory.
    *   Use the **"Change Dir..."** button to open a system file dialog for direct selection of any folder on your machine.
-   **Batch Copy:** A single click copies all currently and previously selected files' content into a single clipboard entry.
-   **Cross-Platform:** Designed to run seamlessly on Linux, Windows, and macOS.

---

## 🛠️ How It Works (Tech Stack)

This project is built using fundamental Python libraries to provide a straightforward desktop GUI experience.

-   **Python 3:** The core programming language.
-   **Tkinter:** Python's standard library for building the graphical user interface.
-   **`os` module:** Used for interacting with the operating system, such as listing directory contents and constructing file paths.
-   **`pyperclip`:** A cross-platform Python module for copying text to and pasting text from the system clipboard.

---

## 🚀 Getting Started (Setup & Usage)

To run this project on your machine, follow these steps.

### 1. System Prerequisites

-   **Linux (e.g., Arch):**
    -   Ensure you have `python`, `python-pip`, and the `tk` package for the GUI installed.
    ```bash
    sudo pacman -S python python-pip tk
    ```
-   **Debian/Ubuntu:**
    ```bash
    sudo apt update
    sudo apt install python3-tk
    ```
-   **macOS:**
    -   Tkinter usually comes pre-installed with Python from python.org. If you installed via Homebrew, ensure `python-tk` is installed.
-   **Windows:**
    -   Tkinter usually comes pre-installed with Python from [python.org](https://www.python.org/downloads/windows/), ensuring you check "Add Python to PATH" and that the "tcl/tk and IDLE" option is selected during installation.

### 2. Project Setup

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/GlebGoodkovsky/gui-code-copier.git
    ```
    *   This will create a folder named `gui-code-copier` in your current directory.

2.  **Navigate into the cloned project directory:**
    ```bash
    cd gui-code-copier
    ```

3.  **Create and Activate a Python Virtual Environment:**
    This isolates the project's Python packages, preventing conflicts with your system's Python.
    ```bash
    python -m venv .venv
    ```
    *   Activate the virtual environment:
        ```bash
        source .venv/bin/activate
        ```
        Your terminal prompt should now show `(.venv)` at the beginning (e.g., `(.venv) [user@hostname gui-code-copier]$`).

4.  **Install Python Dependencies:**
    This installs `pyperclip`, the only external Python library needed.
    *   Ensure your virtual environment is active (see step 3).
    ```bash
    pip install pyperclip
    ```

---

## 📚 Usage

1.  **Activate your virtual environment:**
    *   Navigate into the `gui-code-copier` project directory:
        ```bash
        cd /path/to/gui-code-copier
        # Example: cd ~/github/public/gui-code-copier
        ```
    *   Then activate the environment:
        ```bash
        source .venv/bin/activate
        ```
        Your terminal prompt should show `(.venv)`.

2.  **Run the GUI script:**
    *   Since you are already in the `gui-code-copier` directory and the virtual environment is active, you can run the script directly by its filename:
    ```bash
    python gui_copycode.py
    ```
    A GUI window will appear.
    *   **Navigate within the GUI:** Use the `[ folder_name ]`, `[ .. ] Go Up`, or **"Change Dir..."** button to browse to *any* directory on your system where your code files reside.
    *   Click checkboxes next to files to select them.
    *   Click "Select All Displayed" or "Deselect All Displayed" for current view.
    *   Click **"Copy ALL Selected Code 📋"** to copy all files you've checked (from any directory, even if not currently visible) to your clipboard.

### Deactivating the Virtual Environment

When you're done using the script, you can exit the virtual environment:
```bash
deactivate

## ⚠️ Troubleshooting

- Window doesn't appear / Tkinter error:

Ensure the tk package (or its equivalent for your OS/distro, e.g., python3-tk on Debian/Ubuntu) is installed system-wide.

Verify Python's Tkinter support by opening a Python interpreter (python) and typing import tkinter. If it gives an error, Tkinter setup is incomplete.

- "ModuleNotFoundError: No module named 'pyperclip'":

Make sure your virtual environment is active ((.venv) in your terminal prompt) before running the python command for the script.

Ensure you installed pyperclip into the active virtual environment (pip install pyperclip).

- No content copied to clipboard / Clipboard Error:

Ensure you have a clipboard utility installed on Linux (e.g., xclip for Xorg or wl-clipboard for Wayland). You can install them via sudo pacman -S xclip wl-clipboard.

## 🤝 Contributing

Suggestions, bug reports, and pull requests are warmly welcome! Please feel free to open an issue to discuss features or submit changes.

## A Note on the Learning Process

This project was created as a hands-on exercise to develop a user-friendly desktop application for a common coding task. It demonstrates core concepts of GUI development (Tkinter), file system interaction (os module), and persistent selection logic. The goal was to create a simple, understandable, yet fully functional program that solves a real problem. I used an AI assistant as a tool to help write and, more importantly, explain the code, using it as a learning partner to grasp fundamentals step-by-step.
