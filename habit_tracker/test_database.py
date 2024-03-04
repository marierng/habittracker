#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Testing the HabitTrackerDB Class

# In[1]:


import os
import pytest
from database import HabitTrackerDB


# In[2]:


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Delete the test database file if it exists
    if os.path.exists("test_db.db"):
        os.remove("test_db.db")
        
    yield
    
    # Delete the test database file if it exists
    if os.path.exists("test_db.db"):
        os.remove("test_db.db")


# In[3]:


def test_insert_habit():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    
    # Fetch the habit
    habits = db.get_all_habits()
    
    # Check the length and name 
    assert len(habits) == 1
    assert habits[0][1] == "Test habit"

def test_delete_habit():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
        
    # First insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]
    
    #Delete the habit
    db.delete_habit(habit_id)
    habits = db.get_all_habits()
    
    #Check the length
    assert len(habits) == 0
    
def test_update_habit():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
        
    # First insert a habit
    db.insert_habit("Test habit", frequency='Daily')
    habit_id = db.get_all_habits()[0][0]

    # Now update the habit
    db.update_habit(habit_id, "Updated habit", frequency='Weekly')
    
    # Fetch the habit again and check if it has been updated
    updated_habit = db.get_habit_by_id(habit_id)
    assert updated_habit[1] == "Updated habit"
    assert updated_habit[2] == "Weekly"
    
def test_get_all_habits():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
        
    # First, insert multiple habits
    db.insert_habit("Habit 1")
    db.insert_habit("Habit 2")
    db.insert_habit("Habit 3")

    # Now call the get_all_habits method
    habits = db.get_all_habits()

    # Check the number of habits returned
    assert len(habits) == 3

    # Also, check the names of the habits
    habit_names = [habit[1] for habit in habits]
    assert "Habit 1" in habit_names
    assert "Habit 2" in habit_names
    assert "Habit 3" in habit_names
def test_get_habit_by_id():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # First, insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Now retrieve the habit using the id
    habit = db.get_habit_by_id(habit_id)

    # Check the details of the returned habit
    assert habit is not None
    assert habit[0] == habit_id
    assert habit[1] == "Test habit"
def test_get_habits_by_frequency():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert habits with different frequencies
    db.insert_habit("Test habit daily", frequency="daily")
    db.insert_habit("Test habit weekly", frequency="weekly")
    db.insert_habit("Test habit monthly", frequency="monthly")

    # Get habits by frequency
    daily_habits = db.get_habits_by_frequency("daily")
    weekly_habits = db.get_habits_by_frequency("weekly")
    monthly_habits = db.get_habits_by_frequency("monthly")

    # Check that the correct number of habits were returned
    assert len(daily_habits) == 1
    assert len(weekly_habits) == 1
    assert len(monthly_habits) == 1

    # Check that the habits have the correct frequency
    assert daily_habits[0][2] == "daily"
    assert weekly_habits[0][2] == "weekly"
    assert monthly_habits[0][2] == "monthly"
def test_add_record():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.add_record(habit_id, "2023-07-20")

    # Get the records for the habit
    records = db.get_records_by_habit_id(habit_id)

    # Check that the correct number of records was returned
    assert len(records) == 1

    # Check that the record has the correct habit ID and date
    assert records[0][1] == habit_id
    assert records[0][2] == "2023-07-20"
def test_complete_habit():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.add_record(habit_id, "2023-07-20")

    # Complete the habit
    db.complete_habit(habit_id, "2023-07-20")

    # Get the records for the habit
    records = db.get_records_by_habit_id(habit_id)

    # Check that the habit was marked as completed
    assert records[0][3] == 1
def test_get_records_by_habit_id():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.add_record(habit_id, "2023-07-20")

    # Get the records for the habit
    records = db.get_records_by_habit_id(habit_id)

    # Check that the record was added
    assert len(records) == 1
    assert records[0][1] == habit_id
    assert records[0][2] == "2023-07-20"
def test_get_habit_ids_for_date():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.add_record(habit_id, "2023-07-20")

    # Get the habit ids for the date
    habit_ids = db.get_habit_ids_for_date("2023-07-20")

    # Check that the habit id is in the list of habit ids
    assert habit_id in habit_ids
def test_delete_record():
    db = HabitTrackerDB("test_db.db")
    db.create_table()
    
    # Insert a habit
    db.insert_habit("Test habit")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.add_record(habit_id, "2023-07-20")

    # Delete the record
    db.delete_record(habit_id)

    # Get the records for the habit
    records = db.get_records_by_habit_id(habit_id)

    # Check that the record list is empty
    assert len(records) == 0

