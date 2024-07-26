from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
HEADERS = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    text = request.form['text']
    output = query({
        "inputs": f"'{text}' read this and detect potentially harmful or offensive content",
    })
    generated_text = output[0]['generated_text']
    return render_template('result.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True, port=5006)
