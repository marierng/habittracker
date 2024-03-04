# Daily Habit Manager

Daily Habit Manager is a versatile tool engineered to assist individuals in monitoring and sustaining their daily routines. Developed with Python, this application leverages the principles of object-oriented programming (OOP) to offer a structured and efficient habit management system. It features a graphical user interface (GUI) powered by Tkinter, providing an intuitive and user-friendly experience.
Core Dependencies

# This application is built upon several key dependencies:

Python 3.8.8 or later
The sqlite3 library for database management
Tkinter, which is part of the Python standard library for GUI creation

# Getting Started

To begin using the Daily Habit Manager, please follow these setup instructions:

Confirm the installation of Python 3.8.8 or a later version on your machine.
Download the required files: habitracker.py
Use a terminal or command prompt to navigate to the folder containing the downloaded files.

# Launching the Application

Execute the application by typing the command below in your terminal or command line:

bash

python habittracker.py

Upon execution, the application's main GUI window will appear, presenting options to either view current habits or add new ones.
# Testing

For testing purposes, ensure pytest is installed. If not, you can install it using: pip install pytest
To execute the tests, run:

pytest
Or to target specific tests:

pytest test_database.py pytest test_habit.py
Adding a New Habit

# To add a new habit:

Choose "Create New Habit" from the main window.
In the subsequent window, input the habit's name and set its frequency (daily, weekly, monthly) via the dropdown menu.
Press "Create" to save the habit.
For weekly or monthly habits, a further customization window will appear post-creation for detailed scheduling. 
(For weekly habits, a dropdown menu will appear where you can select all weekdays when you want your habit to appear; 
for a monthly habit, simply type in a number between 1 and 31 to speciy the date when your habit should be appear).
Confirm your settings with the "Confirm" button, and a success message will be shown.
You may close the window or re-run habittracker.py to continue.

# Habit Insights and Management

From the main window, selecting "View Habits" allows you to:

Check off today's habits as done.
Access a comprehensive list of all habits, including recent additions.
Utilize the "Filter by Frequency" feature to sort habits by their recurrence rate.
Use the "Analytics" feature for in-depth habit analysis, including streaks and completion rates.
Modify or remove habits as needed, with immediate changes reflected upon window refresh.
Update habit details or review analytical insights for each habit listed.

# Credits
I hope you find the Habit Manager both useful and insightful!
