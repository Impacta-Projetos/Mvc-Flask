from . import banco_atv

class Atividades(banco_atv.Model):
    __tablename__ = 'atividades'

    id = banco_atv.Column(banco_atv.Integer, primary_key=True)
    nome_atividade = banco_atv.Column(banco_atv.String(50), nullable=False)
    descricao = banco_atv.Column(banco_atv.String(100), nullable=False)
    peso_porcento = banco_atv.Column(banco_atv.Integer, nullable=False)
    data_entrega = banco_atv.Column(banco_atv.DateTime, nullable=False)
    turma_id = banco_atv.Column(banco_atv.Integer, nullable=False)
    professor_id = banco_atv.Column(banco_atv.Integer, nullable=False)

    atividades = banco_atv.relationship('Notas', back_populates='atividade')

    def __repr__(self):
        return f"<Atividade(id={self.id}, nome_atividade='{self.nome_atividade}', descricao='{self.descricao}', peso_porcento={self.peso_porcento}, data_entrega={self.data_entrega}, turma_id={self.turma_id}, professor_id={self.professor_id})>"