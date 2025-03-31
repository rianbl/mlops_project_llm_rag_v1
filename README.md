1 Navegue até o diretório do seu projeto:

cd /caminho/do/seu/projeto

2 Instale o pacote python para ambientes virtuais

sudo apt update && sudo apt install python3-venv

3 Crie o ambiente virtual:

sudo python3 -m venv nome_do_venv

4 Ative o ambiente virtual:

source venv/bin/activate

5 Instale os pacotes necessários

pip install -r requirements.txt

6 Inicie a API do LLM

python3 llm.py

7 Chame a API do LLM

curl -X POST "http://localhost:8081/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Qual é a capital do Brasil?"}'

8 Inicie a API do Search

python3 search.py

9 -  Teste  a API do Search
curl -X POST "http://localhost:5000/query"  \
-H "Content-Type: application/json" \
-d '{"query": "Quem comprou a mesa?"}'