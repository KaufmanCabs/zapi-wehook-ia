from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Recebido webhook:", data)
    # Só responde OK por enquanto
    return jsonify({"status": "Webhook ativo"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
