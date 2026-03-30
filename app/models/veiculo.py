from app import db

class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(20), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    ordens_servico = db.relationship('OrdemServico', backref='veiculo', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "placa": self.placa,
            "cliente": {
                "id": self.cliente.id,
                "nome": self.cliente.nome
            } if self.cliente else None
        }