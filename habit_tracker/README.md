# Habit Tracker
Habit Tracker is a streamlined tool crafted with Python, embracing the principles of object-oriented design. It offers a convenient means for individuals to monitor their routines and assess their development through time. This tool features a user-friendly graphical interface, engineered with the Tkinter library.

# Core Requirements

The Habit Tracker tool operates optimally with the following:

    Python version 3.8.8 or its equivalents
    Access to the sqlite3 module
    Tkinter, a part of the Python standard collection of libraries

# Getting Started

To embark on your journey with Habit Tracker, adhere to these instructions:

    Confirm the installation of Python version 3.8.8 or similar on your device.
    Download the essential components: database.py, habit.py, main.py, and gui.py. To kickstart with a month's worth of preset routine data, ensure to acquire habit_keeper.db.
    Utilize a terminal or command prompt to navigate to the folder containing the downloaded items.

# Launching the Tool

Initiate the tool with the command below in your terminal or command prompt:

shell

python main.py

Upon execution, the tool's GUI springs to life, presenting options to delve into existing routines or forge new ones.

# Conducting Tests

For test execution, ensure the installation of pytest. Absent in your setup? Install it using:

shell

pip install pytest

To commence testing, utilize:

shell

pytest

For specific test files, the following commands are useful:

shell

pytest test_database.py
pytest test_habit.py

# Crafting a New Routine

Should you opt to create a new routine, proceed as follows:

    Choose the "Create new Habit" button in the primary interface.
    A fresh interface emerges, allowing for the input of the routine's name and the selection of its occurrence frequency from a dropdown (options include: daily, weekly, monthly).
    Hit the "Create" button to establish the routine.
    For routines marked as weekly or monthly, Habit Tracker provides a tailored scheduling feature. Post-clicking "Create", another interface allows for the customization of the routine's recurrence.
    Confirm your settings with the "Confirm" button, followed by a confirmation prompt.
    Close the current window or re-run the main.py to proceed further.

# Exploring Routines and Insights

Back at the welcome screen, selecting "View Habits" lets you:

    Identify routines due for completion today (if applicable).
    Mark a routine as completed by clicking "Complete".
    View a comprehensive list of all routines, including newly added ones, by clicking "View All Routines".
    Filter routines based on frequency with the "Filter by Frequency" option.
    Access insights such as the longest streak and completion rates through the "Analytics" button.
    Each listed routine offers options for deletion, modification, and analytics review.
    Modify routine details using the "Update" feature and confirm changes by clicking again on "Update" (refresh the interface to see updates).
    The "View Analytics" option reveals detailed statistics like the longest and current streaks, along with completion percentages.

# Acknowledgement

Habit Keeper was conceived as an introductory project to acquaint oneself with the nuances of object-oriented programming and GUI crafting in Python. It lays the groundwork for more intricate routine tracking and management solutions.
