from flask import Blueprint, request, jsonify, render_template
from utils.database import db
from models import User, Task
from datetime import datetime
from flask_login import login_required

bonificacion_blueprint = Blueprint('bonificaciones', __name__)

@bonificacion_blueprint.route('/bonificaciones', methods=['GET'])
@login_required
def page_bonificacion():
    tasks = Task.query.all() 
    user_task = {} 

    for task in tasks:
        if task.status_id == 3 and task.estimatetime is not None and task.donetime is not None and task.estimatetime >= task.donetime:
            user = User.query.get(task.user_id)
            if user.id not in user_task:
                user_task[user.id] = {
                    'user': user.first_name + ' ' + user.last_name,
                    'tasks': [],
                    'done_early': 0,
                    'total_bonificacion': 0,
                    'total_dolar': 0,
                    'cycle_done_early': 0,
                    'show_bonus_7': False,
                    'show_bonus_21': False
                }
            
            bonus_percentage = 10 if task.difficulty == 'Easy' else 15 if task.difficulty == 'Medium' else 20
            bonus_dollar = 5 if task.difficulty == 'Easy' else 10 if task.difficulty == 'Medium' else 15
            current_bonus_dollar = bonus_dollar + (bonus_dollar * bonus_percentage / 100)

            user_task[user.id]['done_early'] += 1  
            user_task[user.id]['cycle_done_early'] += 1 
            user_task[user.id]['total_bonificacion'] += bonus_percentage 
            user_task[user.id]['total_dolar'] += current_bonus_dollar 

            user_task[user.id]['tasks'].append({
                'task': task.description,
                'bonificacion': bonus_percentage,
                'dolar': current_bonus_dollar
            })

            if user_task[user.id]['cycle_done_early'] == 7:
                user_task[user.id]['show_bonus_7'] = True
            if user_task[user.id]['cycle_done_early'] == 21:
                user_task[user.id]['show_bonus_21'] = True

    total_general_dolares = sum(user['total_dolar'] for user in user_task.values())

    return render_template('bonificacion.html', user_task=user_task, total_dolares=total_general_dolares)
