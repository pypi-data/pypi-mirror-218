import tkinter as tk
from tkinter import filedialog
import subprocess

class SatanEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Editor")

        self.textarea = tk.Text(self.root, wrap=tk.WORD)
        self.textarea.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Run", command=self.run_file)
        menubar.add_cascade(label="Run", menu=runmenu)

        self.root.config(menu=menubar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.textarea.delete(1.0, tk.END)
                self.textarea.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            content = self.textarea.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)

    def run_file(self):
        content = self.textarea.get(1.0, tk.END)
        temp_file = "temp.py"

        with open(temp_file, "w") as file:
            file.write(content)

        subprocess.run(["python", temp_file])

if __name__ == "__main__":
    root = tk.Tk()
    editor = SatanEditor(root)
    root.mainloop()
