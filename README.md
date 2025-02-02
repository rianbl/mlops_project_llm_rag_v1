# Projeto MLOps - Fale com seus dados!

Este projeto implementa uma API de LLM (Large Language Model) para responder a perguntas sobre seus dados de forma interativa.

## 📌 Pré-requisitos
Antes de começar, certifique-se de ter instalado:
- Git
```bash
sudo apt update && sudo apt install -y git
```
- Python 3.x
```bash
sudo apt update && sudo apt install -y python3
```
- pip
```bash
sudo apt update && sudo apt install -y python3-pip
```
- WSL - Subsistema Linux
```bash
wsl --install
```

## 🚀 Primeiros Passos

### 1️⃣ Clone o repositório
Para obter o código-fonte do projeto, execute:
```bash
git clone https://github.com/rianbl/mlops_project_llm_rag_v1.git
cd mlops_project_llm_rag_v1
```

### 2️⃣ Configure um ambiente virtual
Crie e ative um ambiente virtual Python para gerenciar dependências isoladamente:
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate    # Para Windows (cmd)
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Inicie a API do LLM
```bash
python3 llm.py
```

### 5️⃣ Teste a API
Faça uma requisição para a API usando `curl`:
```bash
curl -X POST "http://localhost:8081/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Qual é a capital do Brasil?"}'
```

## 📄 Estrutura do Projeto
```
mlops_project_llm_rag_v1/
├── venv/                   # Ambiente virtual (não incluído no repositório)
├── requirements.txt        # Dependências do projeto
├── llm.py                  # Código principal da API LLM
├── README.md               # Este arquivo
└── ...                     # Outros arquivos relevantes
```

## 📢 Autor
- **Rian Lopes**
- Acesse: [YouTube - DataRVW](https://www.youtube.com/@datarvw)

