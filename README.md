# Task Management System

This project implements a simple task management system in Python with three main modules:
1. `task.py`: Defines task-related classes.
2. `task_manager.py`: Manages tasks and file operations.
3. `interface.py`: Provides a console-based user interface.

## Features
1. ## task.py
- To add, view, and delete tasks.
- Save tasks to and load tasks from a CSV file.
- Filter tasks by status or type.
- Handle both personal and work tasks.


- Add, view, and delete tasks.
- Save tasks to and load tasks from a CSV file.
- Filter tasks by status or type.
- Handle both personal and work tasks.

## Setup Instructions
1. Ensure Python 3 is installed on your system.
2. Save all project files in the same directory.
3. Run `interface.py` using the command: `python interface.py`.

## Class and Method Descriptions
Detailed descriptions of the classes and methods are in the code comments.

## Error Handling
- Prevents adding descriptions longer than 15 characters.
- Handles file not found errors when loading tasks.
- Ensures valid task types and priorities are selected.
