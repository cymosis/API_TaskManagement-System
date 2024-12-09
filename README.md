# Task Management System

This project implements a simple task management system in Python with three main modules:
1. `task.py`: Defines task-related classes.
2. `task_manager.py`: Manages tasks and file operations.
3. `interface.py`: Provides a console-based user interface.

## Features
1. ## task.py
- To add, view, and delete a tasks.
- Handle both personal and work tasks.

2. ## task_manager.py
- Add, view, and delete tasks.
- Get overall view of tasks.
- Save tasks to and load tasks from a CSV file.
- Filter tasks by status or type.

3. ## interface.py
- View different routes to show data displays.


## Setup Instructions
1. Ensure Python 3 is installed on your system with depencies flask installed with importng the classes and subclasses.
2. Save all project files in the same directory.
3. Run `interface.py` using the command: `python interface.py`.

## Class and Method Descriptions
Detailed descriptions of the classes and methods are in the code comments.


### Methods
        The main class responsible for handling task operations.
        Creates a new task in the database.
        - **Parameters:**
        - `data` (dict): Task data containing title, description, due_date, and status
        - **Returns:** Newly created task object
        - **Example:**
        ```python
        task_data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": "2024-12-31",
            "status": "pending"
        }
        #Create task
        task = task_manager.create_task(task_data)
        # Get all tasks
        all_tasks = task_manager.get_all_tasks()

        # Get filtered tasks
        filtered_tasks = task_manager.get_all_tasks({"status": "pending"})
        task = task_manager.get_task_by_id(1)
        updated_data = {"status": "completed"}
        task = task_manager.update_task(1, updated_data)
        task = Task(title="Test", description="Description", due_date="2024-12-31")
        is_valid, error = task.validate()

## Error Handling
1.Validation Errors (400 Bad Request)
    Missing required fields
    Invalid data formats
    Invalid status values
2.Resource Not Found (404 Not Found)
    Task ID doesn't exist
3.Database Errors (500 Internal Server Error)
    Connection issues
    Query execution failures
    This documentation provides detailed information about the classes, methods, and error handling in the Task Management System. It includes practical examples and explains how the system handles various error scenarios.

# Examples of implementation
- Prevents adding descriptions longer than 15 characters.
- Handles file not found errors when loading tasks.
- Ensures valid task types and priorities are selected.


