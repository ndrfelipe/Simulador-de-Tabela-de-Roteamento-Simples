from flask import Flask, request, jsonify, render_template
from core.Router import Roteador
from flask_cors import CORS
from core.Table import TabelaRoteamento
from core.rota import Rota # Importe para o roteador usar
import json

# 1. Cria a aplicação Flask
app = Flask(__name__)
CORS(app)

# 2. Carrega o roteador UMA VEZ quando o servidor inicia.
#    Ele fica em memória, pronto para receber consultas.
print("Carregando rotas estáticas...")
roteador_global = Roteador()
roteador_global.carregar_rotas_estaticas("routes.json")

# --- Definição das Rotas da API ---

@app.route('/')
def index():
    return "API do Simulador de Roteamento está no ar. Use /api/simular."

@app.route('/api/simular', methods=['POST'])
def api_simular():
    """ 
    Esta é a API que o seu frontend vai chamar.
    Ela recebe um JSON (ex: {"ip_destino": "192.168.1.50"})
    e retorna um JSON com o resultado.
    """
    try:
        dados = request.json
        ip_destino = dados.get('ip_destino')

        if not ip_destino:
            return jsonify({"erro": "IP de destino não fornecido"}), 400

  
        
        melhor_rota = roteador_global.tabela_roteamento.encontrar_melhor_rota(ip_destino)

        if melhor_rota:
            resultado = {
                "ip_consultado": ip_destino,
                "melhor_rota_encontrada": {
                    "rede": str(melhor_rota.rede),
                    "proximo_salto": melhor_rota.proximo_salto,
                    "ad": melhor_rota.ad,
                    "metrica": melhor_rota.metrica
                }
            }
            return jsonify(resultado)
        else:
            return jsonify({
                "ip_consultado": ip_destino,
                "melhor_rota_encontrada": None,
                "mensagem": "Nenhuma rota correspondente encontrada (pacote descartado)."
            }), 404

    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {e}"}), 500

@app.route('/api/rotas', methods=['GET'])
def api_get_rotas():
    """ API bônus: permite que o frontend exiba a tabela de rotas atual """
    # Lê o arquivo json e o retorna
    with open("routes.json", 'r') as f:
        rotas = json.load(f)
    return jsonify(rotas)

# --- Fim das Rotas da API ---

if __name__ == '__main__':
    # Roda o servidor web
    app.run(debug=True, port=5000)