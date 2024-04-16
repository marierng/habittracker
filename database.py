import sqlite3
import datetime

from pyasn1.compat import string


class Database:
    def __init__(self, database="habits.db"):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def create_schema(self):
        # Create the 'habits' table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                periodicity TEXT,
                weekdays TEXT,
                monthly_day INTEGER
            )
        ''')

        # Create an additional table for tracking completions, if necessary
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_completion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date DATE NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')

        self.conn.commit()

    def close(self):
        # Close the cursor and connection properly
        self.cursor.close()
        self.conn.close()

    def create_habit(self, name, periodicity, weekdays="", monthly_day=0):
        assert weekdays == "" or monthly_day == 0
        # Use the existing cursor to insert the habit
        self.cursor.execute('INSERT INTO habits (name, periodicity, weekdays, monthly_day) VALUES (?, ?, ?, ?)',
                            (name, periodicity, weekdays, monthly_day))
        self.conn.commit()

    def get_habit(self, habit_id):
        self.cursor.execute("SELECT id, name, periodicity, weekdays, monthly_day FROM habits WHERE id = ?", (habit_id,))
        return self.cursor.fetchone()

    def get_day_habits(self, weekday, day):
        self.cursor.execute('''
                      SELECT id, name, periodicity, weekdays, monthly_day FROM habits
                      WHERE periodicity = 'daily'
                      OR (periodicity = 'weekly' AND weekdays LIKE ?)
                      OR (periodicity = 'monthly' AND monthly_day = ?)
                  ''', ('%' + weekday + '%', day))

        return self.cursor.fetchall()

    def get_all_habits(self):
        self.cursor.execute("SELECT id, name, periodicity, weekdays, monthly_day FROM habits")
        return self.cursor.fetchall()

    def get_periodicity_habits(self, periodicity):
        self.cursor.execute('SELECT id, name, periodicity, weekdays, monthly_day FROM habits WHERE periodicity = ?',
                            (periodicity,))
        return self.cursor.fetchall()

    def delete_habit(self, habit_id):
        # Delete the habit from the database
        self.cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.cursor.execute('DELETE FROM habit_completion WHERE habit_id = ?', (habit_id,))
        self.conn.commit()

    def update_habit(self, habit_id, new_name, new_periodicity, new_weekdays, new_monthly_day):
        # Update the database with new details
        self.cursor.execute('UPDATE habits SET name = ?, periodicity = ?, weekdays = ?, monthly_day = ? WHERE id = ?',
                            (new_name, new_periodicity, new_weekdays, new_monthly_day, habit_id))
        self.conn.commit()

    def complete_habit(self, habit_id):
        completion_date = datetime.date.today().isoformat()

        self.cursor.execute('''
            INSERT INTO habit_completion (habit_id, completion_date) VALUES (?, ?)
        ''', (habit_id, completion_date))
        self.conn.commit()

    def get_completions(self):
        self.cursor.execute("SELECT * FROM habit_completion")
        return self.cursor.fetchall()

    def get_analytics(self, habit_id):
        self.cursor.execute('SELECT name FROM habits WHERE id = ?', (habit_id,))
        habit_name = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT completion_date FROM habit_completion WHERE habit_id = ?', (habit_id,))
        completions = [datetime.datetime.strptime(row[0], '%Y-%m-%d').date() for row in self.cursor.fetchall()]

        current_streak = self.calculate_current_streak(completions)
        longest_streak = self.calculate_longest_streak(completions)
        completion_rate = self.calculate_completion_rate(completions, 30) * 100

        return habit_name, completions, current_streak, longest_streak, completion_rate

    @staticmethod
    def calculate_current_streak(completions):
        if not completions:
            return 0
        streak = 1
        for i in range(len(completions) - 1, 0, -1):
            if (completions[i] - completions[i - 1]).days == 1:
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def calculate_longest_streak(completions):
        if not completions:
            return 0
        longest_streak = 1
        current_streak = 1
        for i in range(1, len(completions)):
            if (completions[i] - completions[i - 1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        return longest_streak

    @staticmethod
    def calculate_completion_rate(completions, days):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        completed_days = sum(start_date <= completion <= end_date for completion in completions)
        return completed_days / days

    def get_overall_longest_streak(self):
        self.cursor.execute(
            "SELECT habit_id, COUNT(*) as streak FROM habit_completion GROUP BY habit_id ORDER BY streak DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            habit_id, longest_streak = result
            self.cursor.execute("SELECT name FROM habits WHERE id = ?", (habit_id,))
            habit_name = self.cursor.fetchone()[0]
            return longest_streak, habit_name
        else:
            return 0, None
