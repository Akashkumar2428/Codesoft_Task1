import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List")
        self.root.geometry("500x500")
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.button_font = Font(family="Arial", size=10)
        self.task_font = Font(family="Arial", size=12)
        self.completed_font = Font(family="Arial", size=12, overstrike=1)
        
        # Task list
        self.tasks = []
        
        # Create GUI
        self.create_widgets()
        self.create_menu()
        
    def create_widgets(self):
        # Title Label
        tk.Label(self.root, text="My To-Do List", font=self.title_font, pady=10).pack()
        
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        self.task_entry = tk.Entry(input_frame, width=40, font=self.task_font)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        add_button = tk.Button(input_frame, text="Add Task", font=self.button_font, 
                              command=self.add_task, bg="#4CAF50", fg="white")
        add_button.pack(side=tk.LEFT)
        
        # Task List Frame
        task_frame = tk.Frame(self.root)
        task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview with scrollbar
        self.tree = ttk.Treeview(task_frame, columns=("Status", "Task"), show="headings", height=10)
        
        # Configure columns
        self.tree.heading("Status", text="Status", anchor=tk.W)
        self.tree.heading("Task", text="Task", anchor=tk.W)
        self.tree.column("Status", width=80, minwidth=80)
        self.tree.column("Task", width=380, minwidth=380)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        complete_button = tk.Button(button_frame, text="Mark Complete", font=self.button_font,
                                  command=self.mark_complete, bg="#2196F3", fg="white")
        complete_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete Task", font=self.button_font,
                                command=self.delete_task, bg="#52F436", fg="white")
        delete_button.pack(side=tk.LEFT, padx=5)
        
        exit_button = tk.Button(button_frame, text="Exit", font=self.button_font,
                              command=self.root.quit, bg="#607D8B", fg="white")
        exit_button.pack(side=tk.LEFT, padx=5)
        
    def create_menu(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add Task", command=self.add_task)
        file_menu.add_command(label="Mark Complete", command=self.mark_complete)
        file_menu.add_command(label="Delete Task", command=self.delete_task)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def mark_complete(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_index = self.tree.index(selected_item[0])
            self.tasks[item_index]["completed"] = not self.tasks[item_index]["completed"]
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark complete.")
    
    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_index = self.tree.index(selected_item[0])
            del self.tasks[item_index]
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")
    
    def update_task_list(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add tasks with appropriate styling
        for i, task in enumerate(self.tasks):
            status = "✔ Done" if task["completed"] else "❌ Pending"
            self.tree.insert("", "end", values=(status, task["text"]))
            
            # Apply strikethrough for completed tasks
            if task["completed"]:
                self.tree.tag_configure(f"completed{i}", font=self.completed_font)
                self.tree.item(self.tree.get_children()[i], tags=(f"completed{i}",))
    
    def show_about(self):
        messagebox.showinfo("About", "To-Do List App\nVersion 1.0\n\nA simple task management application.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


