from controllers.ctrls_turma import TurmaController

def rotas_turmas(app):
    app.add_url_rule('/turmas', view_func=TurmaController.listar_turmas, methods=['GET'])
    app.add_url_rule('/turmas/<int:turma_id>', view_func=TurmaController.buscar_turma, methods=['GET'])
    app.add_url_rule('/turmas', view_func=TurmaController.criar_turma, methods=['POST'])
    app.add_url_rule('/turmas/<int:turma_id>', view_func=TurmaController.atualizar_turma, methods=['PUT'])
    app.add_url_rule('/turmas/<int:turma_id>', view_func=TurmaController.deletar_turma, methods=['DELETE'])