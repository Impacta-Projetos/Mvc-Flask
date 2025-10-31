# arquivo reservado para transformar os modelos em um pacote python
from flask_sqlalchemy import SQLAlchemy
banco_de_dados = SQLAlchemy()

from .models_aluno import Aluno
from .models_professor import Professor
from .models_turma import Turma