#!/usr/bin/env python
# coding: utf-8

# # Habit Tracker
# ## Creating the Main Application

# In[1]:


from database import HabitTrackerDB
from habit import Habit
from gui import HabitTrackerGUI


# In[2]:


# Create an instance of the GUI class and run the application
habit_tracker_gui = HabitTrackerGUI()
habit_tracker_gui.run()

