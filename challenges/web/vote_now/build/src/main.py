from flask import Flask, request, jsonify, render_template
import re
import hmac
import random
import string
import os

app = Flask(__name__)

voted_cidrs = set()
TOKEN = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))

def get_req_ip():
    from_header = request.headers.get('X-Real-IP') or request.headers.get('X-Forwarded-For')
    if from_header and re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', from_header):
        return from_header
    return request.remote_addr

def verify_pow(data: str, proof: str) -> bool:
    hash = hmac.new(TOKEN.encode(), (proof + "|" + data).encode(), 'sha512').hexdigest()
    # print(hash)
    return hash[:5] == "00000"

@app.post('/vote')
def vote():
    data = request.json
    ip = get_req_ip()
    cidr = ip.split('.')[0]
    if cidr in voted_cidrs:
        return jsonify({'error': f'Already voted as {cidr}.0.0.0/8'}), 400
    if not verify_pow(ip, data['proof']):
        return jsonify({'error': 'Invalid PoW'}), 400
    voted_cidrs.add(cidr)
    return jsonify({'success': True})

@app.route('/')
def index():
    return render_template('index.html', voted_cidrs=len(voted_cidrs), ip=get_req_ip(), token=TOKEN, flag=os.environ.get('GZCTF_FLAG'), is_voted=get_req_ip().split('.')[0] in voted_cidrs, cidr=get_req_ip().split('.')[0])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
