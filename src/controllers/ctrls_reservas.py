import requests
from flask import jsonify, request
from models import Reservas, banco_res
from sqlalchemy.exc import IntegrityError

class ReservasController:
    #TODO: implementar os métodos do controlador de reservas
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
                      'data': reserva.data,
                      'turma_id': reserva.turma_id
                  } for reserva in reservas
              ]
              return jsonify(resultado), 200
          else:
              return jsonify({'mensagem': 'Reserva não encontrado.'}), 200

     @staticmethod
     def criar_reserva():
         dados = request.get_json()
         campos_obrigatorios = ['id', 'num_sala', 'lab', 'data', 'turma_id']
         if not dados or not all(k in dados for k in campos_obrigatorios):
             return jsonify({'erro': 'nome, num_sala, lab, data, e turma_id são campos obrigatórios.'}), 400
         turma_id = dados['turma_id']
         valido_turma, msg_turma = validar_turma(dados['turma_id'])
         if not valido_turma:
            return jsonify({'erro': 'Turma  inválida.', 'detalhes': [msg_turma]})

         try:
             from datetime import datetime
             # Converter string de data para objeto date
             data = datetime.strptime(dados['data'], '%Y-%m-%d').date()
             
             nova_reserva = Aluno(
                nome = dados['nome'],
                idade = dados['idade'],
                turma_id = dados['turma_id'],
                data = data,
             )
         except ValueError:
             return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
         except Exception as e:
             return jsonify({'erro': f'Erro ao processar dados: {str(e)}'}), 400

         try:
             banco_de_dados.session.add(nova_reserva)
             banco_de_dados.session.commit()
             
             return jsonify({
                 'mensagem': 'Aluno criado com sucesso!',
                 'id': nova_reserva.id,
                 'num_sala': nova_reserva.num_sala,
                 'lab': nova_reserva.lab,
                 'turma_id': nova_reserva.turma_id,
                 'data_nascimento': nova_reserva.data.strftime('%Y-%m-%d'),
             }), 201
         except Exception as e:
             banco_de_dados.session.rollback()
             return jsonify({'erro': f'Erro ao salvar no banco: {str(e)}'}), 500
         
     @staticmethod
     def buscar_reserva(reserva_id):
         reserva = Reservas.query.get(reserva_id)
         if reserva:
             return jsonify({
                 'id': nova_reserva.id,
                 'num_sala': nova_reserva.num_sala,
                 'lab': nova_reserva.lab,
                 'turma_id': nova_reserva.turma_id,
                 'data_nascimento': nova_reserva.data.strftime('%Y-%m-%d')
             }), 200
         else:
             return jsonify({'erro': 'Reserva não encontrada.'}), 404
     
     @staticmethod
     def atualizar_reserva(reserva_id):
         reserva = Reserva.query.get(reserva_id)
         if reserva:
             dados = request.get_json()
             reserva.num_sala = dados.get('num_sala', reserva.num_sala)
             reserva.data = dados.get('data', reserva.data)
             reserva.turma_id = dados.get('turma_id', reserva.turma_id)
             reserva.lab = dados.get('lab', reserva.lab)
             valido_turma, msg_turma = validar_turma(dados['turma_id'])
             if not valido_prof:
                 return jsonify({'erro': f'Turma com id {dados.get("turma_id")} não existe.'}), 400
             banco_de_dados.session.commit()
             return jsonify({'mensagem': 'Aluno atualizado com sucesso!'}), 200
         else:
             return jsonify({'erro': 'Aluno não encontrado.'}), 404

     @staticmethod
     def deletar_reserva(reserva_id):
         reserva = Reservas.query.get(reserva_id)
         if reserva:
             banco_de_dados.session.delete(reserva)
             banco_de_dados.session.commit()
             return jsonify({'mensagem': 'Reserva deletada com sucesso!'}), 200
         else:
             return jsonify({'erro': 'Reserva não encontrada.'}), 404