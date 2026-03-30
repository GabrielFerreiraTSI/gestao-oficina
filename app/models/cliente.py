from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))

    veiculos = db.relationship('Veiculo', backref='cliente', lazy=True)
    ordens_servico = db.relationship('OrdemServico', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "veiculos": [
                {
                    "id": v.id,
                    "modelo": v.modelo,
                    "placa": v.placa
                }
                for v in self.veiculos
            ]
        }