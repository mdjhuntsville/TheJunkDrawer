import tkinter as tk
from tkinter import Menu, filedialog, ttk
from PIL import Image, ImageTk
import os

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        if "original_image" in globals():
            original_image.save(file_path)

def load_image(file_path):
    global original_image, displayed_image, canvas_image
    img = Image.open(file_path)
    original_image = img.copy()
    displayed_image = img
    update_canvas()

def update_canvas():
    global canvas_image
    if displayed_image:
        img_tk = ImageTk.PhotoImage(displayed_image)
        canvas.config(scrollregion=(0, 0, displayed_image.width, displayed_image.height))
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk  # Prevent garbage collection

def zoom_size(event=None):
    global displayed_image
    if original_image:
        zoom_level = zoom_var.get()
        if zoom_level == "Fit to Window":
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            scale = min(canvas_width / original_image.width, canvas_height / original_image.height)
            new_width = int(original_image.width * scale)
            new_height = int(original_image.height * scale)
        else:
            scale = int(zoom_level.strip('%')) / 100
            new_width = int(original_image.width * scale)
            new_height = int(original_image.height * scale)
        displayed_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        update_canvas()
        
def exit_program():
    root.destroy()

# Initialize main window
root = tk.Tk()
root.title("Matthew's Paint App")
root.geometry("600x600")
root.configure(bg="gray")

# Create menu bar
menu_bar = Menu(root, bg="darkgray", fg="black")
file_menu = Menu(menu_bar, tearoff=0, bg="darkgray", fg="black")
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_program)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Create a toolbar
toolbar = tk.Frame(root, bg="darkgray", height=20)
toolbar.pack(fill=tk.X, side=tk.TOP)

zoom_label = tk.Label(toolbar, text="Zoom:", bg="darkgray", fg="black")
zoom_label.pack(side=tk.LEFT, padx=5)

zoom_var = tk.StringVar(value="100%")
zoom_dropdown = ttk.Combobox(toolbar, textvariable=zoom_var, values=["100%", "50%", "25%", "10%", "Fit to Window"], state="readonly", width=15)
zoom_dropdown.pack(side=tk.LEFT)
zoom_dropdown.bind("<<ComboboxSelected>>", zoom_size)

# Create a frame to hold canvas and scrollbars
frame = tk.Frame(root, bg="gray")
frame.pack(fill=tk.BOTH, expand=True)

# Create scrollbars
h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
v_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL)

# Create canvas for drawing or displaying images
canvas = tk.Canvas(frame, bg="gray", xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
canvas.grid(row=0, column=0, sticky="nsew")

h_scroll.config(command=canvas.xview)
v_scroll.config(command=canvas.yview)

h_scroll.grid(row=1, column=0, sticky="ew")
v_scroll.grid(row=0, column=1, sticky="ns")

# Configure grid to expand properly
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

root.mainloop()
