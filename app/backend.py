from flask import Flask, jsonify, request
import requests

app = Flask('conecta Hemosc')

# Rotas
@app.route('/')
def index():
    return 'Bem-vindo ao Conecta Hemosc!'

@app.route('/agendar_doacao', methods=['POST'])
def agendar_doacao():
    dados = request.get_json()
    # Aqui você pode processar os dados de agendamento de doação
    return jsonify({'mensagem': 'Doação agendada com sucesso!', 'dados': dados})

@app.route('/gerar_carteira/<nome>')
def gerar_carteira(nome):
    # Aqui você pode gerar a carteira de doador para o nome fornecido
    return jsonify({'carteira': 'Carteira de doador para {} gerada com sucesso!'.format(nome)})

# Rota para obter informações dos doadores do Hemoesc
@app.route('/doadores')
def obter_doadores():
    # URL da API do Hemoesc que fornece informações dos doadores
    url_api_hemoesc = 'https://www.hemosc.org.br/agende-sua-doacao.html'

    try:
        # Fazendo uma requisição GET para a API do Hemoesc
        response = requests.get(url_api_hemoesc)

        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            # Retorna os dados dos doadores obtidos da API
            return jsonify(response.json())

        # Caso contrário, retorna uma mensagem de erro
        return jsonify({'erro': 'Falha ao obter dados dos doadores do Hemoesc'})

    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'Erro de conexão com a API do Hemoesc: ' + str(e)}), 500

# Rodando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
    # Definindo a porta e o host para executar a aplicação
    port = 5000
    host = '0.0.0.0'

    # Iniciando a aplicação Flask
    app.run(host=host, port=port)