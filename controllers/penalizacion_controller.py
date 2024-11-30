from flask import Blueprint, request, jsonify, render_template
from utils.database import db
from models import User, Task
from datetime import datetime
from flask_login import login_required

penalizacion_blueprint = Blueprint('penalizaciones', __name__)

@penalizacion_blueprint.route('/penalizaciones', methods=['GET'])
@login_required
def page_penalizacion():
    tasks = Task.query.all()
    user_task = {}

    for task in tasks:
        if task.status_id == 3 and task.estimatetime and task.donetime and task.donetime > task.estimatetime:
            user = User.query.get(task.user_id)
            if user.id not in user_task:
                user_task[user.id] = {
                    'user': user.first_name + ' ' + user.last_name,
                    'tasks': [],
                    'delayed': 0,
                    'total_penalizacion': 0,
                    'total_dolar': 0,
                }

            penalty_percentage = 5 if task.difficulty == 'Easy' else 10 if task.difficulty == 'Medium' else 15
            penalty_dollar = 5 if task.difficulty == 'Easy' else 10 if task.difficulty == 'Medium' else 15
            current_penalty_dollar = penalty_dollar + (penalty_dollar * penalty_percentage / 100)

            user_task[user.id]['delayed'] += 1
            user_task[user.id]['total_penalizacion'] += penalty_percentage
            user_task[user.id]['total_dolar'] += current_penalty_dollar

            user_task[user.id]['tasks'].append({
                'task': task.description,
                'penalizacion':penalty_percentage,
                'dolar':current_penalty_dollar
            })

    total_general_dolares = sum(user['total_dolar'] for user in user_task.values())

    return render_template('penalizacion.html', user_task=user_task, total_dolares=total_general_dolares)
