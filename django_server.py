import tkinter as tk
import subprocess
import webbrowser

def start_django_server():
    subprocess.Popen(['python', 'manage.py', 'runserver'])

def open_browser():
    webbrowser.open('http://127.0.0.1:8000')

root = tk.Tk()
root.title("MASH Systems")

# Set window size and position
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

start_button = tk.Button(root, text="Start Server", command=start_django_server)
start_button.pack(pady=10)

browser_button = tk.Button(root, text="Open Mash Systems", command=open_browser)
browser_button.pack(pady=10)

root.mainloop()
