from controllers.ctrls_atividades import AtividadesController

def rotas_atividades(app):
    app.add_url_rule('/atividades', view_func=AtividadesController.listar_atividades, methods=['GET'])
    app.add_url_rule('/atividades/<int:atividade_id>', view_func=AtividadesController.buscar_atividade, methods=['GET'])
    app.add_url_rule('/atividades', view_func=AtividadesController.criar_atividade, methods=['POST'])
    app.add_url_rule('/atividades/<int:atividade_id>', view_func=AtividadesController.atualizar_atividade, methods=['PUT'])
    app.add_url_rule('/atividades/<int:atividade_id>', view_func=AtividadesController.deletar_atividade, methods=['DELETE'])