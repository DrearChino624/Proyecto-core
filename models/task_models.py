from utils.database import db
from flask_login import UserMixin
from datetime import datetime, timedelta

class Task(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.relationship('User', backref='tasks')
    description = db.Column(db.String(50))
    difficulty = db.Column(db.String(50))
    estimatetime = db.Column(db.Integer)  # Integer, en minutos o segundos
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), default=1)
    donetime = db.Column(db.Integer, nullable=True)  # Integer, en minutos o segundos

    status = db.relationship('Status', backref='tasks')  

    def serialize(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "user_id": self.user_id,
            "description": self.description,
            "difficulty": self.difficulty,
            "estimatetime": self.estimatetime,
            "status_id": self.status_id,
            "donetime": self.donetime
        }

    # Método para verificar si la tarea ha sido completada a tiempo
    def is_done_on_time(self):
        if self.estimatetime is not None and self.donetime is not None:
            # Convertir los tiempos a timedelta si estimatetime y donetime son en minutos
            estimated_time = timedelta(minutes=self.estimatetime)
            done_time = timedelta(minutes=self.donetime)
            # Comparar si el tiempo de finalización está dentro del tiempo estimado
            return done_time <= estimated_time
        return False
