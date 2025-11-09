import requests
from flask import jsonify, request
from models import Notas, Atividades, banco_atv

def validar_aluno(aluno_id):
    try:
        response = requests.get(f'http://gerenciamento:5000/alunos/{aluno_id}')
        if response.status_code == 200:
            dados = response.json()
            mensagem = f"Aluno encontrado: {dados}"
            return True, mensagem
        else:
            mensagem = f"Aluno não encontrado. Status: {response.status_code}"
            return False, mensagem
    except requests.exceptions.RequestException as e:
        mensagem = f"Erro de conexão com Gerenciamento: {e}"
        return False, mensagem

class NotasController:
    @staticmethod
    def listar_notas():
        notas = Notas.query.all()
        if notas:
            resultado = [
                {
                    'id': nota.id,
                    'nota': nota.nota,
                    'aluno_id': nota.aluno_id,
                    'atividade_id': nota.atividade_id,
                } for nota in notas 
            ]
            return jsonify(resultado), 200  
        else:
            return jsonify({'mensagem': 'Nenhuma nota encontrada.'}), 200

    @staticmethod
    def buscar_nota(nota_id):
        nota = Notas.query.get(nota_id)
        if nota:
            return jsonify(
                {
                    'id': nota.id,
                    'nota': nota.nota,
                    'aluno_id': nota.aluno_id,
                    'atividade_id': nota.atividade_id,
                }
            ), 200
        else:
            return jsonify({'erro': 'Nota não encontrada.'}), 404
        
    @staticmethod
    def criar_nota():
        dados = request.get_json()
        campos_obrigatorios = ['nota', 'aluno_id', 'atividade_id']
        if not dados or not all(k in dados for k in campos_obrigatorios):
            return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400
        
        valido_aluno, msg_aluno = validar_aluno(dados['aluno_id'])
        if not valido_aluno:
            return jsonify({'erro': 'Aluno inválido.', 'detalhes': [msg_aluno]}), 400

        atividade = Atividades.query.get(dados['atividade_id'])
        if not atividade:
            return jsonify({'erro': f'Atividade com id {dados["atividade_id"]} não existe.'}), 400

        nova_nota = Notas(
            nota=dados['nota'],
            aluno_id=dados['aluno_id'],
            atividade_id=dados['atividade_id']
        )
        try:
            banco_atv.session.add(nova_nota)
            banco_atv.session.commit()
            return jsonify({
                'mensagem': 'Nota criada com sucesso.',
                'dados': {
                    'id': nova_nota.id,
                    'nota': nova_nota.nota,
                    'aluno_id': nova_nota.aluno_id,
                    'atividade_id': nova_nota.atividade_id
                }
            }), 201
        except Exception as e:
            banco_atv.session.rollback()
            return jsonify({'erro': f'Erro ao criar nota: {str(e)}'}), 400

    @staticmethod
    def atualizar_nota(nota_id):
        nota = Notas.query.get(nota_id)
        if nota:
            dados = request.get_json()
            nota.nota = dados.get('nota', nota.nota)
            nota.aluno_id = dados.get('aluno_id', nota.aluno_id)
            nota.atividade_id = dados.get('atividade_id', nota.atividade_id)

            valido_aluno, msg_aluno = validar_aluno(dados['aluno_id'])
            if not valido_aluno:
                return jsonify({'erro': 'Aluno inválido.', 'detalhes': [msg_aluno]}), 400
            
            atividade = Atividades.query.get(dados.get('atividade_id'))
            if not atividade:
                return jsonify({'erro': f'Atividade com id {dados.get("atividade_id")} não existe.'}), 400

            nota.nota = dados.get('nota', nota.nota)
            nota.aluno_id = dados.get('aluno_id', nota.aluno_id)
            nota.atividade_id = dados.get('atividade_id', nota.atividade_id)

            try:
                banco_atv.session.commit()
                return jsonify({'mensagem': 'Nota atualizada com sucesso.'}), 200
            except Exception as e:
                banco_atv.session.rollback()
                return jsonify({'erro': f'Erro ao atualizar nota: {str(e)}'}), 400
        else:
            return jsonify({'erro': 'Nota não encontrada.'}), 404

    @staticmethod
    def deletar_nota(nota_id):
        nota = Notas.query.get(nota_id)
        if nota:
            try:
                banco_atv.session.delete(nota)
                banco_atv.session.commit()
                return jsonify({'mensagem': 'Nota deletada com sucesso.'}), 200
            except Exception as e:
                banco_atv.session.rollback()
                return jsonify({'erro': f'Erro ao deletar nota: {str(e)}'}), 400
        else:
            return jsonify({'erro': 'Nota não encontrada.'}), 404
        