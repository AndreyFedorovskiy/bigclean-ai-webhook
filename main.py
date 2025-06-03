from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API-ключ через переменные окружения

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get('message', '')

    if not OPENAI_API_KEY:
        return jsonify({
            "messages": [
                {
                    "type": "text",
                    "text": "⚠️ Не настроен ключ доступа к ChatGPT. Обратитесь к администратору."
                }
            ]
        }), 500

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Ты вежливый, дружелюбный менеджер клининговой компании BIGclean. Отвечай тепло, понятно и по-человечески. Не выдавай, что ты бот."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        gpt_reply = response.json()['choices'][0]['message']['content']
        return jsonify({
            "messages": [
                {
                    "type": "text",
                    "text": gpt_reply.strip()
                }
            ]
        })
    else:
        print("Ошибка GPT:", response.text)
        return jsonify({
            "messages": [
                {
                    "type": "text",
                    "text": "Извините, произошла ошибка. Пожалуйста, попробуйте позже."
                }
            ]
        }), 500

if __name__ == '__main__':
    app.run(port=5005)
