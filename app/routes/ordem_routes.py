from flask import Blueprint, request, jsonify
from app import db
from app.models.ordem_servico import OrdemServico
from app.models.cliente import Cliente
from app.models.veiculo import Veiculo

ordem_bp = Blueprint('ordem', __name__)

@ordem_bp.route('/ordens', methods=['POST'])
def criar_ordem():
    data = request.get_json()

    cliente = Cliente.query.get(data.get('cliente_id'))
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    veiculo = Veiculo.query.get(data.get('veiculo_id'))
    if not veiculo:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    if veiculo.cliente_id != cliente.id:
        return jsonify({"erro": "O veículo não pertence a este cliente"}), 400

    ordem = OrdemServico(
        descricao=data['descricao'],
        status=data.get('status', 'pendente'),
        cliente_id=cliente.id,
        veiculo_id=veiculo.id
    )

    db.session.add(ordem)
    db.session.commit()

    return jsonify(ordem.to_dict()), 201


@ordem_bp.route('/ordens', methods=['GET'])
def listar_ordens():
    status = request.args.get('status')

    query = OrdemServico.query

    if status:
        query = query.filter_by(status=status)

    ordens = query.all()
    return jsonify([o.to_dict() for o in ordens])


@ordem_bp.route('/ordens/<int:id>', methods=['GET'])
def buscar_ordem(id):
    ordem = OrdemServico.query.get_or_404(id)
    return jsonify(ordem.to_dict())


@ordem_bp.route('/clientes/<int:cliente_id>/ordens', methods=['GET'])
def listar_ordens_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify([ordem.to_dict() for ordem in cliente.ordens_servico])


@ordem_bp.route('/ordens/<int:id>', methods=['PUT'])
def atualizar_ordem(id):
    ordem = OrdemServico.query.get_or_404(id)
    data = request.get_json()

    if 'descricao' in data:
        ordem.descricao = data['descricao']

    if 'status' in data:
        ordem.status = data['status']

    if 'cliente_id' in data or 'veiculo_id' in data:
        novo_cliente_id = data.get('cliente_id', ordem.cliente_id)
        novo_veiculo_id = data.get('veiculo_id', ordem.veiculo_id)

        cliente = Cliente.query.get(novo_cliente_id)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        veiculo = Veiculo.query.get(novo_veiculo_id)
        if not veiculo:
            return jsonify({"erro": "Veículo não encontrado"}), 404

        if veiculo.cliente_id != cliente.id:
            return jsonify({"erro": "O veículo não pertence a este cliente"}), 400

        ordem.cliente_id = novo_cliente_id
        ordem.veiculo_id = novo_veiculo_id

    db.session.commit()
    return jsonify(ordem.to_dict())


@ordem_bp.route('/ordens/<int:id>', methods=['DELETE'])
def deletar_ordem(id):
    ordem = OrdemServico.query.get_or_404(id)

    db.session.delete(ordem)
    db.session.commit()

    return jsonify({"message": "Ordem de serviço deletada com sucesso"})