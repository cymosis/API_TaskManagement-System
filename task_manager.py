from datetime import date, datetime
import sqlite3
from task import Task,PersonalTask

import pandas as pd
import csv

class TaskManager:
    def __init__(self, db_file='tasks.db'):
        self.db_file = db_file
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                       (task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT,
                       due_date TEXT,
                       description TEXT,
                       status TEXT,
                       task_type TEXT,
                       priority TEXT,
                       team_members TEXT)''')
            conn.commit()

    def add_task(self, task):
        """Add a task to the database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            if isinstance(task, PersonalTask):
                cursor.execute(
                    'INSERT INTO tasks (title, due_date, description, status, task_type, priority) VALUES (?, ?, ?, ?, ?, ?)',
                    (task.title, task.due_date, task._description, task.status, 'personal', task.priority)
                )
            else:  # WorkTask
                cursor.execute(
                    'INSERT INTO tasks (title, due_date, description, status, task_type, team_members) VALUES (?, ?, ?, ?, ?, ?)',
                    (task.title, task.due_date, task._description, task.status, 'work', ','.join(task.team_members))
                )
            conn.commit()
            return cursor.lastrowid

    def delete_task(self, task_id):
        """Delete a task from the database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
            if not cursor.fetchone():
                return f'Task with ID {task_id} not found'
            
            cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
            conn.commit()
            return f'Task with ID {task_id} deleted successfully'

    def list_tasks(self, task_type=None):
        """List all tasks, optionally filtered by type"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            if task_type:
                cursor.execute("SELECT * FROM tasks WHERE task_type = ?", (task_type,))
            else:
                cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            
            # Convert to list of dictionaries for better JSON serialization
            columns = ['task_id', 'title', 'due_date', 'description', 'status', 'task_type', 'priority', 'team_members']
            return [dict(zip(columns, task)) for task in tasks]

    def get_task(self, task_id):
        """Get a specific task by ID"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            task = cursor.fetchone()
            if task:
                columns = ['task_id', 'title', 'due_date', 'description', 'status', 'task_type', 'priority', 'team_members']
                return dict(zip(columns, task))
            return None

    def update_task(self, task_id, updates):
        """Update task details"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Check if task exists
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            if not cursor.fetchone():
                return False

            # Build update query dynamically based on provided fields
            valid_fields = {'title', 'due_date', 'description', 'status', 'priority', 'team_members'}
            update_fields = []
            values = []
            
            for field, value in updates.items():
                if field in valid_fields:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
                
            values.append(task_id)
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = ?"
            cursor.execute(query, values)
            conn.commit()
            return True

    def get_pending_tasks(self):
        """Get all pending tasks"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = 'pending'")
            tasks = cursor.fetchall()
            columns = ['task_id', 'title', 'due_date', 'description', 'status', 'task_type', 'priority', 'team_members']
            return [dict(zip(columns, task)) for task in tasks]

    def get_overdue_tasks(self):
        """Get all overdue tasks"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            
            columns = ['task_id', 'title', 'due_date', 'description', 'status', 'task_type', 'priority', 'team_members']
            all_tasks = [dict(zip(columns, task)) for task in tasks]
            
            today = date.today()
            return [
                task for task in all_tasks 
                if datetime.strptime(task['due_date'], "%Y-%m-%d").date() < today
            ]

    def load_task(self, file_name="task_list.csv"):
        """Load tasks from CSV file"""
        try:
            df = pd.read_csv(file_name)
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                for _, row in df.iterrows():
                    cursor.execute(
                        'INSERT INTO tasks (title, description, due_date, status, task_type) VALUES (?, ?, ?, ?, ?)',
                        (row["Title"], row["Description"], row["Due Date"], row["Status"], row["Task Type"])
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return False

    def save_task(self, filename="all_task_list.csv"):
        """Save tasks to CSV file"""
        try:
            df = pd.DataFrame(self.db_file)
            df.to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False

TaskManager.save_task('all_task_list.csv')