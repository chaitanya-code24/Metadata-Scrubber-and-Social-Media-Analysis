from flask import Flask, render_template, request
from PyGeneratePassword import PasswordGenerate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    if request.method == 'POST':
        length = int(request.form['length'])
        use_digits = True if 'use_digits' in request.form else False
        use_special_chars = True if 'use_special_chars' in request.form else False

        password = PasswordGenerate(length=length, use_digits=use_digits, use_special_chars=use_special_chars)

        return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True,port=5020)
