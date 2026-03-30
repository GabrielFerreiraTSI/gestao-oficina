from flask import Blueprint, request, jsonify
from app import db
from app.models import Tarefa

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "API estruturada 🚀"

@main.route('/tarefas', methods=['GET'])
def listar():
    tarefas = Tarefa.query.all()
    return jsonify([
        {"id": t.id, "nome": t.nome, "status": t.status}
        for t in tarefas
    ])

@main.route('/tarefas', methods=['POST'])
def adicionar():
    data = request.json
    nova = Tarefa(nome=data['nome'], status=data['status'])
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa criada"}), 201

@main.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar(id):
    tarefa = Tarefa.query.get(id)

    if not tarefa:
        return jsonify({"erro": "Não encontrada"}), 404

    data = request.json
    tarefa.nome = data.get('nome', tarefa.nome)
    tarefa.status = data.get('status', tarefa.status)

    db.session.commit()
    return jsonify({"mensagem": "Atualizada"})

@main.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar(id):
    tarefa = Tarefa.query.get(id)

    if not tarefa:
        return jsonify({"erro": "Não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"mensagem": "Deletada"})