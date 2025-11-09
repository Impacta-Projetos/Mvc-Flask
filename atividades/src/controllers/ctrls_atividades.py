import requests
from flask import jsonify, request
from models import Atividades, banco_atv
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def validar_professor(professor_id):
    try:
        response = requests.get(f'http://gerenciamento:5000/professores/{professor_id}')
        if response.status_code == 200:
            dados = response.json()
            mensagem = f"Professor encontrado: {dados}"
            return True, mensagem
        else:
            mensagem = f"Professor não encontrado. Status: {response.status_code}"
            return False, mensagem
    except requests.exceptions.RequestException as e:
        mensagem = f"Erro de conexão com Gerenciamento: {e}"
        return False, mensagem

def validar_turma(turma_id):
    try:
        response = requests.get(f'http://gerenciamento:5000/turmas/{turma_id}')
        if response.status_code == 200:
            dados = response.json()
            mensagem = f"Turma encontrada: {dados}"
            return True, mensagem
        else:
            mensagem = f"Turma não encontrada. Status: {response.status_code}"
            return False, mensagem
    except requests.exceptions.RequestException as e:
        mensagem = f"Erro de conexão com Gerenciamento: {e}"
        return False, mensagem

class AtividadesController:
    @staticmethod
    def listar_atividades():
        atividades = Atividades.query.all()
        if atividades:
            resultado = [
                {
                    'id': atividade.id,
                    'nome_atividade': atividade.nome_atividade,
                    'descricao': atividade.descricao,
                    'peso_porcento': atividade.peso_porcento,
                    'data_entrega': atividade.data_entrega.strftime('%Y-%m-%d') if atividade.data_entrega else None,
                    'turma_id': atividade.turma_id,
                    'professor_id': atividade.professor_id
                } for atividade in atividades
            ]
            return jsonify(resultado), 200
        else:
            return jsonify({'mensagem': 'Nenhuma atividade encontrada.'}), 200
        
    @staticmethod
    def buscar_atividade(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if atividade:
            return jsonify(
                {
                    'id': atividade.id,
                    'nome_atividade': atividade.nome_atividade,
                    'descricao': atividade.descricao,
                    'peso_porcento': atividade.peso_porcento,
                    'data_entrega': atividade.data_entrega.strftime('%Y-%m-%d') if atividade.data_entrega else None,
                    'turma_id': atividade.turma_id,
                    'professor_id': atividade.professor_id
                }
            ), 200
        else:
            return jsonify({'erro': 'Atividade não encontrada.'}), 404
        
    @staticmethod
    def criar_atividade():
        dados = request.get_json()
        campos_obrigatorios = ['nome_atividade', 'descricao', 'peso_porcento', 'data_entrega', 'turma_id', 'professor_id']
        if not dados or not all(k in dados for k in campos_obrigatorios):
            return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400
        
        valido_turma, msg_turma = validar_turma(dados['turma_id'])
        if not valido_turma:
            return jsonify({'erro': 'Turma inválida.', 'detalhes': [msg_turma]}), 400
        
        valido_prof, msg_prof = validar_professor(dados['professor_id'])
        if not valido_prof:
            return jsonify({'erro': 'Professor inválido.', 'detalhes': [msg_prof]}), 400

        # Converter string de data para objeto datetime
        try:
            data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
        
        nova_atividade = Atividades(
            nome_atividade = dados['nome_atividade'],
            descricao = dados['descricao'],
            peso_porcento = dados['peso_porcento'],
            data_entrega = data_entrega,
            turma_id = dados['turma_id'],
            professor_id = dados['professor_id']
        )
        try:
            banco_atv.session.add(nova_atividade)
            banco_atv.session.commit()
            return jsonify({
                'mensagem': 'Atividade criada com sucesso.',
                'dados': {
                    'id': nova_atividade.id,
                    'nome_atividade': nova_atividade.nome_atividade,
                    'descricao': nova_atividade.descricao,
                    'peso_porcento': nova_atividade.peso_porcento,
                    'data_entrega': nova_atividade.data_entrega.strftime('%Y-%m-%d'),
                    'turma_id': nova_atividade.turma_id,
                    'professor_id': nova_atividade.professor_id
                }
            }), 201
        except Exception as e:
            banco_atv.session.rollback()
            return jsonify({'erro': f'Erro ao criar atividade: {str(e)}'}), 400

    @staticmethod
    def atualizar_atividade(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if atividade:
            dados = request.get_json()
            turma_id = dados.get('turma_id', atividade.turma_id)
            professor_id = dados.get('professor_id', atividade.professor_id)

            valido_turma, msg_turma = validar_turma(turma_id)
            if not valido_turma:
                return jsonify({'erro': 'Turma inválida.', 'detalhes': [msg_turma]}), 400
            
            valido_prof, msg_prof = validar_professor(professor_id)
            if not valido_prof:
                return jsonify({'erro': 'Professor inválido.', 'detalhes': [msg_prof]}), 400

            # Converter string de data para objeto datetime se fornecido
            if 'data_entrega' in dados:
                try:
                    data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
            else:
                data_entrega = atividade.data_entrega
            
            atividade.nome_atividade = dados.get('nome_atividade', atividade.nome_atividade)
            atividade.descricao = dados.get('descricao', atividade.descricao)
            atividade.peso_porcento = dados.get('peso_porcento', atividade.peso_porcento)
            atividade.data_entrega = data_entrega
            atividade.turma_id = turma_id
            atividade.professor_id = professor_id

            try:
                banco_atv.session.commit()
                return jsonify({'mensagem': 'Atividade atualizada com sucesso.'}), 200
            except Exception as e:
                banco_atv.session.rollback()
                return jsonify({'erro': f'Erro ao atualizar atividade: {str(e)}'}), 400
        else:
            return jsonify({'erro': 'Atividade não encontrada.'}), 404
            
    @staticmethod
    def deletar_atividade(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if atividade:
            try:
                banco_atv.session.delete(atividade)
                banco_atv.session.commit()
                return jsonify({'mensagem': 'Atividade deletada com sucesso.'}), 200
            except IntegrityError:
                banco_atv.session.rollback()
                return jsonify({'erro': 'Não é possível deletar a atividade pois existem notas vinculadas.'}), 409
            except Exception:
                banco_atv.session.rollback()
                return jsonify({'erro': 'Erro ao deletar atividade.'}), 400
        else:
            return jsonify({'erro': 'Atividade não encontrada.'}), 404