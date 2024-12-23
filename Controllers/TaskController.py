from task import Task, PersonalTask, WorkTask
from task_manager import TaskManager
from flask import Flask,jsonify

class TaskController:
    def __init__(self,task,taskmanager):
        self.task=task
        self.taskmanager=taskmanager

    def create_task(data):
        try:
            # Validate required fields
            required_fields = ['type', 'title', 'due_date']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            # Create appropriate task type
            task_type = data['type'].lower()
            if task_type == 'personal':
                task = PersonalTask(
                    title=data['title'],
                    due_date=data['due_date'],
                    description=data.get('description'),
                    priority=data.get('priority', 'low')
                )
            elif task_type == 'work':
                task = WorkTask(
                    title=data['title'],
                    due_date=data['due_date'],
                    description=data.get('description')
                )
                # Add team members if provided
                if 'team_members' in data:
                    for member in data['team_members']:
                        task.add_team_member(member)
            else:
                return jsonify({'error': 'Invalid task type. Must be "personal" or "work"'}), 400

            # Save task to database
            task_id=task.save_to_db()
            return jsonify({'message': 'Task created successfully','task id':task_id}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 400



