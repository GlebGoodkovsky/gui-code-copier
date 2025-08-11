import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
import os
import pyperclip

class CodeCopierApp:
    IGNORE_PATTERNS = {".git", "__pycache__", ".venv", ".vscode", ".idea", "node_modules", ".DS_Store"}

    COLORS = {
        "bg": "#F0F0F0", "bg_list": "#FFFFFF", "text": "#1F1F1F", 
        "accent": "#0078D7", "accent_fg": "#FFFFFF", "green": "#107C10", "blue": "#00539C"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Code Selector & Copier")
        self.root.geometry("650x550")
        self.root.minsize(500, 400)
        self.root.configure(bg=self.COLORS["bg"])

        self.style = ttk.Style(root)
        self.style.theme_use('clam')
        # ... (all style configurations are the same) ...
        self.style.configure('TFrame', background=self.COLORS["bg"])
        self.style.configure('TLabel', background=self.COLORS["bg"], foreground=self.COLORS["text"], font=('Segoe UI', 9))
        self.style.configure('TCheckbutton', background=self.COLORS["bg"], foreground=self.COLORS["text"], font=('Segoe UI', 9))
        self.style.configure('TButton', font=('Segoe UI', 9, 'bold'))
        self.style.configure('Status.TLabel', font=('Segoe UI', 8))
        self.style.configure('Header.TLabel', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Accent.TButton', background=self.COLORS["accent"], foreground=self.COLORS["accent_fg"])
        self.style.map('Accent.TButton', background=[('active', '#005A9E')])
        self.style.configure('Dir.TLabel', foreground=self.COLORS["green"], background=self.COLORS["bg_list"])
        self.style.configure('Up.TLabel', foreground=self.COLORS["blue"], background=self.COLORS["bg_list"])

        self.selected_file_paths = set() 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1) 
        self.current_directory = os.getcwd()
        
        # --- UI FRAMES ---
        path_frame = ttk.Frame(root, padding=(10, 5))
        path_frame.grid(row=0, column=0, sticky="ew")
        path_frame.columnconfigure(0, weight=1)
        search_frame = ttk.Frame(root, padding=(10, 5))
        search_frame.grid(row=1, column=0, sticky="ew")
        search_frame.columnconfigure(1, weight=1)
        list_container = tk.Frame(root, bd=2, relief="sunken")
        list_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        button_frame = ttk.Frame(root, padding=(10, 10))
        button_frame.grid(row=3, column=0, sticky="ew")
        
        # --- PATH & HIDE WIDGETS ---
        self.path_label = ttk.Label(path_frame, text=f"Current Dir: {self.current_directory}", wraplength=580, style='Header.TLabel')
        self.path_label.grid(row=0, column=0, sticky="ew")
        self.hide_ignored_var = tk.BooleanVar(value=True)
        self.hide_checkbox = ttk.Checkbutton(path_frame, text="Hide Ignored", variable=self.hide_ignored_var, command=self.load_files)
        self.hide_checkbox.grid(row=0, column=1, padx=10)
        
        # --- SEARCH WIDGETS ---
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_files())
        search_label = ttk.Label(search_frame, text="🔎 Filter:")
        search_label.grid(row=0, column=0, padx=(0, 5))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 9))
        search_entry.grid(row=0, column=1, sticky="ew")

        # <<< NEW: A refresh button to manually reload the file list.
        refresh_btn = ttk.Button(search_frame, text="🔄 Refresh", command=self.load_files)
        refresh_btn.grid(row=0, column=2, padx=5)
        
        # ... (rest of the __init__ method is unchanged) ...
        self.canvas = tk.Canvas(list_container, bg=self.COLORS["bg_list"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='List.TFrame')
        self.style.configure('List.TFrame', background=self.COLORS["bg_list"])
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.checkbox_vars = {}
        
        select_all_btn = ttk.Button(button_frame, text="Select All Displayed", command=self.select_all_displayed_files)
        select_all_btn.pack(side="left", padx=(0, 5))
        deselect_all_btn = ttk.Button(button_frame, text="Deselect All Displayed", command=self.deselect_all_displayed_files)
        deselect_all_btn.pack(side="left", padx=(0, 5))
        clear_all_btn = ttk.Button(button_frame, text="Clear All Selections", command=self.clear_all_selections)
        clear_all_btn.pack(side="left")
        copy_btn = ttk.Button(button_frame, text="Copy ALL Selected Code 📋", command=self.copy_all_selected_code, style='Accent.TButton')
        copy_btn.pack(side="right")
        change_dir_btn = ttk.Button(button_frame, text="Change Dir...", command=self.change_directory)
        change_dir_btn.pack(side="right", padx=5)

        self.status_bar = ttk.Label(root, text="", style='Status.TLabel', padding=(10, 3))
        self.status_bar.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.load_files()
        self.update_status_bar()

    # ALL OTHER METHODS (load_files, clear_all_selections, etc.) ARE UNCHANGED.
    # The new button just calls a method we already wrote!
    
    def load_files(self):
        search_term = self.search_var.get().lower()
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.checkbox_vars = {}
        self.path_label.config(text=f"Current: {self.current_directory}")
        try:
            items = os.listdir(self.current_directory)
            if self.hide_ignored_var.get(): items = [item for item in items if item not in self.IGNORE_PATTERNS]
            items.sort(key=str.lower)
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            if search_term: files = [f for f in files if search_term in f.lower()]
            if self.current_directory != os.path.abspath(os.sep):
                up_dir_label = ttk.Label(self.scrollable_frame, text="[ .. ] Go Up", style='Up.TLabel', cursor="hand2")
                up_dir_label.pack(fill="x", padx=5, pady=1)
                up_dir_label.bind("<Button-1>", lambda e: self.navigate_up_directory())
            for d in dirs:
                dir_path = os.path.join(self.current_directory, d)
                dir_label = ttk.Label(self.scrollable_frame, text=f"[ {d} ]", style='Dir.TLabel', cursor="hand2")
                dir_label.pack(fill="x", padx=5, pady=1)
                dir_label.bind("<Button-1>", lambda e, path=dir_path: self.change_directory_to(path))
            for f in files:
                full_path = os.path.join(self.current_directory, f)
                is_selected = full_path in self.selected_file_paths
                var = tk.BooleanVar(value=is_selected)
                cb = ttk.Checkbutton(self.scrollable_frame, text=f, variable=var, style='TCheckbutton', command=lambda p=full_path, v=var: self.toggle_selection(p, v))
                self.style.configure('List.TCheckbutton', background=self.COLORS["bg_list"])
                cb.configure(style='List.TCheckbutton')
                cb.pack(fill="x", padx=5)
                self.checkbox_vars[f] = var
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        self.canvas.yview_moveto(0)

    def clear_all_selections(self):
        if not self.selected_file_paths:
            messagebox.showinfo("Already Clear", "No files were selected.")
            return
        self.selected_file_paths.clear()
        self.load_files()
        self.update_status_bar()

    def update_status_bar(self):
        count = len(self.selected_file_paths)
        file_text = "file" if count == 1 else "files"
        self.status_bar.config(text=f"Total files selected: {count} {file_text}")

    def toggle_selection(self, file_path, var):
        if var.get(): self.selected_file_paths.add(file_path)
        else: self.selected_file_paths.discard(file_path)
        self.update_status_bar()

    def change_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.current_directory)
        if new_dir: self.change_directory_to(new_dir)

    def change_directory_to(self, path):
        self.current_directory = path
        self.load_files()

    def navigate_up_directory(self):
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory: self.change_directory_to(parent_dir)

    def select_all_displayed_files(self):
        all_displayed_paths = {os.path.join(self.current_directory, f) for f in self.checkbox_vars.keys()}
        self.selected_file_paths.update(all_displayed_paths)
        for var in self.checkbox_vars.values(): var.set(True)
        self.update_status_bar()

    def deselect_all_displayed_files(self):
        all_displayed_paths = {os.path.join(self.current_directory, f) for f in self.checkbox_vars.keys()}
        self.selected_file_paths.difference_update(all_displayed_paths)
        for var in self.checkbox_vars.values(): var.set(False)
        self.update_status_bar()

    def copy_all_selected_code(self):
        if not self.selected_file_paths:
            messagebox.showinfo("No Selection", "No files have been selected to copy.")
            return
        selected_content = []
        for full_path in sorted(list(self.selected_file_paths)):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
                selected_content.append(f"\n\n# --- File: {full_path} ---\n\n{content}")
            except Exception as e:
                messagebox.showwarning("File Read Error", f"Could not read {os.path.basename(full_path)}: {e}")
        if not selected_content:
            messagebox.showinfo("No Content", "No readable content found from selected files.")
            return
        try:
            pyperclip.copy("".join(selected_content))
            messagebox.showinfo("Copied! 🎉", f"Successfully copied {len(selected_content)} file(s)!")
        except pyperclip.PyperclipException as e:
            messagebox.showerror("Clipboard Error", f"Could not copy to clipboard.\nError: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCopierApp(root)
    root.mainloop()
