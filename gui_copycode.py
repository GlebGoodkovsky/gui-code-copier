# --- File: /home/wiphz/github/public/gui-code-copier/gui_copycode.py ---

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyperclip

class CodeCopierApp:
    # <<< NEW: A set of common file/folder names to ignore for a cleaner view.
    # A 'set' is used because checking if an item is in a set is very fast!
    IGNORE_PATTERNS = {".git", "__pycache__", ".venv", ".vscode", ".idea", "node_modules", ".DS_Store"}

    def __init__(self, root):
        self.root = root
        self.root.title("Code Selector & Copier")
        self.root.geometry("600x450")
        self.root.minsize(400, 300)

        self.selected_file_paths = set() 

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.current_directory = os.getcwd()
        
        # --- Directory Path Display Frame ---
        path_frame = tk.Frame(root, bd=2, relief="groove")
        path_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        path_frame.columnconfigure(0, weight=1) # <<< NEW: Allow the path label to expand

        self.path_label = tk.Label(path_frame, text=f"Current Dir: {self.current_directory}", wraplength=550, anchor="w")
        self.path_label.grid(row=0, column=0, sticky="ew", padx=5, pady=2) # <<< CHANGED from .pack() to .grid()

        # <<< NEW: A variable to hold the state of our checkbox (True = hide, False = show).
        self.hide_ignored_var = tk.BooleanVar(value=True)

        # <<< NEW: The actual checkbox widget to turn the filter on and off.
        # The `command=self.load_files` makes the list refresh every time you click it!
        self.hide_checkbox = tk.Checkbutton(
            path_frame, 
            text="Hide Ignored", 
            variable=self.hide_ignored_var,
            command=self.load_files
        )
        self.hide_checkbox.grid(row=0, column=1, padx=5) # <<< NEW: Placing the checkbox next to the path label.
        
        # --- File List Frame (with Canvas and Scrollbar) ---
        list_frame = tk.Frame(root, bd=2, relief="sunken")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.canvas = tk.Canvas(list_frame)
        self.scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

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

        self.checkbox_vars = {}
        
        self.load_files()

        # --- Buttons Frame ---
        button_frame = tk.Frame(root, bd=2, relief="ridge")
        button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        select_all_btn = tk.Button(button_frame, text="Select All Displayed", command=self.select_all_displayed_files)
        select_all_btn.pack(side="left", padx=5, pady=5)
        
        deselect_all_btn = tk.Button(button_frame, text="Deselect All Displayed", command=self.deselect_all_displayed_files)
        deselect_all_btn.pack(side="left", padx=5, pady=5)

        copy_btn = tk.Button(button_frame, text="Copy ALL Selected Code 📋", command=self.copy_all_selected_code, bg="lightblue", fg="darkblue", font=("Helvetica", 10, "bold"))
        copy_btn.pack(side="right", padx=5, pady=5)

        change_dir_btn = tk.Button(button_frame, text="Change Dir...", command=self.change_directory)
        change_dir_btn.pack(side="right", padx=5, pady=5)


    def load_files(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = {}

        self.path_label.config(text=f"Current Dir: {self.current_directory}")

        try:
            items = os.listdir(self.current_directory)

            # <<< NEW: The magic happens here! 🧙‍♂️
            # If our checkbox variable is True, we filter the 'items' list.
            if self.hide_ignored_var.get():
                items = [item for item in items if item not in self.IGNORE_PATTERNS]

            items.sort(key=str.lower)

            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            
            if self.current_directory != os.path.abspath(os.sep):
                up_dir_label = tk.Label(self.scrollable_frame, text="[ .. ] Go Up", fg="blue", cursor="hand2", anchor="w")
                up_dir_label.pack(fill="x", padx=2, pady=1)
                up_dir_label.bind("<Button-1>", lambda e: self.navigate_up_directory())

            for d in dirs:
                dir_path = os.path.join(self.current_directory, d)
                dir_label = tk.Label(self.scrollable_frame, text=f"[ {d} ]", fg="green", cursor="hand2", anchor="w")
                dir_label.pack(fill="x", padx=2, pady=1)
                dir_label.bind("<Button-1>", lambda e, path=dir_path: self.change_directory_to(path))

            for f in files:
                full_path = os.path.join(self.current_directory, f)
                
                is_selected = full_path in self.selected_file_paths
                var = tk.BooleanVar(value=is_selected)
                
                checkbox = tk.Checkbutton(self.scrollable_frame, text=f, variable=var, anchor="w",
                                          justify="left", padx=5,
                                          command=lambda p=full_path, v=var: self.toggle_selection(p, v))
                checkbox.pack(fill="x", padx=2, pady=1)
                self.checkbox_vars[f] = var

        except PermissionError:
            messagebox.showerror("Permission Denied", f"Cannot access directory: {self.current_directory}\nAttempting to go back to parent directory.")
            self.current_directory = os.path.dirname(self.current_directory)
            if not self.current_directory:
                self.current_directory = os.path.expanduser("~")
            self.load_files()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
        self.canvas.yview_moveto(0)

    # ... (the rest of your methods are unchanged) ...
    def toggle_selection(self, file_path, var):
        if var.get():
            self.selected_file_paths.add(file_path)
        else:
            if file_path in self.selected_file_paths:
                self.selected_file_paths.remove(file_path)

    def change_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.current_directory)
        if new_dir:
            self.current_directory = new_dir
            self.load_files()

    def change_directory_to(self, path):
        self.current_directory = path
        self.load_files()

    def navigate_up_directory(self):
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory:
            self.current_directory = parent_dir
            self.load_files()

    def select_all_displayed_files(self):
        for filename, var in self.checkbox_vars.items():
            if not var.get():
                var.set(True)
                full_path = os.path.join(self.current_directory, filename)
                self.selected_file_paths.add(full_path)

    def deselect_all_displayed_files(self):
        for filename, var in self.checkbox_vars.items():
            if var.get():
                var.set(False)
                full_path = os.path.join(self.current_directory, filename)
                if full_path in self.selected_file_paths:
                    self.selected_file_paths.remove(full_path)

    def copy_all_selected_code(self):
        if not self.selected_file_paths:
            messagebox.showinfo("No Selection", "No files have been selected in any directory to copy.")
            return

        selected_content = []
        sorted_paths = sorted(list(self.selected_file_paths), key=str.lower) 

        for full_path in sorted_paths:
            filename = os.path.basename(full_path)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                selected_content.append(f"\n\n# --- File: {full_path} ---\n\n{content}")
            except Exception as e:
                messagebox.showwarning("File Read Error", f"Could not read selected file {full_path}: {e}\n(This file will be skipped.)")
        
        if not selected_content:
            messagebox.showinfo("No Content", "No readable content found from selected files.")
            return

        combined_code = "".join(selected_content)
        
        try:
            pyperclip.copy(combined_code)
            messagebox.showinfo("Copied! 🎉", f"Successfully copied {len(selected_content)} file(s) to clipboard!")
        except pyperclip.PyperclipException as e:
            messagebox.showerror("Clipboard Error", f"Could not copy to clipboard. Ensure a clipboard utility (like 'xclip' or 'wl-clipboard' on Linux) is installed.\nError: {e}")
            print("\n--- Content to copy (manual copy if clipboard failed) ---\n")
            print(combined_code)
            print("\n--------------------------------------------------------\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCopierApp(root)
    root.mainloop()
