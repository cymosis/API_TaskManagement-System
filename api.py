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
    get_tasks=task_controller.get_tasks()
    return get_tasks

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    indiv_task=task_controller.specific_task(task_id)
    return indiv_task


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    update=task_controller.update_task(task_id)
    return update

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    deleted_atask=task_controller.delete_task(task_id)
    return delete_task

@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    pending=task_controller.pending_tasks()
    return pending

@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    overdue=task_controller.overdue_tasks()
    return overdue

if __name__ == '__main__':
    app.run(debug=True,port=5000)

