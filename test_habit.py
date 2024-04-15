#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Testing the Habit Class

# In[1]:


import pytest
from habit import Habit
from database import HabitTrackerDB
import os
import datetime
import uuid


# In[2]:


@pytest.fixture
def setup():
    # Create new database and habit for testing
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    db.insert_habit("Test habit", frequency='Daily')
    habit_id = db.get_all_habits()[0][0]
    habit = Habit(habit_id, "Test habit", "test_db.db")

    # Print the habit_id and existing records
    print(f"habit_id: {habit_id}")
    print("Records before deletion:")
    records_before = habit.get_records()
    for record in records_before:
        print(record)

    # Attempt to delete existing records
    db.cursor.execute("DELETE FROM records WHERE habit_id=?", (habit_id,))
    db.conn.commit()

    # Print the records after deletion
    print("Records after deletion:")
    records_after = habit.get_records()
    for record in records_after:
        print(record)

    return habit


# In[3]:


def test_habit_records(setup):
    habit = setup
    # Get current records (should be empty)
    records_before = habit.get_records()
    assert len(records_before) == 0, f"Expected 0 records but got {len(records_before)}"

    # Call habit_records function
    habit.habit_records()

    # Check if a new record is created
    records_after = habit.get_records()
    assert len(records_after) == 1, f"Expected 1 record but got {len(records_after)}"

    # Check that the date of the new record is correct
    new_record = records_after[0]
    new_record_date = datetime.datetime.strptime(new_record[2], "%Y-%m-%d").date()
    today = datetime.date.today()

    # Get the habit details to check the frequency
    habit_details = habit.db.get_habit_by_id(habit.habit_id)
    frequency = habit_details[2]

    if frequency == "Daily":
        assert new_record_date == today + datetime.timedelta(days=1)
    elif frequency == "Weekly":
        day = habit_details[3]
        assert new_record_date == habit.get_next_weekday(today, day)
    elif frequency == "Monthly":
        date = habit_details[4]
        assert new_record_date == habit.get_next_monthday(today, date)
        
def test_completion_rate(setup):
    habit = setup
    # Case 1: No records
    assert habit.calculate_completion_rate() == 0, "Completion rate should be 0 when there are no records"

    # Case 2: One completed record
    habit.db.add_record(habit.habit_id, datetime.date.today().strftime("%Y-%m-%d"))
    habit.db.complete_habit(habit.habit_id, datetime.date.today().strftime("%Y-%m-%d"))
    assert habit.calculate_completion_rate() == 100, "Completion rate should be 100 when all records are completed"

    # Case 3: One completed and one incomplete record
    next_day = datetime.date.today() + datetime.timedelta(days=1)
    habit.db.add_record(habit.habit_id, next_day.strftime("%Y-%m-%d"))
    assert habit.calculate_completion_rate() == 50, "Completion rate should be 50 when half the records are completed"

def test_current_streak(setup):
    habit = setup
    # Case 1: No records
    assert habit.calculate_current_streak() == 0, "Current streak should be 0 when there are no records"

    # Case 2: One completed record
    today = datetime.date.today().strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, today)
    habit.db.complete_habit(habit.habit_id, today)
    assert habit.calculate_current_streak() == 1, "Current streak should be 1 when there is one completed record for today"

    # Case 3: Two consecutive completed records
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, yesterday)
    habit.db.complete_habit(habit.habit_id, yesterday)
    assert habit.calculate_current_streak() == 2, "Current streak should be 2 when there are two consecutive completed records"

    # Case 4: Incomplete record before the streak
    day_before = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, day_before)
    assert habit.calculate_current_streak() == 2, "Current streak should remain 2 when an incomplete record is added before the streak"

def test_longest_streak(setup):
    habit = setup
    # Case 1: No records
    assert habit.calculate_longest_streak() == 0, "Longest streak should be 0 when there are no records"

    # Case 2: One completed record
    today = datetime.date.today().strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, today)
    habit.db.complete_habit(habit.habit_id, today)
    assert habit.calculate_longest_streak() == 1, "Longest streak should be 1 when there is one completed record"

    # Case 3: Two consecutive completed records
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, yesterday)
    habit.db.complete_habit(habit.habit_id, yesterday)
    assert habit.calculate_longest_streak() == 2, "Longest streak should be 2 when there are two consecutive completed records"

    # Case 4: Incomplete record before the streak
    day_before = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    habit.db.add_record(habit.habit_id, day_before)
    assert habit.calculate_longest_streak() == 2, "Longest streak should remain 2 when an incomplete record is added before the streak"

