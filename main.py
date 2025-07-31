from flask import Flask, request
import openai
import requests
from gtts import gTTS
import os
import base64

# CONFIGURAÇÕES
openai.api_key = "SUA_API_OPENAI"
zapi_instance = "SUA_INSTANCIA_ID"
zapi_token = "SEU_TOKEN_ZAPI"
zapi_base_url = f"https://api.z-api.io/instances/{zapi_instance}/token/{zapi_token}"

app = Flask(__name__)

def gerar_resposta_ia(pergunta):
    prompt = f"Você é Kaufman Galado, um motoboy esperto de Natal-RN. Fale com gírias e humor: {pergunta}"
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()

def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt-br')
    tts.save("resposta.mp3")
    with open("resposta.mp3", "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode('utf-8')
    os.remove("resposta.mp3")
    return audio_b64

def enviar_texto(numero, msg):
    payload = {"phone": numero, "message": msg}
    requests.post(f"{zapi_base_url}/send-text", json=payload)

def enviar_audio(numero, audio_b64):
    payload = {
        "phone": numero,
        "audio": audio_b64,
        "filename": "resposta.mp3"
    }
    requests.post(f"{zapi_base_url}/send-audio-base64", json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    msg = data.get("message")
    num = data.get("from")
    if msg:
        resposta = gerar_resposta_ia(msg)
        audio = gerar_audio(resposta)
        enviar_texto(num, resposta)
        enviar_audio(num, audio)
    return "ok", 200

if __name__ == "__main__":
    app.run(port=3000)
