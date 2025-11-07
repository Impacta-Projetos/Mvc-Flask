from controllers.ctrls_reservas import ReservasController

def rotas_reservas(app):
    #TODO: definir as rotas para o recurso reservas
    app.add_url_rule('/reservas', view_func=ReservasController.listar_reservas, methods=['GET'])
    app.add_url_rule('/reservas/<int:reserva_id>', view_func=ReservasController.buscar_reserva, methods=['GET'])
    app.add_url_rule('/reservas', view_func=ReservasController.criar_reserva, methods=['POST'])
    app.add_url_rule('/reservas/<int:reserva_id>', view_func=ReservasController.atualizar_reserva, methods=['PUT'])
    app.add_url_rule('/reservas/<int:reserva_id>', view_func=ReservasController.deletar_reserva, methods=['DELETE'])