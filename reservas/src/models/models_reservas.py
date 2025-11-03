from . import banco_res

class Reservas(banco_res.Model):
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    num_sala = banco_de_dados.Column(banco_de_dados.Integer, nullable=False)
    lab = banco_de_dados.Column(banco_de_dados.Boolean, nullable=False)
    data = banco_de_dados.Column(banco_de_dados.Date, nullable=False)
    turma_id = banco_atv.Column(banco_atv.Integer, nullable=False)