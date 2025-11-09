from flask import request, jsonify
from models import Professor, banco_de_dados
from sqlalchemy.exc import IntegrityError

class ProfessorController:
     # A chamada para esse método seria feita diretamente pela classe, sem a necessidade de criar um objeto (uma instância):
     @staticmethod
     def listar_professores():
          professores = Professor.query.all()
          if professores:
              resultado = [
                  {
                      'id': professor.id,
                      'nome': professor.nome,
                      'idade': professor.idade,
                      'materia': professor.materia,
                      'observacoes': professor.observacoes
                  } for professor in professores
              ]
              return jsonify(resultado), 200
          else:
              return jsonify({'mensagem': 'Nenhum professor encontrado.'}), 200
          

     @staticmethod
     def buscar_professor(professor_id):
         professor = Professor.query.get(professor_id)
         if professor:
             return jsonify({
                 'id': professor.id,
                 'nome': professor.nome,
                 'idade': professor.idade,
                 'materia': professor.materia,
                 'observacoes': professor.observacoes
             }), 200
         else:
             return jsonify({'erro': 'Professor não encontrado.'}), 404

     @staticmethod
     def criar_professor():
         dados = request.get_json()
         campos_obrigatorios = ['nome', 'idade', 'materia']
         if not dados or not all(k in dados for k in campos_obrigatorios):
             return jsonify({'erro': 'nome, idade e materia são campos obrigatórios.'}), 400
         
         novo_professor = Professor(
            nome = dados['nome'],
            idade = dados['idade'],
            materia = dados['materia'],
            observacoes = dados.get('observacoes')
         )
         banco_de_dados.session.add(novo_professor)
         banco_de_dados.session.commit()

         return jsonify({
             'mensagem': 'Professor criado com sucesso!',
             'dados': {
                 'id': novo_professor.id,
                 'nome': novo_professor.nome,
                 'idade': novo_professor.idade,
                 'materia': novo_professor.materia,
                 'observacoes': novo_professor.observacoes
             }
         }), 201
     
     @staticmethod
     def atualizar_professor(professor_id):
         professor = Professor.query.get(professor_id)
         if professor:
             dados = request.get_json()
             professor.nome = dados.get('nome', professor.nome)
             professor.idade = dados.get('idade', professor.idade)
             professor.materia = dados.get('materia', professor.materia)
             professor.observacoes = dados.get('observacoes', professor.observacoes)
             
             banco_de_dados.session.commit()
             return jsonify({'mensagem': 'Professor atualizado com sucesso!'}), 200
         else:
             return jsonify({'erro': 'Professor não encontrado.'}), 404
     
     @staticmethod
     def deletar_professor(professor_id):
         professor = Professor.query.get(professor_id)
         if not professor:
            return jsonify({"erro": "Professor não encontrado."}), 404
         try:
             banco_de_dados.session.delete(professor)
             banco_de_dados.session.commit()
             return jsonify({"mensagem": "Professor deletado com sucesso!"}), 200
         except IntegrityError:
             banco_de_dados.session.rollback()
             return jsonify({"erro": "Não é possível deletar o professor pois existem turmas vinculadas."}), 409
         except Exception as e:
             banco_de_dados.session.rollback()
             return jsonify({"erro": f"Erro ao deletar professor: {str(e)}"}), 400