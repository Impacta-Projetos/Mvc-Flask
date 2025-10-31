# criando uma pathlib para facilitar o uso em outros sistemas operacionais
from pathlib import Path
arquivo_src = Path(__file__).parent / "src"
import sys
sys.path.append(str(arquivo_src))

import os
from flask import Flask
from config.config import Config
from models import banco_de_dados
from flasgger import Swagger
from api.professores.api_professores import rotas_professores
from api.turma.api_turma import rotas_turmas
from api.aluno.api_alunos import rotas_aluno

app = Flask(__name__)
app.config.from_object(Config)

banco_de_dados.init_app(app)

swagger = Swagger(app, template_file='docs/swagger.yaml')

@app.route('/')
def index():
    return 'API de Gerenciamento Escolar funcionando! A documentação está disponível em: /apidocs'

with app.app_context():
    banco_de_dados.create_all()

rotas_professores(app)
rotas_turmas(app)
rotas_aluno(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host=host, port=port, debug=debug)