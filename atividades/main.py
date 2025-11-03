from pathlib import Path
arquivo_src = Path(__file__).parent / "src"
import sys
sys.path.append(str(arquivo_src))

import os
from flask import Flask
from config.config import Config
from src.models import banco_atv
from flasgger import Swagger
from src.api.atividades.api_atividades import rotas_atividades
from src.api.notas.api_notas import rotas_notas

app = Flask(__name__)
app.config.from_object(Config)

banco_atv.init_app(app)

swagger = Swagger(app, template_file='docs/swagger.yaml')

@app.route('/')
def index():
    return 'API de Atividades funcionando! A documentação está disponível em: /apidocs'

with app.app_context():
    banco_atv.create_all()

rotas_atividades(app)
rotas_notas(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host=host, port=port, debug=debug)