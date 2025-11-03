from pathlib import Path
arquivo_src = Path(__file__).parent / "src"
import sys
sys.path.append(str(arquivo_src))

import os
from flask import Flask
from config.config import Config
from models import banco_res
from flasgger import Swagger
from api.reservas import rotas_reservas

app = Flask(__name__)

app.config.from_object(Config)

banco_res.init_app(app)

swagger = Swagger(app, template_file='docs/swagger.yaml')

@app.route('/')
def index():
    return 'API de Reservas funcionando! A documentação está disponível em: /apidocs'

with app.app_context():
    banco_res.create_all()

rotas_reservas(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host=host, port=port, debug=debug)