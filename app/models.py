from app import db

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    status = db.Column(db.String(50))