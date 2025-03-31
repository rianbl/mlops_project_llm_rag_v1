import requests
import time
from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug=True

HF_API_URL = os.getenv("HF_API_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_URL:
    logger.error("URL da API do Hugging Face não foi definida! Certifique-se de configurar a variável HF_API_URL.")
    raise ValueError("HF_API_URL não pode estar vazia.")

if not HF_API_TOKEN:
    logger.error("Token da API do Hugging Face não foi definido! Certifique-se de configurar a variável HF_API_TOKEN.")
    raise ValueError("HF_API_TOKEN não pode estar vazio.")

def query_hf_api(payload, retries=3, delay=5):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    for attempt in range(retries):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Tentativa {attempt}/{retries} falhou: {e}")
            time.sleep(delay) 

    logger.error("Falha ao obter resposta da API após múltiplas tentativas.")
    return None

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint que processa a requisição e chama o modelo."""
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()

        if not user_query:
            return jsonify({"error": "O campo 'query' é obrigatório."}), 400

        response = query_hf_api({
            "inputs": user_query,
            "parameters": {"temperature": 0.2, "max_length": 200}
        })

        if response is None:
            return jsonify({"error": "Falha ao obter resposta do modelo."}), 500

        return response[0].get("generated_text", "").strip()
    
    except Exception as e:
            logger.exception("Erro inesperado ao processar requisição.")
            return jsonify({"error": "Erro interno no servidor."}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
