import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyperclip # This is the library you just installed with pip

class CodeCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Selector & Copier")
        self.root.geometry("600x450") # Set a default window size
        self.root.minsize(400, 300) # Minimum size

        # Configure grid weights so content expands nicely when resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Start in the directory where the script is run, or fall back to home if an issue
        self.current_directory = os.getcwd()
        
        # --- Directory Path Display Frame ---
        # Shows the current directory path
        path_frame = tk.Frame(root, bd=2, relief="groove")
        path_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.path_label = tk.Label(path_frame, text=f"Current Dir: {self.current_directory}", wraplength=550, anchor="w")
        self.path_label.pack(side="left", fill="x", expand=True, padx=5, pady=2)
        
        # --- File List Frame (with Canvas and Scrollbar) ---
        # This holds the scrollable list of files and folders with checkboxes
        list_frame = tk.Frame(root, bd=2, relief="sunken")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.canvas = tk.Canvas(list_frame)
        self.scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas) # This frame will contain the actual checkboxes/labels

        # Bind scrollable_frame size to canvas scrollregion to make scrolling work
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.checkbox_vars = {} # Dictionary to hold Checkbutton variables (filename: tk.BooleanVar)
        
        self.load_files() # Populate the file list when the app starts

        # --- Buttons Frame ---
        # Holds "Select All", "Deselect All", "Copy", and "Change Dir" buttons
        button_frame = tk.Frame(root, bd=2, relief="ridge")
        button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Left side buttons
        select_all_btn = tk.Button(button_frame, text="Select All", command=self.select_all_files)
        select_all_btn.pack(side="left", padx=5, pady=5)
        
        deselect_all_btn = tk.Button(button_frame, text="Deselect All", command=self.deselect_all_files)
        deselect_all_btn.pack(side="left", padx=5, pady=5)

        # Right side buttons
        copy_btn = tk.Button(button_frame, text="Copy Selected Code 📋", command=self.copy_selected_code, bg="lightblue", fg="darkblue", font=("Helvetica", 10, "bold"))
        copy_btn.pack(side="right", padx=5, pady=5)

        change_dir_btn = tk.Button(button_frame, text="Change Dir...", command=self.change_directory)
        change_dir_btn.pack(side="right", padx=5, pady=5)


    def load_files(self):
        # Clear existing checkboxes and variables when changing directories
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = {}

        # Update the displayed path
        self.path_label.config(text=f"Current Dir: {self.current_directory}")

        try:
            # Get items (files and directories) in the current directory
            items = os.listdir(self.current_directory)
            items.sort(key=str.lower) # Sort alphabetically, case-insensitive

            # Separate into directories and files for organized display
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            
            # --- Add 'Go Up' directory option ---
            # Allows navigating to the parent directory, unless at the root of the filesystem
            if self.current_directory != os.path.abspath(os.sep):
                up_dir_label = tk.Label(self.scrollable_frame, text="[ .. ] Go Up", fg="blue", cursor="hand2", anchor="w")
                up_dir_label.pack(fill="x", padx=2, pady=1)
                up_dir_label.bind("<Button-1>", lambda e: self.navigate_up_directory())

            # --- Display Directories (clickable labels) ---
            for d in dirs:
                dir_path = os.path.join(self.current_directory, d)
                dir_label = tk.Label(self.scrollable_frame, text=f"[ {d} ]", fg="green", cursor="hand2", anchor="w")
                dir_label.pack(fill="x", padx=2, pady=1)
                dir_label.bind("<Button-1>", lambda e, path=dir_path: self.change_directory_to(path))

            # --- Display Files (with checkboxes) ---
            for f in files:
                var = tk.BooleanVar(value=False) # Variable to track checkbox state (checked/unchecked)
                checkbox = tk.Checkbutton(self.scrollable_frame, text=f, variable=var, anchor="w",
                                          justify="left", padx=5)
                checkbox.pack(fill="x", padx=2, pady=1)
                self.checkbox_vars[f] = var # Store the variable so we can read its state later

        except PermissionError:
            # Handle cases where the script can't access a directory
            messagebox.showerror("Permission Denied", f"Cannot access directory: {self.current_directory}\nAttempting to go back to parent directory.")
            self.current_directory = os.path.dirname(self.current_directory)
            if not self.current_directory: # If we somehow hit an invalid or inaccessible path, default to home
                self.current_directory = os.path.expanduser("~")
            self.load_files() # Reload the file list for the corrected directory
        except Exception as e:
            # Catch any other unexpected errors during file loading
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
        # After loading, scroll the list to the very top
        self.canvas.yview_moveto(0)


    def change_directory(self):
        # Opens a system dialog to select a new directory
        new_dir = filedialog.askdirectory(initialdir=self.current_directory)
        if new_dir: # If a directory was selected (user didn't click Cancel)
            self.current_directory = new_dir
            self.load_files() # Reload files for the new directory

    def change_directory_to(self, path):
        # Navigates to a directory that was clicked in the list
        self.current_directory = path
        self.load_files()

    def navigate_up_directory(self):
        # Navigates to the parent directory of the current one
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory: # Prevent getting stuck at root
            self.current_directory = parent_dir
            self.load_files()

    def select_all_files(self):
        # Iterates through all file checkboxes and sets them to checked
        for var in self.checkbox_vars.values():
            var.set(True)

    def deselect_all_files(self):
        # Iterates through all file checkboxes and sets them to unchecked
        for var in self.checkbox_vars.values():
            var.set(False)

    def copy_selected_code(self):
        selected_content = []
        # Loop through all files that have a checkbox
        for filename, var in self.checkbox_vars.items():
            if var.get(): # Check if the checkbox is marked (True)
                full_path = os.path.join(self.current_directory, filename)
                try:
                    # Read the content of the selected file
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # Add a header with the filename and then the file's content
                    selected_content.append(f"\n\n# --- File: {filename} ---\n\n{content}")
                except Exception as e:
                    # If a specific file can't be read, show a warning but continue
                    messagebox.showwarning("File Read Error", f"Could not read file {filename}: {e}")
        
        if not selected_content:
            messagebox.showinfo("No Selection", "Please select at least one file to copy.")
            return

        # Join all the selected file contents into one big string
        combined_code = "".join(selected_content)
        
        try:
            # Use pyperclip to copy the combined string to the system clipboard
            pyperclip.copy(combined_code)
            messagebox.showinfo("Copied! 🎉", "Selected code copied to clipboard!")
        except pyperclip.PyperclipException as e:
            # If pyperclip encounters an error (e.g., no clipboard utility found on system)
            messagebox.showerror("Clipboard Error", f"Could not copy to clipboard. Ensure a clipboard utility (like 'xclip' or 'wl-clipboard' on Linux) is installed.\nError: {e}")
            # As a fallback, print the content to the console so it can be manually copied
            print("\n--- Content to copy (manual copy if clipboard failed) ---\n")
            print(combined_code)
            print("\n--------------------------------------------------------\n")

# This block runs when the script is executed directly
if __name__ == "__main__":
    root = tk.Tk() # Create the main window of the GUI
    app = CodeCopierApp(root) # Create an instance of our application
    root.mainloop() # Start the Tkinter event loop, which keeps the window open and responsive
