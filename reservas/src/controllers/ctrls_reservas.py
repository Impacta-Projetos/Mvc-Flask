import requests
from flask import jsonify, request
from models import Reservas, banco_res
from datetime import datetime

class ReservasController:
    @staticmethod
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

    @staticmethod
    def listar_reservas():
        reservas = Reservas.query.all()
        if reservas:
            resultado = [
                {
                    'id': reserva.id,
                    'num_sala': reserva.num_sala,
                    'lab': reserva.lab,
                    'data': reserva.data.strftime('%Y-%m-%d') if reserva.data else None,
                    'turma_id': reserva.turma_id
                } for reserva in reservas
            ]
            return jsonify(resultado), 200
        else:
            return jsonify({'mensagem': 'Nenhuma reserva encontrada.'}), 200

    @staticmethod
    def criar_reserva():
        dados = request.get_json()
        campos_obrigatorios = ['num_sala', 'data', 'turma_id']
        if not dados or not all(k in dados for k in campos_obrigatorios):
            return jsonify({'erro': 'num_sala, data e turma_id são campos obrigatórios.'}), 400

        valido_turma, msg_turma = ReservasController.validar_turma(dados['turma_id'])
        if not valido_turma:
            return jsonify({'erro': 'Turma inválida.', 'detalhes': [msg_turma]}), 400

        try:
            data = datetime.strptime(dados['data'], '%Y-%m-%d').date()
            nova_reserva = Reservas(
                num_sala=dados['num_sala'],
                lab=dados.get('lab', False),
                data=data,
                turma_id=dados['turma_id']
            )
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro ao processar dados: {str(e)}'}), 400

        try:
            banco_res.session.add(nova_reserva)
            banco_res.session.commit()
            return jsonify({
                'mensagem': 'Reserva criada com sucesso!',
                'id': nova_reserva.id,
                'num_sala': nova_reserva.num_sala,
                'lab': nova_reserva.lab,
                'turma_id': nova_reserva.turma_id,
                'data': nova_reserva.data.strftime('%Y-%m-%d') if nova_reserva.data else None,
            }), 201
        except Exception as e:
            banco_res.session.rollback()
            return jsonify({'erro': f'Erro ao criar reserva: {str(e)}'}), 400

    @staticmethod
    def buscar_reserva(reserva_id):
        reserva = Reservas.query.get(reserva_id)
        if reserva:
            return jsonify({
                'id': reserva.id,
                'num_sala': reserva.num_sala,
                'lab': reserva.lab,
                'turma_id': reserva.turma_id,
                'data': reserva.data.datetime.strptime('%Y-%m-%d') if reserva.data else None
            }), 200
        else:
            return jsonify({'erro': 'Reserva não encontrada.'}), 404

    @staticmethod
    def atualizar_reserva(reserva_id):
        reserva = Reservas.query.get(reserva_id)
        if not reserva:
            return jsonify({'erro': 'Reserva não encontrada.'}), 404

        dados = request.get_json() or {}

        if 'turma_id' in dados:
            valido_turma, msg_turma = ReservasController.validar_turma(dados['turma_id'])
            if not valido_turma:
                return jsonify({'erro': f'Turma com id {dados.get("turma_id")} não existe.', 'detalhes': [msg_turma]}), 400
            reserva.turma_id = dados['turma_id']

        if 'num_sala' in dados:
            reserva.num_sala = dados['num_sala']
        if 'lab' in dados:
            reserva.lab = dados['lab']
        if 'data' in dados:
            try:
                reserva.data = datetime.strptime(dados['data'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        try:
            banco_res.session.commit()
            return jsonify({'mensagem': 'Reserva atualizada com sucesso!'}), 200
        except Exception as e:
            banco_res.session.rollback()
            return jsonify({'erro': f'Erro ao atualizar reserva: {str(e)}'}), 400

    @staticmethod
    def deletar_reserva(reserva_id):
        reserva = Reservas.query.get(reserva_id)
        if reserva:
            try:
                banco_res.session.delete(reserva)
                banco_res.session.commit()
                return jsonify({'mensagem': 'Reserva deletada com sucesso!'}), 200
            except Exception as e:
                return jsonify({'erro': f'Erro ao deletar reserva: {str(e)}'}), 400
        else:
            return jsonify({'erro': 'Reserva não encontrada.'}), 404
