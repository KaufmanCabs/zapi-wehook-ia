from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv(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)
ZAPI_INSTANCE = os.getenv(https://api.z-api.io/instances/3E4FE8ADEA217089D7C596DEC512DD4C/token/38AD93FD88F22C35B4E73392/send-text)  # URL base da sua instância Z-API

# Rota de teste
@app.route("/")
def home():
    return "Servidor rodando com OpenAI + Z-API!"

# Rota de Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        # Extrair número e mensagem
        msg = data["message"]
        numero = data["phone"]

        # Enviar msg pra OpenAI
        resposta = consultar_openai(msg)

        # Enviar resposta via Z-API
        enviar_mensagem(numero, resposta)

        return jsonify({"status": "respondido"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"erro": str(e)}), 500


def consultar_openai(texto):
    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-4",  # ou gpt-3.5-turbo se quiser economizar
        "messages": [
            {"role": "system", "content": "Seja um assistente simpático e direto."},
            {"role": "user", "content": texto}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    resposta_ia = response.json()["choices"][0]["message"]["content"]
    return resposta_ia.strip()


def enviar_mensagem(numero, texto):
    url = f"{ZAPI_INSTANCE}/send-text"
    payload = {
        "phone": numero,
        "message": texto
    }

    response = requests.post(url, json=payload)
    print("Resposta da Z-API:", response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
