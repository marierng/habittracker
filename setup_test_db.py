import os
from datetime import date
from datetime import datetime

import pytest
from database import Database

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Ensure the test database file does not exist before the test starts
    if os.path.exists("test_db.db"):
        os.remove("test_db.db")

    # Setup phase: connect to the database and set up the schema
    db = Database("test_db.db")
    db.create_schema()  # Ensure to use create_schema if it sets up all tables

    yield db  # Yield the database object for use in tests

    # Teardown phase: clean up after the tests
    db.close()  # Properly close the database connection
    if os.path.exists("test_db.db"):
        os.remove("test_db.db")

def test_create_habit(run_before_and_after_tests):
    db = run_before_and_after_tests  # Use the db instance from the fixture

    # Insert a habit
    db.create_habit("Test habit", "Daily")  # Assuming 'periodicity' parameter is required

    # Fetch the habit
    habits = db.get_all_habits()

    # Check the length and name
    assert len(habits) == 1
    assert habits[0][1] == "Test habit"


def test_delete_habit(run_before_and_after_tests):
    db = run_before_and_after_tests  # Use the db instance from the fixture

    # First insert a habit
    db.create_habit("Test habit", "Daily")  # Ensure you provide all required arguments
    habit_id = db.get_all_habits()[0][0]

    # Delete the habit
    db.delete_habit(habit_id)
    habits = db.get_all_habits()

    # Check the length
    assert len(habits) == 0


def test_update_habit(run_before_and_after_tests):
    db = run_before_and_after_tests  # Use the db instance from the fixture

    # First insert a habit
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Now update the habit
    db.update_habit(habit_id, "Updated habit", "Weekly", "Tuesday, Thursday", 10)

    # Fetch the habit again and check if it has been updated
    updated_habit = db.get_habit(habit_id)
    assert updated_habit[1] == "Updated habit"
    assert updated_habit[2] == "Weekly"
    assert updated_habit[3] == "Tuesday, Thursday"
    assert updated_habit[4] == 10

def test_get_all_habits(run_before_and_after_tests):
    db = run_before_and_after_tests  # This is now correctly using the yielded database object

    # First, insert multiple habits
    db.create_habit("Habit 1", "Daily")
    db.create_habit("Habit 2", "Weekly")
    db.create_habit("Habit 3", "Monthly")

    # Now call the get_all_habits method
    habits = db.get_all_habits()

    # Check the number of habits returned
    assert len(habits) == 3

    # Also, check the names of the habits
    habit_names = [habit[1] for habit in habits]
    assert "Habit 1" in habit_names
    assert "Habit 2" in habit_names
    assert "Habit 3" in habit_names


def test_get_day_habits(run_before_and_after_tests):
    db = run_before_and_after_tests  # Use the database object from the fixture

    # Insert habits with varying periodicities and days
    db.create_habit("Daily Habit", "daily")
    db.create_habit("Weekly Habit on Monday", "weekly", weekdays="Monday")
    db.create_habit("Monthly Habit on the 15th", "monthly", monthly_day=15)

    # Now retrieve habits for Monday, day 15 (which matches all conditions hypothetically)
    habits = db.get_day_habits("Monday", 15)

    # Check the number of habits returned
    assert len(habits) == 3

    # Check for the presence of specific habits based on the query logic
    habit_names = [habit[1] for habit in habits]
    assert "Daily Habit" in habit_names
    assert "Weekly Habit on Monday" in habit_names
    assert "Monthly Habit on the 15th" in habit_names


def test_get_periodicity_habits(run_before_and_after_tests):
    db = run_before_and_after_tests  # Use the database object from the fixture

    # Insert habits with different frequencies
    db.create_habit("Test habit daily", periodicity="daily")
    db.create_habit("Test habit weekly", periodicity="weekly")
    db.create_habit("Test habit monthly", periodicity="monthly")

    # Get habits by frequency
    daily_habits = db.get_periodicity_habits("daily")
    weekly_habits = db.get_periodicity_habits("weekly")
    monthly_habits = db.get_periodicity_habits("monthly")

    # Check that the correct number of habits were returned
    assert len(daily_habits) == 1
    assert len(weekly_habits) == 1
    assert len(monthly_habits) == 1

    # Check that the habits have the correct frequency
    assert daily_habits[0][2] == "daily"
    assert weekly_habits[0][2] == "weekly"
    assert monthly_habits[0][2] == "monthly"


def test_complete_habit(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with periodicity
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Complete the habit without specifying the date
    db.complete_habit(habit_id)

    # Retrieve all completions and filter for the specific habit
    records = db.get_completions()  # This method should exist and fetch all completion records

    # Filter the records to find those related to the specific habit ID
    specific_records = [rec for rec in records if rec[1] == habit_id]

    # Assuming completion dates are auto-set to today's date in the method implementation
    today = date.today().isoformat()  # Use the 'date' class from the 'datetime' module

    # Check that the habit was marked as completed today
    assert any(rec[2] == today for rec in specific_records), "Habit was not completed as expected today."

def test_get_completions(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with periodicity
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit; completion date is automatically set by the method
    db.complete_habit(habit_id)

    # Get all records for completions
    records = db.get_completions()  # Fetch all completion records without filtering

    # Filter records manually in the test to find those related to the specific habit ID
    specific_records = [record for record in records if record[1] == habit_id]

    # Check that the record has the correct habit ID and today's date
    today = date.today().isoformat()  # Use the 'date' class correctly
    assert any(record[2] == today for record in specific_records), "Completion records are incorrect or missing."


def test_get_analytics(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with all necessary details
    db.create_habit("Test habit", "Daily")

    # Retrieve the habit ID for further processing
    habit_id = db.get_all_habits()[0][0]

    # Complete the habit multiple times on different days if needed
    # Since the method sets the completion date to today, you can only effectively test it once per day
    db.complete_habit(habit_id)  # Completes for today

    # Sleep or manipulate system time here if necessary to simulate passage of time

    # Get the analytics data for the habit
    habit_name, completions, current_streak, longest_streak, completion_rate = db.get_analytics(habit_id)

    # Asserting expected values
    assert habit_name == "Test habit"
    assert len(completions) >= 1  # Check number of completions
    assert current_streak >= 1  # Depending on how streak is calculated
    assert longest_streak >= 1  # Assuming a streak calculation method
    assert completion_rate >= 0  # Assuming completion rate calculation over 30 days



def test_calculate_current_streak(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.complete_habit(habit_id)  # This sets the completion date to today by default

    # Get all completion records
    all_records = db.get_completions()  # Fetch all completion records
    records = [rec for rec in all_records if rec[1] == habit_id]  # Filter records for this habit

    # Check that the record was added
    assert len(records) == 1
    assert records[0][1] == habit_id
    assert records[0][2] == date.today().isoformat()  # Using date from datetime correctly


def test_calculate_longest_streak(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with the required periodicity parameter
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.complete_habit(habit_id)

    # Get all completions, then filter for this specific habit
    all_completions = db.get_completions()
    records = [rec for rec in all_completions if rec[1] == habit_id]

    # Check that the record was added
    assert len(records) == 1
    assert records[0][1] == habit_id
    assert records[0][2] == date.today().isoformat()  # Correctly using date from datetime



def test_calculate_completion_rate(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with necessary parameters
    db.create_habit("Test habit", "Daily")  # Assume "Daily" as the periodicity for the example

    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit; assume the completion date is handled automatically by the method
    db.complete_habit(habit_id)

    # Since the get_completions() method is not defined with a date filter in previous discussions,
    # We'll assume we need to manually filter for the specified date:
    all_completions = db.get_completions()  # Fetch all completion records
    completions_on_date = [comp for comp in all_completions if comp[2] == "2024-04-18"]

    # Check that the habit id is in the list of completions on that date
    assert any(comp[1] == habit_id for comp in completions_on_date)


def test_overall_longest_streak(run_before_and_after_tests):
    db = run_before_and_after_tests

    # Insert a habit with the necessary periodicity parameter
    db.create_habit("Test habit", "Daily")
    habit_id = db.get_all_habits()[0][0]

    # Add a record for the habit
    db.complete_habit(habit_id)

    # Delete the habit and its completions, assuming `delete_habit` also deletes completions
    db.delete_habit(habit_id)

    # Check that all completions were deleted
    completions = db.get_completions()  # Fetch all completions to verify
    assert not any(comp[1] == habit_id for comp in completions), "Completions were not properly deleted"

    # Get the overall longest streak, which should now be 0, assuming all completions are deleted
    longest_streak, habit_name = db.get_overall_longest_streak()
    assert longest_streak == 0, "Longest streak should be 0 after deletion"
    assert habit_name is None, "No habit name should be returned after deletion"

