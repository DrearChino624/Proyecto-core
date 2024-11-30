from flask import Blueprint, render_template
from flask_login import login_required
from models import Task, User, Status
from utils.database import db

# Crear blueprint para este controlador
user_status_blueprint = Blueprint('user_status', __name__)

@user_status_blueprint.route('/user_status', methods=['GET'])
@login_required
def user_status():
    # Obtener las tareas junto con los usuarios asignados
    tasks = Task.query.join(User, Task.user_id == User.id).add_columns(
        Task.description, Task.difficulty, Task.status_id, Task.donetime, User.first_name
    ).all()

    # Obtener las descripciones de los status
    statuses = {status.id: status.status_description for status in Status.query.all()}

    # Crear un contenedor para las tareas procesadas
    processed_tasks = []

    for task in tasks:
        task_data = {
            'first_name': task.first_name,
            'description': task.description,
            'difficulty': task.difficulty,
            'status_description': statuses.get(task.status_id, 'Unknown'),  # Usar el status description
            'penalty_or_bonus': 'Tarea en progreso' if task.status_id != 3 else 'N/A'
        }

        if task_data['status_description'] == 'Completed' and task.donetime is not None:
            # Verifica si estimatetime existe en el task
            if hasattr(task, 'estimatetime') and task.estimatetime is not None:
                if task.donetime < task.estimatetime:
                    task_data['penalty_or_bonus'] = "Bonificación"
                elif task.donetime > task.estimatetime:
                    task_data['penalty_or_bonus'] = "Penalización"
                else:
                    task_data['penalty_or_bonus'] = "Sin Penalización/Boni."
            else:
                task_data['penalty_or_bonus'] = "Sin Estimación de Tiempo"


        processed_tasks.append(task_data)

    # Aquí continúa el resto de tu lógica (si tienes más cosas)
    # Renderizar la vista de 'Estados de Usuarios' con las tareas procesadas
    return render_template('user_status.html', tasks=processed_tasks)
