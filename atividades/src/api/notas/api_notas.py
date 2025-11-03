from controllers.ctrls_notas import NotasController

def rotas_notas(app):
    #TODO: definir as rotas para o recurso notas
    app.add_url_rule('/notas', view_func=NotasController.listar_notas, methods=['GET'])
    app.add_url_rule('/notas/<int:nota_id>', view_func=NotasController.buscar_nota, methods=['GET'])
    app.add_url_rule('/notas', view_func=NotasController.criar_nota, methods=['POST'])
    app.add_url_rule('/notas/<int:nota_id>', view_func=NotasController.atualizar_nota, methods=['PUT'])
    app.add_url_rule('/notas/<int:nota_id>', view_func=NotasController.deletar_nota, methods=['DELETE'])

