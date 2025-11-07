from . import banco_de_dados

# inicializa a classe turma que herda de database.Model, se tornando uma tabela dentro do banco de dados.
class Turma(banco_de_dados.Model):

    __tablename__ = 'turmas'
    # definindo as colunas de turma dentro da tabela
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    descricao = banco_de_dados.Column(banco_de_dados.String(100), nullable=False)
    professor_id = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('professores.id'), nullable=False)
    ativo = banco_de_dados.Column(banco_de_dados.Boolean, default=True)
    
    alunos = banco_de_dados.relationship('Aluno', back_populates='turma')
    professor = banco_de_dados.relationship('Professor', back_populates='turmas')