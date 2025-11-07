from . import banco_res



class Reservas(banco_res.Model):
    __tablename__ = "reservas"

    id = banco_res.Column(banco_res.Integer, primary_key=True)
    num_sala = banco_res.Column(banco_res.Integer, nullable=False)
    lab = banco_res.Column(banco_res.Boolean, nullable=False)
    data = banco_res.Column(banco_res.Date, nullable=False)
    turma_id = banco_res.Column(banco_res.Integer, nullable=False)

     def __repr__(self):
        return f"<Reserva(id={self.id}, num_sala={self.num_sala}, lab={self.lab}, data={self.data}, turma_id={self.turma_id})>"