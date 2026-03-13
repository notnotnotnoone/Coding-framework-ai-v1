import tkinter as tk
import time

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital Clock")
        self.time_label = tk.Label(self.root, font=('times', 50, 'bold'), fg='red', bg='black')
        self.time_label.pack()
        self.update_time()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def run(self):
        self.root.mainloop()

clock = Clock()
clock.run()