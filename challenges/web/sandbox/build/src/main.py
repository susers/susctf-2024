from flask import Flask, request, redirect, render_template
import os
import secrets
import random
import string


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
working_ids = []


@app.route('/', methods=['GET', 'POST'])
def index():
    id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return redirect(f"/sandbox/{id}")


@app.route('/sandbox/<id>', methods=['GET', 'POST'])
def sandbox(id):
    if not id.isalnum() or len(id) != 8:
        return 'invalid id'
    if not os.path.exists(f'/sandbox/{id}'):
        os.popen(f'mkdir /sandbox/{id} && chown www-data /sandbox/{id} && chmod a+w /sandbox/{id}').read()
    if request.method == 'GET':
        return render_template('submit_code.html', id=id)
    if request.method == 'POST':
        if id in working_ids:
            return 'sandbox is busy'
        working_ids.append(id)
        code = request.form.get('code')
        os.popen(f'cd /sandbox/{id} && rm *').read()
        os.popen(f'sudo -u www-data cp /app/init.py /sandbox/{id}/init.py && cd /sandbox/{id} && python3 init.py').read()
        os.popen(f'rm -rf /sandbox/{id}/phpcode').read()
        
        php_file = open(f'/sandbox/{id}/phpcode', 'w')
        php_file.write(code)
        php_file.close()

        result = os.popen(f'cd /sandbox/{id} && sudo -u nobody php phpcode').read()
        os.popen(f'cd /sandbox/{id} && rm *').read()
        working_ids.remove(id)

        return result


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
