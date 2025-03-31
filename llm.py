import requests
import time
from flask import Flask, request

app = Flask(__name__)
app.debug=True

HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"

HF_API_TOKEN = "seu_token"

def query_hf_api(payload, retries=2, delay=5):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    for attempt in range(retries):
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        
        print(f"Tentativa {attempt+1}/{retries} falhou: {response.text}")
        time.sleep(delay) 
    
    response.raise_for_status()

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint que processa a requisição e chama o modelo."""
    user_query = request.json.get("query", "").strip()

    response = query_hf_api({
        "inputs": user_query,
        "parameters": {"temperature": 0.2, "max_length": 200}
    })

    return response[0].get("generated_text", "").strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)