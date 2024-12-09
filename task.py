
import sqlite3

class Task:
    
    _task_id = 1

    def __init__(self, title, due_date, description=None):
        self._task_id = Task._task_id
        Task._task_id+= 1
        self.title = title
        self.due_date = due_date
        self._description = None
        self.status = "pending"
        self.flag = None

#Initializing the database and creating a table
    def initialize_database():
        conn=sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                       (task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT ,
                       due_date TEXT,
                       description TEXT,
                       status TEXT,
                       flag TEXT)''')
        conn.commit()
        conn.close()


    def mark_completed(self):
        self.status = "completed"

    def get_task_id(self):
        return Task._task_id
    
    def set_task_id(self,task_id):
        Task._task_id=task_id
        

    def get_description(self):
        return self._description

   
    def set_description(self, description):
        if len(description) > 15:
            raise ValueError("Description exceeds 15 characters.")
        self._description = description

    def save_to_db(self):
        """Save the current task to the database."""
        conn=sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, due_date, description, status, flag) VALUES (?, ?, ?, ?, ?)', 
                       (self.title, self.due_date, self._description, self.status, self.flag))
        conn.commit()
        cursor.close()
        conn.close()

#Load all tasks from database
    
    def load_from_db(task_id):
        conn=sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        task = cursor.fetchone()
        if task:
            return task
#update

    def update_in_db(description_set,status_set,task_id):
        connection=sqlite3.connect('tasks.db')
        cursor=connection.cursor()
        cursor.execute(''' UPDATE tasks SET title = ? , status= ? WHERE task_id= ?''',(description_set,status_set,task_id))
        connection.commit()
        cursor.close()
        connection.close()
        return f'The task with ID {task_id} has been updated successfully'


    def delete_from_db(task_id):
        connection=sqlite3.connect('tasks.db')
        cursor=connection.cursor()
        cursor.execute('''SELECT * FROM tasks WHERE task_id = ?''', (task_id,))
        row=cursor.fetchone()
        if row is None:
            return 'Task ID not found'
        cursor.execute('DELETE FROM tasks WHERE task_id= ?',(task_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return f'The task with ID {task_id} has been deleted successfully'

    def __str__(self):
        return f"Task ID: {self._task_id}, Title: {self.title}, Due: {self.due_date}, Status: {self.status}"


class PersonalTask(Task):
    def __init__(self, title, due_date, description=None, priority="low"):
        super().__init__(title, due_date, description)
        self.priority = priority


    def set_priority(self, priority):
        if priority in ["high", "medium", "low"]:
            self.priority = priority
        else:
            print("Invalid priority value. Use 'high', 'medium', or 'low'.")

    def is_high_priority(self):
        return self.priority=='high'
    
    def __str__(self):
        return super().__str__() + f", Priority: {self.priority}"


class WorkTask(Task):
    def __init__(self, title, due_date, description=None, team_members=None):
        super().__init__(title, due_date, description)
        self.team_members = team_members if team_members else []


    def add_team_member(self,member):
        if member:
            self.team_members.append(member)
        else:
            print("Invalid team member name.")

    def __str__(self):
        return super().__str__() + f", Team Members: {', '.join(self.team_members)}"
    
#Example 
Task.initialize_database()
task=Task('Do preset','2024-12-20')
task.set_description('Python prs')
task.save_to_db()

#Example of loading data from db
task=Task.load_from_db(2)
print(task)

task=Task.update_in_db('Python Task','In Progress',2)
print(task)

task=Task.delete_from_db(2)
print(task)