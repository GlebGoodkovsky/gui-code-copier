import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyperclip

class CodeCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Selector & Copier")
        self.root.geometry("600x450")
        self.root.minsize(400, 300)

        # Global set to store full paths of all selected files, regardless of current directory
        self.selected_file_paths = set() 

        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.current_directory = os.getcwd() # Start in the directory where the script is run
        
        # --- Directory Path Display Frame ---
        path_frame = tk.Frame(root, bd=2, relief="groove")
        path_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.path_label = tk.Label(path_frame, text=f"Current Dir: {self.current_directory}", wraplength=550, anchor="w")
        self.path_label.pack(side="left", fill="x", expand=True, padx=5, pady=2)
        
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

        self.checkbox_vars = {} # Stores filename: tk.BooleanVar for *currently displayed* files
        
        self.load_files() # Load files when the app starts

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
        # Clear existing checkboxes and variables from previous directory view
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = {} # Reset this dict for the new directory's files

        # Update the displayed path label
        self.path_label.config(text=f"Current Dir: {self.current_directory}")

        try:
            items = os.listdir(self.current_directory)
            items.sort(key=str.lower)

            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            
            # --- Add 'Go Up' directory option ---
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
                full_path = os.path.join(self.current_directory, f)
                
                # Check if this file was previously selected (sticky selection logic!)
                is_selected = full_path in self.selected_file_paths
                var = tk.BooleanVar(value=is_selected)
                
                # Bind the checkbox state change to our tracking method
                checkbox = tk.Checkbutton(self.scrollable_frame, text=f, variable=var, anchor="w",
                                          justify="left", padx=5,
                                          command=lambda p=full_path, v=var: self.toggle_selection(p, v))
                checkbox.pack(fill="x", padx=2, pady=1)
                self.checkbox_vars[f] = var # Keep track of currently displayed checkbox vars

        except PermissionError:
            messagebox.showerror("Permission Denied", f"Cannot access directory: {self.current_directory}\nAttempting to go back to parent directory.")
            self.current_directory = os.path.dirname(self.current_directory)
            if not self.current_directory:
                self.current_directory = os.path.expanduser("~")
            self.load_files()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
        self.canvas.yview_moveto(0)

    # New method to toggle selection state in our global set
    def toggle_selection(self, file_path, var):
        if var.get(): # If checkbox is now checked
            self.selected_file_paths.add(file_path)
        else: # If checkbox is now unchecked
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
        # Selects all files currently shown in the list
        for filename, var in self.checkbox_vars.items():
            if not var.get(): # Only change if not already selected to avoid redundant calls
                var.set(True)
                full_path = os.path.join(self.current_directory, filename)
                self.selected_file_paths.add(full_path)

    def deselect_all_displayed_files(self):
        # Deselects all files currently shown in the list
        for filename, var in self.checkbox_vars.items():
            if var.get(): # Only change if selected
                var.set(False)
                full_path = os.path.join(self.current_directory, filename)
                if full_path in self.selected_file_paths:
                    self.selected_file_paths.remove(full_path)

    def copy_all_selected_code(self):
        if not self.selected_file_paths:
            messagebox.showinfo("No Selection", "No files have been selected in any directory to copy.")
            return

        selected_content = []
        # Iterate through the global set of selected file paths
        # Sort for consistent output order, though not strictly required
        sorted_paths = sorted(list(self.selected_file_paths), key=str.lower) 

        for full_path in sorted_paths:
            filename = os.path.basename(full_path) # Get just the file name from the path
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                selected_content.append(f"\n\n# --- File: {full_path} ---\n\n{content}") # Use full path in header for clarity
            except Exception as e:
                messagebox.showwarning("File Read Error", f"Could not read selected file {full_path}: {e}\n(This file will be skipped.)")
        
        if not selected_content: # Possible if all selected files had read errors
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
