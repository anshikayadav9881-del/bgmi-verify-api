from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/get-bgmi-name', methods=['GET', 'POST'])
def get_bgmi_name():
    # Automatically extracts UID whether it comes from a browser link or a data payload
    uid = request.args.get('uid') or (request.get_json() or {}).get('uid') if request.is_json else None
    if not uid and request.method == 'POST':
        try: uid = request.get_json().get('uid')
        except: pass
        
    if not uid:
        uid = request.args.get('uid')

    if not uid:
        return jsonify({"success": False, "error": "No UID provided"})
        
    try:
        target_url = "https://codashop.com"
        payload = {
            "userId": str(uid),
            "zoneId": "",
            "shopId": "bgmi",
            "country": "IN"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json"
        }
        
        response = requests.post(target_url, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        if data and "confirmationFields" in data:
            username = data["confirmationFields"].get("username", "Unknown Player")
            return jsonify({"success": True, "nickname": username})
        else:
            return jsonify({"success": False, "error": "UID not found"})
            
    except Exception as e:
        return jsonify({"success": False, "error": "Server busy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
