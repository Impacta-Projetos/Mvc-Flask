from . import banco_de_dados

# inicializa a classe professor que herda de database.Model, se tornando uma tabela dentro do banco de dados.
class Professor(banco_de_dados.Model):

    __tablename__ = 'professores'
    # definindo as colunas de professor dentro da tabela
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    nome = banco_de_dados.Column(banco_de_dados.String(100), nullable=False)
    idade = banco_de_dados.Column(banco_de_dados.Integer, nullable=False)
    materia = banco_de_dados.Column(banco_de_dados.String(100), nullable=False)
    observacoes = banco_de_dados.Column(banco_de_dados.Text, nullable=True)

    turmas = banco_de_dados.relationship('Turma', back_populates='professor')