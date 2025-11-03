from flask import request, jsonify
from models import Aluno, Turma, banco_de_dados

class AlunoController:
     # A chamada para esse método seria feita diretamente pela classe, sem a necessidade de criar um objeto (uma instância):
     @staticmethod
     def listar_alunos():
          alunos = Aluno.query.all()
          if alunos:
              resultado = [
                  {
                      'id': aluno.id,
                      'nome': aluno.nome,
                      'idade': aluno.idade,
                      'turma_id': aluno.turma_id,
                      'data_nascimento': aluno.data_nascimento.strftime('%Y-%m-%d') if aluno.data_nascimento else None,
                  } for aluno in alunos
              ]
              return jsonify(resultado), 200
          else:
              return jsonify({'mensagem': 'Nenhum aluno encontrado.'}), 200

     @staticmethod
     def criar_aluno():
         dados = request.get_json()
         campos_obrigatorios = ['nome', 'idade', 'turma_id', 'data_nascimento']
         if not dados or not all(k in dados for k in campos_obrigatorios):
             return jsonify({'erro': 'nome, idade, turma_id, data_nascimento são campos obrigatórios.'}), 400
         turma_id = dados['turma_id']
         turma = Turma.query.get(turma_id)
         if not turma:
             return jsonify({'erro': f'Turma com id {turma_id} não existe.'}), 400

         try:
             from datetime import datetime
             # Converter string de data para objeto date
             data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
             
             novo_aluno = Aluno(
                nome = dados['nome'],
                idade = dados['idade'],
                turma_id = dados['turma_id'],
                data_nascimento = data_nascimento,
             )
         except ValueError:
             return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
         except Exception as e:
             return jsonify({'erro': f'Erro ao processar dados: {str(e)}'}), 400

         try:
             banco_de_dados.session.add(novo_aluno)
             banco_de_dados.session.commit()
             
             return jsonify({
                 'mensagem': 'Aluno criado com sucesso!',
                 'id': novo_aluno.id,
                 'nome': novo_aluno.nome,
                 'idade': novo_aluno.idade,
                 'turma_id': novo_aluno.turma_id,
                 'data_nascimento': novo_aluno.data_nascimento.strftime('%Y-%m-%d'),
             }), 201
         except Exception as e:
             banco_de_dados.session.rollback()
             return jsonify({'erro': f'Erro ao salvar no banco: {str(e)}'}), 500
         
     @staticmethod
     def buscar_aluno(aluno_id):
         aluno = Aluno.query.get(aluno_id)
         if aluno:
             return jsonify({
                 'id': aluno.id,
                 'nome': aluno.nome,
                 'idade': aluno.idade,
                 'turma_id': aluno.turma_id,
                 'data_nascimento': aluno.data_nascimento.strftime('%Y-%m-%d'),
             }), 200
         else:
             return jsonify({'erro': 'Aluno não encontrado.'}), 404
     
     @staticmethod
     def atualizar_aluno(aluno_id):
         aluno = Aluno.query.get(aluno_id)
         if aluno:
             dados = request.get_json()
             aluno.nome = dados.get('nome', aluno.nome)
             aluno.idade = dados.get('idade', aluno.idade)
             aluno.turma_id = dados.get('turma_id', aluno.turma_id)

             turma = Turma.query.get(dados.get('turma_id'))
             if not turma:
                 return jsonify({'erro': f'Turma com id {dados.get("turma_id")} não existe.'}), 400
             banco_de_dados.session.commit()
             return jsonify({'mensagem': 'Aluno atualizado com sucesso!'}), 200
         else:
             return jsonify({'erro': 'Aluno não encontrado.'}), 404

     @staticmethod
     def deletar_aluno(aluno_id):
         aluno = Aluno.query.get(aluno_id)
         if aluno:
             banco_de_dados.session.delete(aluno)
             banco_de_dados.session.commit()
             return jsonify({'mensagem': 'Aluno deletado com sucesso!'}), 200
         else:
             return jsonify({'erro': 'Aluno não encontrado.'}), 404