from flask import jsonify, request
import requests
from models import Atividades, banco_atv
from sqlalchemy.exc import IntegrityError

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
                    'data_entrega': atividade.data_entrega,
                    'turma_id': atividade.turma_id,
                    'professor_id': atividade.professor_id
                } for atividade in atividades
            ], 200
            return jsonify(resultado)
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
                    'data_entrega': atividade.data_entrega,
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
        valido_prof, msg_prof = validar_professor(dados['professor_id'])
        if not valido_turma or not valido_prof:
            return jsonify({'erro': 'Turma ou professor inválido.', 'detalhes': [msg_turma, msg_prof]}), 400
        
        nova_atividade = Atividades(
            nome_atividade = dados['nome_atividade'],
            descricao = dados['descricao'],
            peso_porcento = dados['peso_porcento'],
            data_entrega = dados['data_entrega'],
            turma_id = dados['turma_id'],
            professor_id = dados['professor_id']
        )
        try:
            banco_atv.session.add(nova_atividade)
            banco_atv.session.commit()
            return jsonify({'mensagem': 'Atividade criada com sucesso.'}), 201
        except IntegrityError:
            banco_atv.session.rollback()
            return jsonify({'erro': 'Erro ao criar atividade. Verifique os dados e tente novamente.'}), 400
        
    @staticmethod
    def atualizar_atividade(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if atividade:
            dados = request.get_json()
            turma_id = dados.get('turma_id', atividade.turma_id)
            professor_id = dados.get('professor_id', atividade.professor_id)

            valido_turma, msg_turma = validar_turma(turma_id)
            valido_prof, msg_prof = validar_professor(professor_id)
            if not valido_turma or not valido_prof:
                return jsonify({'erro': 'Turma ou professor inválido.', 'detalhes': [msg_turma, msg_prof]}), 400
            
            atividade.nome_atividade = dados.get('nome_atividade', atividade.nome_atividade)
            atividade.descricao = dados.get('descricao', atividade.descricao)
            atividade.peso_porcento = dados.get('peso_porcento', atividade.peso_porcento)
            atividade.data_entrega = dados.get('data_entrega', atividade.data_entrega)
            atividade.turma_id = turma_id
            atividade.professor_id = professor_id

            try:
                banco_atv.session.commit()
                return jsonify({'mensagem': 'Atividade atualizada com sucesso.'}), 200
            except IntegrityError:
                banco_atv.session.rollback()
                return jsonify({'erro': 'Erro ao atualizar atividade. Verifique os dados e tente novamente.'}), 400
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
                return jsonify({'erro': 'Erro ao deletar atividade. Tente novamente mais tarde.'}), 400
        else:
            return jsonify({'erro': 'Atividade não encontrada.'}), 404