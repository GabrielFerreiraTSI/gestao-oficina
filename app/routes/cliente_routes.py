from flask import Blueprint, request, jsonify
from app import db
from app.models.cliente import Cliente

cliente_bp = Blueprint('cliente', __name__)

# Criar cliente
@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()

    cliente = Cliente(
        nome=data['nome'],
        email=data['email'],
        telefone=data.get('telefone')
    )

    db.session.add(cliente)
    db.session.commit()

    return jsonify(cliente.to_dict()), 201


# Listar clientes
@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])


# Buscar cliente por ID
@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def buscar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())


# Deletar cliente
@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"message": "Cliente deletado com sucesso"})