import requests
import time
import os
import logging
import difflib
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

HF_API_URL = os.getenv("HF_API_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

LOCAL_KNOWLEDGE_FILE = "source.txt"  # Arquivo local para RAG

if not HF_API_URL or not HF_API_TOKEN:
    logger.error("Certifique-se de configurar as variáveis HF_API_URL e HF_API_TOKEN.")
    raise ValueError("HF_API_URL e HF_API_TOKEN são obrigatórios.")


def load_local_knowledge():
    """Carrega o conhecimento do arquivo e divide em trechos."""
    if not os.path.exists(LOCAL_KNOWLEDGE_FILE):
        logger.warning("Arquivo de conhecimento local não encontrado. Continuando sem RAG.")
        return []
    
    with open(LOCAL_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return f.read().split("\n\n")  # Divide em blocos de conhecimento


knowledge_base = load_local_knowledge()


def retrieve_relevant_passage(query):
    """Retorna o trecho mais similar ao query do usuário usando difflib."""
    if not knowledge_base:
        return "Nenhuma informação adicional disponível."

    best_match = max(knowledge_base, key=lambda passage: difflib.SequenceMatcher(None, query, passage).ratio())
    return best_match


def query_hf_api(payload, retries=2, delay=5):
    """Envia a consulta para a API do Hugging Face com tentativas de repetição."""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    for attempt in range(retries):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Tentativa {attempt + 1}/{retries} falhou: {e}")
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

        relevant_context = retrieve_relevant_passage(user_query)

        full_prompt = f"""
        [INSTRUÇÕES]
        Você é um assistente especializado em fornecer respostas diretas e concisas, evitando redundâncias.
        Sua resposta deve se basear no [CONHECIMENTO RELEVANTE] se houver.

        [CONHECIMENTO RELEVANTE]
        "{relevant_context}"

        [PERGUNTA DO USUÁRIO]
        "{user_query}"

        **Resposta:** [Sua resposta direta]
        """

        logger.info(f"Full prompt enviado ao modelo: {full_prompt}")

        response = query_hf_api({
            "inputs": full_prompt,
            "parameters": {
                "temperature": 0.1, 
                "max_new_tokens": 100, 
                "repetition_penalty": 1.2, 
                "frequency_penalty": 0.5, 
                "return_full_text": False
            }
        })

        if response is None:
            return jsonify({"error": "Falha ao obter resposta do modelo."}), 500

        return response[0].get("generated_text", "").strip()
    except Exception as e:
        logger.exception("Erro inesperado ao processar requisição.")
        return jsonify({"error": "Erro interno no servidor."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
