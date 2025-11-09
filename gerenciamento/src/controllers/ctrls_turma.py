from flask import request, jsonify
from models import Turma, Professor, banco_de_dados
from sqlalchemy.exc import IntegrityError

class TurmaController:
     # A chamada para esse método seria feita diretamente pela classe, sem a necessidade de criar um objeto (uma instância):
     @staticmethod
     def listar_turmas():
          turmas = Turma.query.all()
          if turmas:
               resultado = [
                    {
                         'id': turma.id,
                         'descricao': turma.descricao,
                         'professor_id': turma.professor_id,
                         'ativo': turma.ativo,
                    } for turma in turmas
               ]
               return jsonify(resultado), 200
          else:
               return jsonify({'mensagem': 'Nenhuma turma encontrada.'}), 200
          
     @staticmethod
     def buscar_turma(turma_id):
          turma = Turma.query.get(turma_id)
          if turma:
               return jsonify({
                    'id': turma.id,
                    'descricao': turma.descricao,
                    'professor_id': turma.professor_id,
                    'ativo': turma.ativo
               }), 200
          else:
               return jsonify({'erro': 'Turma não encontrada.'}), 404

     @staticmethod
     def criar_turma():
          dados = request.get_json()
          campos_obrigatorios = ['descricao', 'professor_id']
          if not dados or not all(k in dados for k in campos_obrigatorios):
               return jsonify({'erro': 'descricao e professor_id são campos obrigatórios.'}), 400
          professor_id = dados['professor_id']
          professor = Professor.query.get(professor_id)
          if not professor:
               return jsonify({'erro': f'Professor com id {professor_id} não existe'}), 400

          nova_turma = Turma(
               descricao = dados['descricao'],
               professor_id = dados['professor_id'],
               ativo = dados.get('ativo', True)
          )
          banco_de_dados.session.add(nova_turma)
          banco_de_dados.session.commit()

          return jsonify(
               {
                    'mensagem': 'Turma criada com sucesso!',
                    'dados': {
                         'id': nova_turma.id,
                         'descricao': nova_turma.descricao,
                         'professor_id': nova_turma.professor_id,
                         'ativo': nova_turma.ativo
                    }
               }
          ), 201
     @staticmethod
     def atualizar_turma(turma_id):
          turma = Turma.query.get(turma_id)
          if turma:
               dados = request.get_json()
               turma.descricao = dados.get('descricao', turma.descricao)
               turma.professor_id = dados.get('professor_id', turma.professor_id)
               turma.ativo = dados.get('ativo', turma.ativo)

               professor = Professor.query.get(dados.get('professor_id'))
               if not professor:
                    return jsonify({'erro': f'Professor com id {dados.get("professor_id")} não existe'}), 400
               
               banco_de_dados.session.commit()
               return jsonify({'mensagem': 'Turma atualizada com sucesso!'}), 200
          else:
               return jsonify({'erro': 'Turma não encontrada.'}), 404

     @staticmethod
     def deletar_turma(turma_id):
          turma = Turma.query.get(turma_id)
          if not turma:
            return jsonify({"erro": "Turma não encontrada."}), 404
          try:
               banco_de_dados.session.delete(turma)
               banco_de_dados.session.commit()
               return jsonify({"mensagem": "Turma deletada com sucesso!"}), 200
          except IntegrityError:
               banco_de_dados.session.rollback()
               return jsonify({"erro": "Não é possível deletar a turma pois existem alunos vinculados."}), 409
          except Exception as e:
               banco_de_dados.session.rollback()
               return jsonify({"erro": f"Erro ao deletar turma: {str(e)}"}), 500