#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Setting up the Database

# In[1]:


import sqlite3
import os


# In[2]:


class HabitTrackerDB:
        
    def __init__(self, db_path="habit_tracker.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT,
                day TEXT DEFAULT 'Everyday',
                date INTEGER DEFAULT 0,
                created_at DATE DEFAULT (DATE(CURRENT_TIMESTAMP))
            )
        """)
        self.conn.commit()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT,
                completed INTEGER,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        """)
        self.conn.commit()

    def insert_habit(self, name, frequency=None, day='Everyday', date=0):
        query = "INSERT INTO habits (name, frequency, day, date) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, frequency, day, date))
        self.conn.commit()

    def update_habit(self, habit_id, name, frequency=None, day='Everyday', date=0):
        query = "UPDATE habits SET name = ?, frequency = ?, day = ?, date = ? WHERE id = ?"
        self.cursor.execute(query, (name, frequency, day, date, habit_id))
        self.conn.commit()

    def delete_habit(self, habit_id):
        query = "DELETE FROM habits WHERE id = ?"
        self.cursor.execute(query, (habit_id,))
        self.conn.commit()

    def get_all_habits(self):
        query = "SELECT * FROM habits"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_habit_by_id(self, habit_id):
        query = "SELECT * FROM habits WHERE id = ?"
        self.cursor.execute(query, (habit_id,))
        return self.cursor.fetchone()

    def get_habits_by_frequency(self, frequency):
        query = "SELECT * FROM habits WHERE frequency = ?"
        self.cursor.execute(query, (frequency,))
        return self.cursor.fetchall()

    def add_record(self, habit_id, date):
        query = "INSERT INTO records (habit_id, date, completed) VALUES (?, ?, ?)"
        self.cursor.execute(query, (habit_id, date, 0))
        self.conn.commit()

    def complete_habit(self, habit_id, date):
        query = "UPDATE records SET completed = 1 WHERE habit_id = ? AND date = ?"
        self.cursor.execute(query, (habit_id, date))
        self.conn.commit()

    def get_records_by_habit_id(self, habit_id):
        query = "SELECT * FROM records WHERE habit_id = ?"
        self.cursor.execute(query, (habit_id,))
        return self.cursor.fetchall()

    def get_habit_ids_for_date(self, date):
        query = "SELECT habit_id FROM records WHERE date = ?"
        self.cursor.execute(query, (date,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def delete_record(self, habit_id):
        query = "DELETE FROM records WHERE habit_id = ?"
        self.cursor.execute(query, (habit_id,))
        self.conn.commit()


# In[3]:


habit_db = HabitTrackerDB()
habit_db.create_table()

