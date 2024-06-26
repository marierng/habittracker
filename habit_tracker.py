import tkinter as tk
from tkinter import messagebox
import datetime

from database import Database


class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.database = Database()
        self.create_welcome_window()

    def create_welcome_window(self):
        welcome_label = tk.Label(self.root, text="Welcome to Habit Tracker")
        welcome_label.pack()

        create_habit_button = tk.Button(self.root, text="Create a Habit", command=self.create_habit_window)
        create_habit_button.pack()

        view_habits_button = tk.Button(self.root, text="View Habits", command=self.view_habits)
        view_habits_button.pack()

        longest_streak_button = tk.Button(self.root, text="Show Longest Streak", command=self.display_longest_streak)
        longest_streak_button.pack()

    def create_habit_window(self):
        self.habit_window = tk.Toplevel(self.root)
        self.habit_window.title("Create a Habit")

        name_label = tk.Label(self.habit_window, text="Habit Name:")
        name_label.pack()
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self.habit_window, textvariable=self.name_var)
        name_entry.pack()

        periodicity_label = tk.Label(self.habit_window, text="Periodicity:")
        periodicity_label.pack()
        self.periodicity_var = tk.StringVar(value="daily")
        periodicity_menu = tk.OptionMenu(self.habit_window, self.periodicity_var, "daily", "weekly", "monthly")
        periodicity_menu.pack()

        create_button = tk.Button(self.habit_window, text="Create", command=self.save_habit)
        create_button.pack()

        self.periodicity_var.trace("w", self.show_periodicity_entry)

    def show_periodicity_entry(self, *args):
        periodicity = self.periodicity_var.get()
        if periodicity == "weekly":
            self.weekly_window = tk.Toplevel(self.habit_window)
            self.weekly_window.title("Select Weekdays")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            self.selected_weekdays_vars = [tk.BooleanVar(value=False) for _ in days]
            for i, day in enumerate(days):
                checkbox = tk.Checkbutton(self.weekly_window, text=day, variable=self.selected_weekdays_vars[i])
                checkbox.pack()

            # Add a "Confirm" button
            confirm_button = tk.Button(self.weekly_window, text="Confirm", command=self.save_weekly_habit)
            confirm_button.pack()
        elif periodicity == "monthly":
            self.create_monthly_habit_window()
        else:
            if hasattr(self, "weekly_window"):
                self.weekly_window.destroy()

    def save_weekly_habit(self):
        # This function will be called when confirming the selection of weekdays
        selected_weekdays = [day for day, var in
                             zip(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                 self.selected_weekdays_vars) if var.get()]
        weekdays = ', '.join(selected_weekdays)
        self.weekly_window.destroy()
        self.save_habit(weekdays=weekdays)

    def save_habit(self, weekdays="", monthly_day=0):
        name = self.name_var.get()
        periodicity = self.periodicity_var.get()

        # Use the existing cursor to insert the habit
        self.database.create_habit(name, periodicity, weekdays, monthly_day)
        self.habit_window.destroy()  # Close the habit creation window
        messagebox.showinfo("Success", f"Habit '{name}' created!")

    def create_monthly_habit_window(self):
        self.monthly_window = tk.Toplevel(self.habit_window)
        self.monthly_window.title("Select Monthly Day")
        day_label = tk.Label(self.monthly_window, text="Select a day (1-31):")
        day_label.pack()
        self.monthly_day_var = tk.IntVar(value=1)
        day_entry = tk.Entry(self.monthly_window, textvariable=self.monthly_day_var)
        day_entry.pack()
        confirm_button = tk.Button(self.monthly_window, text="Confirm", command=self.save_monthly_habit)
        confirm_button.pack()

    def save_monthly_habit(self):
        monthly_day = self.monthly_day_var.get()
        self.monthly_window.destroy()  # Close the monthly habit creation window
        self.save_habit(monthly_day=monthly_day)

    def view_habits(self):
        self.close_all_toplevels()
        self.habits_window = tk.Toplevel(self.root)
        self.habits_window.title("Today's Habits")
        headline = tk.Label(self.habits_window, text="These are your daily habits", font=("Arial", 14))
        headline.pack()

        # Assuming you have a method to filter habits due today
        today_habits = self.get_habits_due_today()

        for habit in today_habits:
            habit_id, name, periodicity, weekdays, monthly_day = habit
            habit_frame = tk.Frame(self.habits_window)
            habit_frame.pack(fill='x')

            habit_label = tk.Label(habit_frame, text=f"{name} - {periodicity.capitalize()}")
            habit_label.pack(side='left')

            complete_button = tk.Button(habit_frame, text="Complete", command=lambda h=habit: self.complete_habit(h))
            complete_button.pack(side='left')

            analytics_button = tk.Button(habit_frame, text="Analytics",
                                         command=lambda h=habit_id: self.view_analytics(h))
            analytics_button.pack(side='left')

        # Button to show all habits
        all_habits_button = tk.Button(self.habits_window, text="View All Habits", command=self.show_all_habits)
        all_habits_button.pack()

    def get_habits_due_today(self):
        today = datetime.date.today()
        weekday = today.strftime('%A')  # e.g., 'Monday'
        day = today.day
        return self.database.get_day_habits(weekday, day)

    def complete_habit(self, habit):
        habit_id = habit[0]  # Extracting only the habit ID
        self.database.complete_habit(habit_id)

        messagebox.showinfo("Completed", "Habit marked as complete for today!")
        # Refresh the displayed habits list
        self.close_all_toplevels()

    def list_completions(self):
        completions = self.database.get_completions()

        if completions:
            for completion in completions:
                print(f"Completion ID: {completion[0]}, Habit ID: {completion[1]}, Date: {completion[2]}")
        else:
            print("No completions found.")

    def show_all_habits(self):
        self.close_all_toplevels()
        self.all_habits_window = tk.Toplevel(self.root)
        self.all_habits_window.title("All Habits")

        filter_button = tk.Button(self.all_habits_window, text="Filter by Frequency", command=self.filter_by_frequency)
        filter_button.pack()

        all_habits = self.database.get_all_habits()
        self.display_all_habits(all_habits)

    def filter_by_frequency(self):
        self.filter_window = tk.Toplevel(self.root)
        self.filter_window.title("Filter by Frequency")

        self.frequency_var = tk.StringVar(value="daily")
        frequency_dropdown = tk.OptionMenu(self.filter_window, self.frequency_var, "daily", "weekly", "monthly")
        frequency_dropdown.pack()

        go_button = tk.Button(self.filter_window, text="Go", command=self.apply_frequency_filter)
        go_button.pack()

    def apply_frequency_filter(self):
        periodicity = self.frequency_var.get()
        self.filter_window.destroy()

        # Clear existing frames and display filtered habits
        for widget in self.all_habits_window.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        filtered_habits = self.database.get_periodicity_habits(periodicity)

        for habit in filtered_habits:
            self.create_habit_frame(self.all_habits_window, habit)

    def display_all_habits(self, all_habits):
        # Clear existing frames and display all habits
        for widget in self.all_habits_window.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        for habit in all_habits:
            self.create_habit_frame(self.all_habits_window, habit)

    def create_habit_frame(self, window, habit):
        habit_id, name, periodicity, weekdays, monthly_day = habit
        habit_frame = tk.Frame(window)
        habit_frame.pack(fill='x', padx=5, pady=5)

        habit_label = tk.Label(habit_frame, text=f"{name} - {periodicity.capitalize()}")
        habit_label.pack(side='left')

        # Buttons for Complete, Update, Analytics, and Delete
        complete_button = tk.Button(habit_frame, text="Complete", command=lambda: self.complete_habit(habit))
        complete_button.pack(side='left')

        update_button = tk.Button(habit_frame, text="Update", command=lambda: self.update_habit(habit))
        update_button.pack(side='left')

        analytics_button = tk.Button(habit_frame, text="Analytics", command=lambda: self.view_analytics(habit_id))
        analytics_button.pack(side='left')

        delete_button = tk.Button(habit_frame, text="Delete", command=lambda: self.delete_habit(habit_id))
        delete_button.pack(side='left')

    def delete_habit(self, habit_id):
        self.database.delete_habit(habit_id)
        messagebox.showinfo("Deleted", "Habit deleted successfully")
        # Refresh the displayed habits list
        self.close_all_toplevels()

    def view_analytics(self, habit_id):
        habit_name, completions, current_streak, longest_streak, completion_rate = self.database.get_analytics(habit_id)

        analytics_message = f"Habit: {habit_name}\nTotal Completions: {len(completions)}\n" \
                            f"Current Streak: {current_streak}\n" \
                            f"Longest Streak: {longest_streak}\n" \
                            f"Completion Rate (Last 30 days): {completion_rate:.2f}%"
        messagebox.showinfo("Analytics", analytics_message)
        self.close_all_toplevels()

    def display_longest_streak(self):
        longest_streak, habit_name = self.database.get_overall_longest_streak()
        if habit_name:
            messagebox.showinfo("Longest Streak",
                                f"The longest streak is {longest_streak} days for habit '{habit_name}'.")
        else:
            messagebox.showinfo("Longest Streak", "No completions found.")

    def update_habit(self, habit):
        # Assuming habit is a tuple and the first element is the habit ID
        habit_id = habit[0]
        habit_id, name, periodicity, weekdays, monthly_day = self.database.get_habit(habit_id)

        # Create a new window for updating the habit
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Habit")

        # Name
        name_label = tk.Label(self.update_window, text="Habit Name:")
        name_label.pack()
        self.update_name_var = tk.StringVar(value=name)
        name_entry = tk.Entry(self.update_window, textvariable=self.update_name_var)
        name_entry.pack()

        # Periodicity
        periodicity_label = tk.Label(self.update_window, text="Periodicity:")
        periodicity_label.pack()
        self.update_periodicity_var = tk.StringVar(value=periodicity)
        periodicity_menu = tk.OptionMenu(self.update_window, self.update_periodicity_var, "daily", "weekly", "monthly")
        periodicity_menu.pack()
        self.update_periodicity_var.trace("w", self.update_show_additional_options)

        # Add a button to update the habit
        update_button = tk.Button(self.update_window, text="Update",
                                  command=lambda: self.commit_habit_update(habit_id))
        update_button.pack()

        # Initialize additional options based on current periodicity
        self.update_show_additional_options(periodicity)

    def update_show_additional_options(self, *args):
        periodicity = self.update_periodicity_var.get()
        # Remove existing widgets for weekdays or monthly day if they exist
        if hasattr(self, 'weekly_frame'):
            self.weekly_frame.destroy()
        if hasattr(self, 'monthly_frame'):
            self.monthly_frame.destroy()

        if periodicity == "weekly":
            self.weekly_frame = tk.Frame(self.update_window)
            self.weekly_frame.pack()
            self.selected_weekdays_vars = []
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                var = tk.BooleanVar(value=False)
                checkbox = tk.Checkbutton(self.weekly_frame, text=day, variable=var)
                checkbox.pack()
                self.selected_weekdays_vars.append(var)

        elif periodicity == "monthly":
            self.monthly_frame = tk.Frame(self.update_window)
            self.monthly_frame.pack()
            day_label = tk.Label(self.monthly_frame, text="Select Monthly Day (1-31):")
            day_label.pack()
            self.monthly_day_var = tk.IntVar(value=1)
            day_entry = tk.Entry(self.monthly_frame, textvariable=self.monthly_day_var)
            day_entry.pack()

    def commit_habit_update(self, habit_id):
        new_name = self.update_name_var.get()
        new_periodicity = self.update_periodicity_var.get()
        new_weekdays = ','.join([day for day, var in
                                 zip(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                     self.selected_weekdays_vars) if
                                 var.get()]) if new_periodicity == "weekly" else None
        new_monthly_day = self.monthly_day_var.get() if new_periodicity == "monthly" else None

        self.database.update_habit(habit_id, new_name, new_periodicity, new_weekdays, new_monthly_day)
        self.update_window.destroy()
        messagebox.showinfo("Updated", "Habit updated successfully")
        self.close_all_toplevels()

    @staticmethod
    def clear_window_contents(window):
        for widget in window.winfo_children():
            widget.destroy()

    def close_all_toplevels(self):
        # Close all toplevel windows
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
