from flask import render_template, request, Blueprint
from models import Task, User
from utils.database import db
from flask_login import login_required

user_report_blueprint = Blueprint('user_reports', __name__)

@user_report_blueprint.route('/user_reports', methods=['GET'])
@login_required
def user_report():
    user_id = request.args.get('user_id')  

    users = User.query.filter_by(role='ROLE_USER').all()

    tasks = []
    if user_id:
        tasks = Task.query.filter_by(user_id=user_id).all()

    total_bonus = 0
    total_penalty = 0
    completed_tasks = 0
    pending_tasks = 0
    in_progress_tasks = 0
    completed_early = 0
    completed_late = 0

    for task in tasks:
        if task.donetime: 
            if task.donetime <= task.estimatetime:
                total_bonus += (task.estimatetime - task.donetime) 
                completed_early += 1
            else:
                total_penalty += (task.donetime - task.estimatetime) 
                completed_late += 1

        if task.status_id == 1: 
            pending_tasks += 1
        elif task.status_id == 2: 
            in_progress_tasks += 1
        else:
            completed_tasks += 1

    total = total_bonus - total_penalty 
    user = User.query.get(user_id) if user_id else None  

    return render_template('user_reports.html', users=users, user=user, tasks=tasks,
                           completed_tasks=completed_tasks, pending_tasks=pending_tasks,
                           in_progress_tasks=in_progress_tasks, completed_early=completed_early,
                           completed_late=completed_late, total_bonus=total_bonus,
                           total_penalty=total_penalty, total=total)
