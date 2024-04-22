import tkinter as tk

from habit_tracker import HabitTrackerApp

if __name__ == "__main__":
    # Start the Tkinter loop
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()