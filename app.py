from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    status = db.Column(db.String(50))

# Criar banco
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "API com SQLite 🚀"

@app.route('/tarefas', methods=['GET'])
def listar():
    tarefas = Tarefa.query.all()
    return jsonify([
        {"id": t.id, "nome": t.nome, "status": t.status}
        for t in tarefas
    ])

@app.route('/tarefas', methods=['POST'])
def adicionar():
    data = request.json
    nova = Tarefa(nome=data['nome'], status=data['status'])
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Tarefa salva no banco"}), 201

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar(id):
    data = request.json
    tarefa = Tarefa.query.get(id)

    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    tarefa.nome = data.get('nome', tarefa.nome)
    tarefa.status = data.get('status', tarefa.status)

    db.session.commit()

    return jsonify({"mensagem": "Tarefa atualizada"})

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar(id):
    tarefa = Tarefa.query.get(id)

    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"mensagem": "Tarefa deletada"})

if __name__ == '__main__':
    app.run(debug=True)