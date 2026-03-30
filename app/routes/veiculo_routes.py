from flask import Blueprint, request, jsonify
from app import db
from app.models.veiculo import Veiculo
from app.models.cliente import Cliente

veiculo_bp = Blueprint('veiculo', __name__)

@veiculo_bp.route('/veiculos', methods=['POST'])
def criar_veiculo():
    data = request.get_json()

    cliente_id = data.get('cliente_id')
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    veiculo = Veiculo(
        modelo=data['modelo'],
        placa=data['placa'],
        cliente_id=cliente_id
    )

    db.session.add(veiculo)
    db.session.commit()

    return jsonify(veiculo.to_dict()), 201


@veiculo_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return jsonify([v.to_dict() for v in veiculos])


@veiculo_bp.route('/veiculos/<int:id>', methods=['GET'])
def buscar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    return jsonify(veiculo.to_dict())


@veiculo_bp.route('/clientes/<int:cliente_id>/veiculos', methods=['GET'])
def listar_veiculos_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify([veiculo.to_dict() for veiculo in cliente.veiculos])


@veiculo_bp.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    data = request.get_json()

    veiculo.modelo = data.get('modelo', veiculo.modelo)
    veiculo.placa = data.get('placa', veiculo.placa)

    if 'cliente_id' in data:
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404
        veiculo.cliente_id = data['cliente_id']

    db.session.commit()

    return jsonify(veiculo.to_dict())


@veiculo_bp.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)

    db.session.delete(veiculo)
    db.session.commit()

    return jsonify({"message": "Veículo deletado com sucesso"})