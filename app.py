from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")  # https://api.z-api.io/instances/SEU_INSTANCIA/token/SEU_TOKEN

@app.route("/")
def home():
    return "Servidor rodando com OpenAI + Z-API!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        # Validação e extração
        if data.get("event") == "MESSAGE" and "message" in data:
            texto = data["message"].get("text", "")
            numero = data["message"].get("from", "")

            if not texto or not numero:
                return jsonify({"erro": "Mensagem ou número ausente."}), 400

            # Chama IA
            resposta = consultar_openai(texto)

            # Envia resposta
            enviar_mensagem(numero, resposta)

            return jsonify({"status": "respondido"}), 200
        else:
            return jsonify({"status": "ignorado"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"erro": str(e)}), 500

def consultar_openai(texto):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4",
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
