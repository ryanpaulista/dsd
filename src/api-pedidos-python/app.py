from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados em memória (Mock)
PEDIDOS_DB = {
    1: {"id": 1, "item": "Notebook Gamer", "valor": 5000.00},
    2: {"id": 2, "item": "Mouse Sem Fio", "valor": 150.00},
    3: {"id": 3, "item": "Monitor 4K", "valor": 2500.00}
}

@app.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    pedido = PEDIDOS_DB.get(pedido_id)
    if pedido:
        return jsonify(pedido)
    return jsonify({"error": "Pedido não encontrado"}), 404

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.json
    novo_id = len(PEDIDOS_DB) + 1
    dados['id'] = novo_id
    PEDIDOS_DB[novo_id] = dados
    return jsonify(dados), 201

if __name__ == '__main__':
    # Rodando na porta 8001 para não bater com o Gateway (8000)
    app.run(port=8001, debug=True)