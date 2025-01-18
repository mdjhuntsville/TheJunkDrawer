import tkinter as tk
from tkinter import Menu

root = tk.Tk() #Create!
root.title("All your base")  # Set window title
root.geometry("400x400")
root.configure(bg="black")

menu_bar = Menu(root)  # Create a menu bar

file_menu = Menu(menu_bar, tearoff=0) # Create menu.
file_menu.add_command(label="to Us...")  # Add a command
menu_bar.add_cascade(label="Are Belong", menu=file_menu) #Add a dropdown.

root.config(menu=menu_bar) #Add the menu

root.mainloop() #Run it!