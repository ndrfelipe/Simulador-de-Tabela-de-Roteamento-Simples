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
    print("\nLOG DO SERVIDOR: Recebida requisição em /api/simular")
    
    try:
        dados = request.json
        ip_destino = dados.get('ip_destino')

        if not ip_destino:
            print("LOG DO SERVIDOR: Erro - IP de destino não fornecido")
            return jsonify({"erro": "IP de destino não fornecido"}), 400

        # 1. Chamar a função atualizada
        # Ela agora retorna (melhor_rota, todas_as_rotas)
        melhor_rota, rotas_correspondentes = roteador_global.tabela_roteamento.encontrar_melhor_rota(ip_destino)

        # 2. Construir o JSON de resposta no formato que o React espera
        routes_json = []
        if rotas_correspondentes:
            for rota in rotas_correspondentes:
                # Verifica se a 'rota' atual é a 'melhor_rota'
                is_best = False
                if melhor_rota and (
                    rota.rede == melhor_rota.rede and
                    rota.proximo_salto == melhor_rota.proximo_salto and
                    rota.ad == melhor_rota.ad and
                    rota.metrica == melhor_rota.metrica
                ):
                    is_best = True
                
                routes_json.append({
                    "network": str(rota.rede),
                    "nextHop": rota.proximo_salto, # <-- Ajuste: 'nextHop' (camelCase)
                    "ad": rota.ad,
                    "metric": rota.metrica,        # <-- Ajuste: 'metric' (camelCase)
                    "isBest": is_best             # <-- A flag que o React espera!
                })
        
        # O frontend espera um objeto com uma chave 'routes'
        return jsonify({"routes": routes_json})

    except Exception as e:
        print(f"LOG DO SERVIDOR: Erro inesperado: {e}")
        return jsonify({"erro": f"Erro interno no servidor: {e}"}), 500
    

@app.route('/api/rotas', methods=['GET'])
def api_get_rotas():
    """ API bônus: permite que o frontend exiba a tabela de rotas atual """
    with open("routes.json", 'r') as f:
        rotas = json.load(f)
    return jsonify(rotas)


if __name__ == '__main__':
    # Roda o servidor web
    app.run(debug=True, port=5000)