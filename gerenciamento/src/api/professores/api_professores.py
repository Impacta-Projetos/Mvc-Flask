from controllers.ctrls_professores import ProfessorController

def rotas_professores(app):
    app.add_url_rule('/professores', view_func=ProfessorController.listar_professores, methods=['GET'])
    app.add_url_rule('/professores/<int:professor_id>', view_func=ProfessorController.buscar_professor, methods=['GET'])
    app.add_url_rule('/professores', view_func=ProfessorController.criar_professor, methods=['POST'])
    app.add_url_rule('/professores/<int:professor_id>', view_func=ProfessorController.atualizar_professor, methods=['PUT'])
    app.add_url_rule('/professores/<int:professor_id>', view_func=ProfessorController.deletar_professor, methods=['DELETE'])