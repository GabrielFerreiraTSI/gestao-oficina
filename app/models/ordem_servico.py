from datetime import datetime
from app import db

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendente')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "cliente": {
                "id": self.cliente.id,
                "nome": self.cliente.nome
            } if self.cliente else None,
            "veiculo": {
                "id": self.veiculo.id,
                "modelo": self.veiculo.modelo,
                "placa": self.veiculo.placa
            } if self.veiculo else None
        }