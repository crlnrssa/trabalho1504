from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulação de banco de dados em memória
estoque = {}
proximo_id = 1

# Produtos padrão
produtos_iniciais = [
    {"nome": "Mouse sem fio", "quantidade": 50, "valor": 79.90},
    {"nome": "Notebook Dell", "quantidade": 10, "valor": 3999.00},
    {"nome": "HD Externo 1TB", "quantidade": 20, "valor": 299.99},
    {"nome": "Monitor 24''", "quantidade": 15, "valor": 899.90}
]


# Inserindo os produtos padrão no estoque
for produto in produtos_iniciais:
    estoque[proximo_id] = {
        "id": proximo_id,
        "nome": produto["nome"],
        "quantidade": produto["quantidade"],
        "valor": float(produto["valor"])
    }
    proximo_id += 1


# Rota para listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(list(estoque.values())), 200

# Rota para adicionar novo produto
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    global proximo_id
    dados = request.get_json()

    if not dados.get('nome') or not isinstance(dados.get('quantidade'), int) or not isinstance(dados.get('valor'), (int, float)):
        return jsonify({'erro': 'Dados inválidos'}), 400

    produto = {
        'id': proximo_id,
        'nome': dados['nome'],
        'quantidade': dados['quantidade'],
        'valor': float(dados['valor'])
    }
    estoque[proximo_id] = produto
    proximo_id += 1
    return jsonify(produto), 201

# Rota para obter um produto específico
@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = estoque.get(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto), 200

# Rota para atualizar um produto
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    dados = request.get_json()
    produto = estoque.get(produto_id)

    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    if 'nome' in dados:
        produto['nome'] = dados['nome']
    if 'quantidade' in dados and isinstance(dados['quantidade'], int):
        produto['quantidade'] = dados['quantidade']
    if 'valor' in dados and isinstance(dados['valor'], (int, float)):
        produto['valor'] = float(dados['valor'])

    return jsonify(produto), 200

# Rota para deletar um produto
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    if produto_id not in estoque:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    del estoque[produto_id]
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200

# Inicia a aplicação em localhost:5000
if __name__ == '__main__':
    app.run(debug=True, host='localhost')
