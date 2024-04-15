import sqlite3
from datetime import datetime, timedelta
from database import Database

# Function to create and populate the test database
def setup_test_database():
    # Connect to the SQLite database (this will create the file if it doesn't exist)
    conn = sqlite3.connect('test_habits.db')
    cursor = conn.cursor()

    # Create the 'habits' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            periodicity TEXT CHECK(periodicity IN ('daily', 'weekly', 'monthly')),
            weekdays TEXT,
            monthly_day INTEGER CHECK(monthly_day >= 1 AND monthly_day <= 31)
        )
    ''')

    # Create the 'habit_completion' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_completion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date DATE NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
        )
    ''')

    # Insert test data into the 'habits' table
    habits = [
        ('Drink Water', 'daily', None, None),
        ('Exercise', 'weekly', 'Monday,Wednesday,Friday', None),
        ('Read Book', 'monthly', None, 15),
        ('Invalid Periodicity', 'yearly', None, None),  # Edge case: Invalid periodicity
    ]
    cursor.executemany('INSERT INTO habits (name, periodicity, weekdays, monthly_day) VALUES (?, ?, ?, ?)', habits)

    # Insert test data into the 'habit_completion' table
    today = datetime.now()
    completions = [
        (1, today.strftime('%Y-%m-%d')),  # Completion for today
        (2, (today - timedelta(days=1)).strftime('%Y-%m-%d')),  # Completion for yesterday
        (2, (today - timedelta(days=2)).strftime('%Y-%m-%d')),  # Consecutive completion for the day before yesterday
        (3, today.replace(day=15).strftime('%Y-%m-%d')),  # Monthly completion on the 15th
        (999, today.strftime('%Y-%m-%d')),  # Edge case: Non-existent habit ID
    ]
    cursor.executemany('INSERT INTO habit_completion (habit_id, completion_date) VALUES (?, ?)', completions)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print('Test database setup complete.')



def test_create_habit():
    # Connect to the SQLite database
    conn = sqlite3.connect('test_habits.db')
    cursor = conn.cursor()

    # Drop a table if it exists
    cursor.execute("""DROP TABLE IF EXISTS habits""")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    db = Database("test_habits.db")

    # Create a habit
    db.create_habit("Test habit", "monthly", "", 1)

    # Fetch the habit
    habits = db.get_all_habits()

    # Check the length and name
    assert len(habits) == 1
    assert habits[0][1] == "Test habit"

def test_get_habit():
    db = Database("test_habits.db")

    # Retrieve a habit by name or ID
    habit = db.get_habit("Test habit")  # Assuming get_habit takes a name or ID as an argument

    # Check the details of the habit
    assert habit['name'] == "Test habit"



if __name__ == '__main__':
    setup_test_database()