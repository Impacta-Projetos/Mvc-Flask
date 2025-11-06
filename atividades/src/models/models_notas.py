from . import banco_atv

class Notas(banco_atv.Model):
    __tablename__ = "notas"
    #TODO: Implementar - id, nota, aluno_id, atividade_id
    id = banco_atv.Column(banco_atv.Integer, primary_key=True)
    nota = banco_atv.Column(banco_atv.Float, nullable=False)
    aluno_id = banco_atv.Column(banco_atv.Integer, nullable=False)
    atividade_id = banco_atv.Column(banco_atv.Integer, banco_atv.ForeignKey('atividades.id'), nullable=False)

    atividade = banco_atv.relationship('Atividades', back_populates='atividades')

    def __repr__(self):
        return f"<Nota(id={self.id}, nota={self.nota}, aluno_id={self.aluno_id}, atividade_id={self.atividade_id})>"
    