from flask import Flask, request, jsonify
from task import Task, PersonalTask, WorkTask
from task_manager import TaskManager
from datetime import datetime, date
from Controllers.TaskController import TaskController as task_controller



app = Flask(__name__)
task_manager = TaskManager()

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    return task_controller.create_task(data)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        task_type = request.args.get('type')
        tasks = task_manager.list_tasks()
        
        if task_type:
            # Filter tasks by type if specified
            tasks = [task for task in tasks if task[5] == task_type]
            
        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.load_from_db(task_id)
        if task:
            return jsonify({'task': str(task)}), 200
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No update data provided'}), 400

        # Get existing task
        task = Task.load_from_db(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Update description if provided
        if 'description' in data:
            Task.update_in_db(data['description'], task.status, task_id)
            return jsonify({'message': 'Task updated successfully'}), 200

        return jsonify({'error': 'No valid update fields provided'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        result = Task.delete_from_db(task_id)
        if 'not found' in result.lower():
            return jsonify({'error': result}), 404
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    try:
        pending_tasks = task_manager.get_pending_tasks()
        return jsonify({'pending_tasks': pending_tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    try:
        overdue_tasks = task_manager.get_overdue_tasks()
        return jsonify({'overdue_tasks': overdue_tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5000)

