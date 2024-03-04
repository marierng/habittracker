#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Implementing Habit Class

# In[1]:


import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from database import HabitTrackerDB
import datetime


# In[2]:


class Habit:
    def __init__(self, habit_id, name, db = "habit_tracker.db"):
        self.habit_id = habit_id
        self.name = name
        self.db = HabitTrackerDB(db) 
        #self.db = db
        self.records = []

    def get_records(self):
        return self.db.get_records_by_habit_id(self.habit_id)  
    
    def habit_records(self):
        habit = self.db.get_habit_by_id(self.habit_id)
        frequency = habit[2]

        records = self.get_records()
        last_record_date = None
        if records:
            last_record = records[-1]
            last_record_date = datetime.datetime.strptime(last_record[2], "%Y-%m-%d")

        created_at = datetime.datetime.strptime(habit[5].split()[0], "%Y-%m-%d")
        if (records and last_record_date.date() <= datetime.date.today()) or (not records and created_at.date() <= datetime.date.today()):
            if last_record_date is not None:
                next_date = self.get_next_date(last_record_date, frequency, habit[3], habit[4])
            else:
                next_date = self.get_next_date(created_at, frequency, habit[3], habit[4])
            date = next_date.strftime("%Y-%m-%d")
            self.db.add_record(self.habit_id, date)

    @staticmethod
    def get_next_weekday(date, target_weekday):
        target_weekday = target_weekday.lower()
        weekdays = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }
        days_ahead = (weekdays[target_weekday] - date.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return date + datetime.timedelta(days=days_ahead)

    def get_next_monthday(self, date, day_of_month):
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1)
        else:
            next_month = date.replace(month=date.month + 1)
        next_date = next_month.replace(day=day_of_month)
        return next_date
    
    def get_next_date(self, last_date, frequency, day=None, date=None):
        if frequency == "Daily":
            return last_date + datetime.timedelta(days=1)
        elif frequency == "Weekly":
            return self.get_next_weekday(last_date, day)
        elif frequency == "Monthly":
            return self.get_next_monthday(last_date, date)

    def calculate_completion_rate(self):
        self.records = self.get_records()
        total_records = len(self.records)
        completed_records = sum(1 for record in self.records if record[3] == 1)
        completion_rate = completed_records / total_records * 100 if total_records > 0 else 0
        return round(completion_rate, 2) # round to 2 decimal places

    def calculate_current_streak(self):
        import datetime
        today = datetime.date.today()

        records = self.get_records()
        # Filter out records in the future
        records = [record for record in records if datetime.datetime.strptime(record[2], "%Y-%m-%d").date() <= today]
        sorted_records = sorted(records, key=lambda record: datetime.datetime.strptime(record[2], "%Y-%m-%d").date(), reverse=True)
        current_streak = 0

        for record in sorted_records:
            if record[3] == 1:
                current_streak += 1
            else:
                break

        return current_streak


    def calculate_longest_streak(self):
        records = self.get_records()
        sorted_records = sorted(records, key=lambda record: record[2])
        longest_streak = 0
        current_streak = 0

        for record in sorted_records:
            if record[3] == 1:  
                current_streak += 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
            else:
                current_streak = 0

        return longest_streak
    
    def get_longest_streak_among_all_habits(self, frequency):
        habits = self.db.get_all_habits()
        longest_streak = 0
        habit_with_longest_streak = None

        for habit in habits:
            if habit[2] == frequency:  # Check if the habit has the required frequency
                habit_id = habit[0]
                habit_name = habit[1]
                habit_instance = Habit(habit_id, habit_name)
                records = habit_instance.get_records()
                if records:  # Check if there are any records for the habit
                    habit_longest_streak = habit_instance.calculate_longest_streak()
                    if habit_longest_streak > longest_streak:
                        longest_streak = habit_longest_streak
                        habit_with_longest_streak = habit_name

        return habit_with_longest_streak

    def get_highest_completion_rate_among_all_habits(self, frequency):
        habits = self.db.get_all_habits()
        highest_completion_rate = 0
        habit_with_highest_completion_rate = None

        for habit in habits:
            if habit[2] == frequency:  # Check if the habit has the required frequency
                habit_id = habit[0]
                habit_name = habit[1]
                habit_instance = Habit(habit_id, habit_name)
                habit_completion_rate = habit_instance.calculate_completion_rate()
                if habit_completion_rate > highest_completion_rate:
                    highest_completion_rate = habit_completion_rate
                    habit_with_highest_completion_rate = habit_name

        return habit_with_highest_completion_rate
    
    def plot_completion_rates(self):
        habits = self.db.get_all_habits()
        habit_names = []
        completion_rates = []

        for habit in habits:
            habit_id = habit[0]
            habit_name = habit[1]
            habit_instance = Habit(habit_id, habit_name)
            habit_completion_rate = habit_instance.calculate_completion_rate()
            habit_names.append(habit_name)
            completion_rates.append(habit_completion_rate)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(habit_names, completion_rates, color='blue')
        plt.xlabel('Habits')
        plt.ylabel('Completion Rates (%)')
        plt.title('Completion Rates of All Habits')
        plt.xticks(rotation=45)

        return fig

    def plot_current_streaks(self):
        habits = self.db.get_all_habits()
        habit_names = []
        current_streaks = []

        for habit in habits:
            habit_id = habit[0]
            habit_name = habit[1]
            habit_instance = Habit(habit_id, habit_name)
            current_streak = habit_instance.calculate_current_streak()
            habit_names.append(habit_name)
            current_streaks.append(current_streak)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(habit_names, current_streaks, color='green')
        plt.xlabel('Habits')
        plt.ylabel('Current Streaks')
        plt.title('Current Streaks of All Habits')
        plt.xticks(rotation=45)

        return fig

