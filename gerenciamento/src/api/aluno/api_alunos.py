from controllers.ctrls_aluno import AlunoController

def rotas_aluno(app):
    app.add_url_rule('/alunos', view_func=AlunoController.listar_alunos, methods=['GET'])
    app.add_url_rule('/alunos/<int:aluno_id>', view_func=AlunoController.buscar_aluno, methods=['GET'])
    app.add_url_rule('/alunos', view_func=AlunoController.criar_aluno, methods=['POST'])
    app.add_url_rule('/alunos/<int:aluno_id>', view_func=AlunoController.atualizar_aluno, methods=['PUT'])
    app.add_url_rule('/alunos/<int:aluno_id>', view_func=AlunoController.deletar_aluno, methods=['DELETE'])