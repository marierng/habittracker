#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Building the GUI

# In[1]:


from database import HabitTrackerDB
from habit import Habit
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import datetime
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# In[2]:


class HabitTrackerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Habit Tracker")
        self.window.configure(background="black")
        self.window.geometry("1500x750")
        
        self.habit_db = HabitTrackerDB()

        # Set font properties
        heading_font = Font(family="Segae Script", size=75, weight="bold")
        subheading_font = Font(family="Segae Script", size=45, weight="bold")
        label_font = Font(family="Segae Script", size=20)

        # Welcome Heading
        welcome_label = tk.Label(
            self.window, text="Welcome to Habit-tracker!", font=heading_font, fg="white", bg="black"
        )
        welcome_label.pack(pady=75)

        # Create a Habit Button
        create_habit_button = tk.Button(
            self.window, text="Create a Habit", font=subheading_font, command=self.open_create_habit_window
        )
        create_habit_button.pack(pady=30)

        # View Habits Button
        view_habits_button = tk.Button(
            self.window, text="View Habits", font=subheading_font, command=self.open_view_habits_window
        )
        view_habits_button.pack(pady=30)

    def open_create_habit_window(self):
        create_habit_window = tk.Toplevel()
        create_habit_window.title("Create a Habit")
        create_habit_window.configure(background="black")
        create_habit_window.geometry("1500x750")

        # Set font properties
        heading_font = Font(family="Segae Script", size=60, weight="bold")
        subheading_font = Font(family="Segae Script", size=30, weight="bold")
        label_font = Font(family="Segae Script", size=25)

        # Heading - Create a New Habit
        create_heading_label = tk.Label(
            create_habit_window, text="You can create a new habit here!", font=heading_font, fg="white", bg="black"
        )
        create_heading_label.pack(pady=40)

        # Subheading - Enter the name of the habit
        create_subheading_label = tk.Label(
            create_habit_window,
            text="Enter the name of the habit, select the frequency and press create to create a new habit.",
            font=subheading_font,
            fg="white",
            bg="black",
            anchor="w",
        )
        create_subheading_label.pack(pady=20)

        # Name Label and Text Field
        name_label = tk.Label(create_habit_window, text="Name:", font=label_font, fg="white", bg="black")
        name_label.pack(pady=10)
        name_entry = tk.Entry(create_habit_window, font=label_font)
        name_entry.pack(pady=10)

        # Frequency Label and Dropdown Menu
        frequency_label = tk.Label(create_habit_window, text="Frequency:", font=label_font, fg="white", bg="black")
        frequency_label.pack(pady=10)
        frequency_var = tk.StringVar()
        frequency_dropdown = tk.OptionMenu(create_habit_window, frequency_var, "Daily", "Weekly", "Monthly")
        frequency_dropdown.config(font=label_font, bg="white", width=10)
        frequency_dropdown.pack(pady=10)

        def create_habit():
            if frequency_var.get() == "Daily":
                self.habit_db.insert_habit(name_entry.get(), frequency_var.get())
                messagebox.showinfo("Success", "Habit created successfully!")

            elif frequency_var.get() == "Weekly":
                create_weekly_habit_window = tk.Toplevel()
                create_weekly_habit_window.title("Create a Weekly Habit")
                create_weekly_habit_window.configure(background="black")
                create_weekly_habit_window.geometry("500x300")

                day_label = tk.Label(
                    create_weekly_habit_window,
                    text="Enter the day of the week:",
                    font=label_font,
                    fg="white",
                    bg="black",
                )
                day_label.pack(pady=10)
                day_var = tk.StringVar()
                day_dropdown = tk.OptionMenu(
                    create_weekly_habit_window,
                    day_var,
                    "Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                )
                day_dropdown.config(font=label_font, bg="white", width=10)
                day_dropdown.pack(pady=10)

                def create_weekly_habit():
                    self.habit_db.insert_habit(name_entry.get(), frequency_var.get(), day_var.get())
                    messagebox.showinfo("Success", "Habit created successfully!")

                confirm_button = tk.Button(
                    create_weekly_habit_window,
                    text="Confirm",
                    font=label_font,
                    fg="black",
                    bg="white",
                    command=create_weekly_habit,
                )
                confirm_button.pack(pady=20)

            elif frequency_var.get() == "Monthly":
                create_monthly_habit_window = tk.Toplevel()
                create_monthly_habit_window.title("Create a Monthly Habit")
                create_monthly_habit_window.configure(background="black")
                create_monthly_habit_window.geometry("500x300")

                date_label = tk.Label(
                    create_monthly_habit_window,
                    text="Enter the date:",
                    font=label_font,
                    fg="white",
                    bg="black",
                )
                date_label.pack(pady=10)
                date_var = tk.IntVar()
                date_dropdown = tk.OptionMenu(
                    create_monthly_habit_window,
                    date_var,
                    *range(1, 32),
                )
                date_dropdown.config(font=label_font, bg="white", width=10)
                date_dropdown.pack(pady=10)

                def create_monthly_habit():
                    self.habit_db.insert_habit(name_entry.get(), frequency_var.get(), date=date_var.get())
                    messagebox.showinfo("Success", "Habit created successfully!")

                confirm_button = tk.Button(
                    create_monthly_habit_window,
                    text="Confirm",
                    font=label_font,
                    fg="black",
                    bg="white",
                    command=create_monthly_habit,
                )
                confirm_button.pack(pady=20)

        create_button = tk.Button(
            create_habit_window,
            text="Create",
            font=label_font,
            fg="black",
            bg="white",
            command=create_habit,
        )
        create_button.pack(pady=20)

        create_habit_window.mainloop()
    
    def open_view_habits_window(self):
        view_habits_window = tk.Toplevel()
        view_habits_window.title("View Habits")
        view_habits_window.configure(background="black")
        view_habits_window.geometry("1500x750")

        # Create a canvas with scrollbar
        canvas = tk.Canvas(view_habits_window, bg="black")
        scrollbar = tk.Scrollbar(view_habits_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to contain the habit labels
        habit_frame = tk.Frame(canvas, bg="black")
        habit_frame.pack(fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=habit_frame, anchor="nw")

        # Set font properties
        heading_font = Font(family="Segae Script", size=60, weight="bold")
        subheading_font = Font(family="Segae Script", size=30, weight="bold")
        label_font = Font(family="Segae Script", size=20)

        # Call create_or_update_habit with habit_id
        habit_ids = [habit[0] for habit in self.habit_db.get_all_habits()]
        for habit_id in habit_ids:
            habit = self.habit_db.get_habit_by_id(habit_id)
            if habit is not None:
                habit_name = habit[1]
                self.create_or_update_habit(habit_id, habit_name)

        # Heading - Here's your current habits
        view_heading_label = tk.Label(
            habit_frame, text="Habits for today!", font=heading_font, fg="white", bg="black"
        )
        view_heading_label.pack(pady=40)

        current_date = datetime.date.today().strftime("%Y-%m-%d")
        habit_ids = self.habit_db.get_habit_ids_for_date(current_date)

        for habit_id in habit_ids:
            habit = self.habit_db.get_habit_by_id(habit_id)
            if habit is not None:
                habit_name = habit[1]
                frequency = habit[2]
                habit_id = habit_id

                # Display habit name
                habit_name_label = tk.Label(
                    habit_frame, text=habit_name, font=subheading_font, fg="white", bg="black"
                )
                habit_name_label.pack(pady=10)

                # Display frequency
                frequency_label = tk.Label(
                    habit_frame, text=f"Frequency: {frequency}", font=label_font, fg="white", bg="black"
                )
                frequency_label.pack(pady=10)

                # Add buttons for completion
                complete_button = tk.Button(habit_frame, text="Complete", 
                                            command=lambda habit_id=habit_id: self.habit_db.complete_habit(habit_id, current_date))
                complete_button.pack(pady=10)

                # Analytics Button
                view_analytics_button = tk.Button(
                    habit_frame,
                    text="View Analytics",
                    command=lambda habit_id=habit_id, habit_name=habit_name: self.open_analytics_window(habit_id, habit_name),
                )
                view_analytics_button.pack(pady=10)

                # Separator
                separator = tk.Label(
                    habit_frame,
                    text="-------------------------------------------",
                    font=subheading_font,
                    fg="white",
                    bg="black",
                )
                separator.pack()
        
        other_heading_label = tk.Label(
                    view_habits_window, text="Other Options", font=heading_font, fg="white", bg="black"
                )
        other_heading_label.pack(pady=40) 
        
        button_frame = tk.Frame(view_habits_window, bg="black")
        button_frame.pack()

        view_all_button = tk.Button(
            button_frame,
            text="View All Habits",
            font=subheading_font,
            fg="black",
            bg="white",
            command=self.view_all_habits,
        )
        view_all_button.grid(row=0, column=0, padx=10, pady=20)

        filter_by_frequency_button = tk.Button(
            button_frame,
            text="Filter by Frequency",
            font=subheading_font,
            fg="black",
            bg="white",
            command=self.filter_by_frequency,
        )
        filter_by_frequency_button.grid(row=0, column=1, padx=10, pady=20)
        
        analytics_button = tk.Button(
            button_frame,
            text="Analytics",
            font=subheading_font,
            fg="black",
            bg="white",
            command=self.open_general_analytics_window,
        )
        analytics_button.grid(row=0, column=2, padx=10, pady=20)

        # Configure the canvas scroll region
        habit_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        view_habits_window.mainloop()
        
    def open_general_analytics_window(self):
        analytics_window = tk.Toplevel()
        analytics_window.title("General Analytics")
        analytics_window.configure(background="black")
        analytics_window.geometry("1500x750")
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(analytics_window, bg="black")
        scrollbar = tk.Scrollbar(analytics_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=200)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to contain the habit labels
        habit_frame = tk.Frame(canvas, bg="black")
        habit_frame.pack(fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=habit_frame, anchor="nw")

        # Set font properties
        heading_font = Font(family="Segae Script", size=50, weight="bold")
        subheading_font = Font(family="Segae Script", size=30, weight="bold")
        label_font = Font(family="Segae Script", size=30)
        
        habit_id = 1
        name = "Habit"
        habit = Habit(habit_id, name)

        # Heading - General Analytics
        analytics_heading = tk.Label(habit_frame, text="Analytics Among All Habits", 
                                     font=heading_font, fg="white", bg="black")
        analytics_heading.pack(pady=20)

        for frequency in ['Daily', 'Weekly', 'Monthly']:
            
            frequency_heading = tk.Label(habit_frame, text=f"Frequency - {frequency}", 
                                              font=subheading_font, fg="white", bg="black")
            frequency_heading.pack(pady=15)
            
            # Longest Streak
            longest_streak = habit.get_longest_streak_among_all_habits(frequency)
            longest_streak_label = tk.Label(habit_frame, text=f"Habit with longest streak : {longest_streak}", 
                                            font=label_font, fg="white", bg="black")
            longest_streak_label.pack(pady=10)

            # Highest Completion Rate
            highest_completion_rate = habit.get_highest_completion_rate_among_all_habits(frequency)
            highest_completion_rate_label = tk.Label(habit_frame, 
                                                     text=f"Habit with highest completion rate (%) : {highest_completion_rate}", 
                                                     font=label_font, fg="white", bg="black")
            highest_completion_rate_label.pack(pady=10)

        # Plot Completion Rates
        plot_completion_rate_heading = tk.Label(habit_frame, 
                                                       text="Comparison of Completion Rate", 
                                                       font=subheading_font, fg="white", bg="black")
        plot_completion_rate_heading.pack(pady=10)
        completion_rate_figure = habit.plot_completion_rates()
        completion_rate_canvas = FigureCanvasTkAgg(completion_rate_figure, master=habit_frame)  
        completion_rate_canvas.draw()
        completion_rate_canvas.get_tk_widget().pack(pady=10)

        # Plot Current Streaks
        plot_current_streak_heading = tk.Label(habit_frame, 
                                                       text="Comparison of Current Streak", 
                                                       font=subheading_font, fg="white", bg="black")
        plot_current_streak_heading.pack(pady=10)
        current_streak_figure = habit.plot_current_streaks()
        current_streak_canvas = FigureCanvasTkAgg(current_streak_figure, master=habit_frame)  
        current_streak_canvas.draw()
        current_streak_canvas.get_tk_widget().pack(pady=10)
        
        # Configure the canvas scroll region
        habit_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def filter_by_frequency(self):
        # Create a new window for filtering habits by frequency
        filter_window = tk.Toplevel()
        filter_window.title("Filter by Frequency")
        filter_window.configure(background="black")
        filter_window.geometry("1500x750")

        # Heading
        heading_label = tk.Label(filter_window, text="Select Frequency", font=("Arial", 40, "bold"), bg="black", fg="white")
        heading_label.pack(pady=20)

        # Frequency dropdown menu
        frequency_var = tk.StringVar()
        frequency_dropdown = tk.OptionMenu(filter_window, frequency_var, "Daily", "Weekly", "Monthly")
        frequency_dropdown.config(font=("Arial", 30), bg="white", width=10)
        frequency_dropdown.pack(pady=10)

        # Go button
        def on_go():
            selected_frequency = frequency_var.get()
            habits = self.habit_db.get_habits_by_frequency(selected_frequency)

            # Display the habits in a new window
            display_window = tk.Toplevel()
            display_window.title("Filtered Habits")

            # Display the habits in a listbox
            habits_listbox = tk.Listbox(display_window, font=("Arial", 20), width=30)
            habits_listbox.pack(padx=20, pady=10)

            for habit in habits:
                habits_listbox.insert(tk.END, habit[1])

        go_button = tk.Button(filter_window, text="Go", font=("Arial", 30, "bold"), bg="white", fg="black", 
                              command=on_go)
        go_button.pack(pady=20)

        # Run the filter window
        filter_window.mainloop()
    
    def view_all_habits(self):
        # Create a new window
        view_all_window = tk.Toplevel()
        view_all_window.title("View All Habits")
        view_all_window.configure(background="black")
        view_all_window.geometry("1500x750")
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(view_all_window, bg="black")
        scrollbar = tk.Scrollbar(view_all_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=500)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to contain the habit labels
        habit_frame = tk.Frame(canvas, bg="black")
        habit_frame.pack(fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=habit_frame, anchor="nw")

        # Set font properties
        heading_font = Font(family="Segae Script", size=40, weight="bold")
        subheading_font = Font(family="Segae Script", size=30)
        label_font = Font(family="Segae Script", size=20)
        
        # Heading - All Habits
        all_habits_heading = tk.Label(habit_frame, text="All Habits", font=heading_font, fg="white", bg="black")
        all_habits_heading.pack(pady=5)
        
        habits = self.habit_db.get_all_habits()

        for i, habit in enumerate(habits):
            habit_name = habit[1]
            frequency = habit[2]
            habit_id = habit[0]

           # Display habit name
            habit_name_label = tk.Label(habit_frame, text=habit_name, font=subheading_font, fg="white", bg="black")
            habit_name_label.pack(pady=5, anchor='center')

            # Display frequency
            frequency_label = tk.Label(habit_frame, text=f"Frequency: {frequency}", font=label_font, fg="white", bg="black")
            frequency_label.pack(pady=5, anchor='center')

            # Delete button
            delete_button = tk.Button(
                habit_frame,
                text="Delete",
                command=lambda habit_id=habit_id: self.habit_db.delete_habit(habit_id)
            )
            delete_button.pack(pady=5, anchor='center')

            # Create the update button
            update_button = tk.Button(
                habit_frame,
                text="Update",
                command=lambda habit_id=habit_id, name=habit[1], frequency=habit[2], day=habit[3], date=habit[4]:
                    self.open_update_window(habit_id, name, frequency, day, date)
            )
            update_button.pack(pady=5, anchor='center')

            view_analytics_button = tk.Button(
                habit_frame, text="View Analytics",
                command=lambda habit_id=habit_id, habit_name=habit_name:
                    self.open_analytics_window(habit_id, habit_name)
            )
            view_analytics_button.pack(pady=5, anchor='center')

        # Configure the canvas scroll region
        habit_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        view_all_window.mainloop()


    def open_update_window(self, habit_id, name, frequency=None, day='Everyday', date=0):
        # Create a new window for updating the habit
        update_window = tk.Toplevel()
        update_window.title("Update Habit")

        # Create labels and entry fields for habit details
        name_label = tk.Label(update_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, name)  # Set the current habit name in the entry field
        name_entry.pack()
        
        day_entry = None
        date_entry = None

        if frequency == "Daily":
            frequency_label = tk.Label(update_window, text="Frequency:")
            frequency_label.pack()
            frequency_entry = tk.Entry(update_window)
            frequency_entry.insert(0, frequency)  # Set the current frequency in the entry field
            frequency_entry.pack()

        elif frequency == "Weekly":
            frequency_label = tk.Label(update_window, text="Frequency:")
            frequency_label.pack()
            frequency_entry = tk.Entry(update_window)
            frequency_entry.insert(0, frequency)  # Set the current frequency in the entry field
            frequency_entry.pack()

            day_label = tk.Label(update_window, text="Day:")
            day_label.pack()
            day_entry = tk.Entry(update_window)
            day_entry.insert(0, day)  # Set the current day in the entry field
            day_entry.pack()

        elif frequency == "Monthly":
            frequency_label = tk.Label(update_window, text="Frequency:")
            frequency_label.pack()
            frequency_entry = tk.Entry(update_window)
            frequency_entry.insert(0, frequency)  # Set the current frequency in the entry field
            frequency_entry.pack()

            date_label = tk.Label(update_window, text="Date:")
            date_label.pack()
            date_entry = tk.Entry(update_window)
            date_entry.insert(0, date)  # Set the current date in the entry field
            date_entry.pack()

        update_button = tk.Button(
            update_window,
            text="Update",
            command=lambda day_entry=day_entry, date_entry=date_entry: self.habit_db.update_habit(
                habit_id,
                name_entry.get(),
                frequency_entry.get() if frequency_entry else None,
                day_entry.get() if day_entry else 'Everyday',
                date_entry.get() if date_entry else 0   
            )
        )

        update_button.pack(pady=5)
        
    def open_analytics_window(self, habit_id, habit_name):
        analytics_window = tk.Toplevel()
        analytics_window.title("Analytics")
        analytics_window.configure(background="black")

        # Set font properties
        heading_font = Font(family="Segae Script", size=50, weight="bold")
        subheading_font = Font(family="Segae Script", size=30, weight="bold")
        label_font = Font(family="Segae Script", size=20)
        
        # Create an instance of the Habit class
        habit = Habit(habit_id, habit_name)

        # Heading - Analytics
        analytics_heading = tk.Label(analytics_window, text="Analytics", font=heading_font, fg="white", bg="black")
        analytics_heading.pack(pady=20)

        # Habit Name
        habit_name_label = tk.Label(analytics_window, text=habit_name, font=subheading_font, fg="white", bg="black")
        habit_name_label.pack()

        # Current Streak
        current_streak = habit.calculate_current_streak()  
        current_streak_label = tk.Label(analytics_window, text=f"Current Streak: {current_streak}", font=label_font,
                                        fg="white", bg="black")
        current_streak_label.pack()

        # Longest Streak
        longest_streak = habit.calculate_longest_streak()  
        longest_streak_label = tk.Label(analytics_window, text=f"Longest Streak: {longest_streak}", font=label_font,
                                        fg="white", bg="black")
        longest_streak_label.pack()

        # Completion Rate
        completion_rate = habit.calculate_completion_rate()  
        completion_rate_label = tk.Label(analytics_window, text=f"Completion Rate: {completion_rate}%", 
                                         font=label_font, fg="white", bg="black")
        completion_rate_label.pack()

        analytics_window.mainloop()
    
    def create_or_update_habit(self, habit_id, name):
        habit = Habit(habit_id, name)
        habit.habit_records()
        
    def run(self):
        self.window.mainloop()

