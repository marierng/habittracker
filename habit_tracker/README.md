# Habit Tracker

Habit Tracker is a simple application built using Python and object-oriented programming (OOP) concepts. It allows users to track their habits and monitor their progress over time. The application provides a graphical user interface (GUI) created with Tkinter.

## Dependencies

The Habit Tracker application relies on the following dependencies:

- Python 3.8.8 or a compatible version
- sqlite3 module
- Tkinter (included in Python standard library)

## Installation and Setup

To set up and run the Habit Tracker application, follow these steps:

1. Ensure that you have Python 3.8.8 or a compatible version installed on your system.
2. Download all the necessary files: `database.py`, `habit.py`, `main.py`, and `gui.py` (download `habit_tracker.db` for 4 weeks of predefined habit data).
3. Open a terminal or command prompt and navigate to the directory where you downloaded the files.

## Running the Program

To run the application, use the following command in your terminal or command prompt:


    python main.py



The application's GUI window will open, providing options to either view existing habits or create a new habit.

## Running Tests

To run the tests, you would need to have `pytest` installed. If it's not installed, you can install it using the following command:



    pip install pytest
    


Then, to run the tests, use the following command:



    pytest
   


Or use the following command to run a specific test:



    pytest test_database.py
    pytest test_habit.py
    


## Creating a New Habit

If you choose to create a new habit, follow these steps:

1. Select the "Create New Habit" option in the initial window.
2. A new window will open, allowing you to enter the name of the habit and choose its frequency from a drop-down menu (e.g., daily, weekly, monthly).
3. Click the "Create" button to create the habit.
4. For habits with a weekly and monthly frequency, the Habit Tracker app offers a flexible scheduling option. After clicking on the "Create" button, a new window will open, allowing you to customize the habit's recurrence.
5. Click the "Confirm" button. You'll receive a confirmation message displayed upon creation.
6. Close the window or run the `main.py` file again to proceed.

## Viewing Habits and Analytics

After returning to the welcome window and selecting the "View Habits" option, you can:

- View habits that need to be completed on the current day (if any).
- Click on the "Complete" button to complete the habit.
- Click the "View All Habits" button to see a list of all created habits, including the one you just created.
- Click the "Filter by Frequency" button to see a list of habits of the chosen frequency.
- Click the "Analytics" button to see the longest streak, highest completion rate among all habits, and comparison graph.
- For each habit listed, you can delete, update, and view analytics.
- Click the "Update" button to modify the name of the habit and frequency, once completed simply click on the "Update" button (close the window and open it again to see the changes). Note: If the frequency is weekly specify the day with the first letter alone uppercase and for monthly enter a number between 1-31.
- Click the "View Analytics" button to display the habit's longest streak, current streak, and completion rate.
- Please note that if you view the analytics immediately after creating a habit, the values will be zero since there won't be any recorded data yet.

## Acknowledgments

The Habit Tracker application was developed as a learning exercise in object-oriented programming and GUI development using Python. It serves as a starting point for building more complex habit-tracking and management systems.


#### Enjoy using the Habit Tracker application!
