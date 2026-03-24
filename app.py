from flask import Flask, render_template, request, jsonify
import json
import pandas as pd

app = Flask(__name__)

# Load results
try:
    with open('insights.json', 'r') as f:
        insights = json.load(f)
except:
    insights = {}

@app.route('/')
def index():
    return render_template('index.html', insights=insights)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    aha = float(data.get('aha', 0))
    qsr = float(data.get('qsr', 0))
    sessions = int(data.get('sessions', 0))
    div = int(data.get('div', 0))
    
    # Logic from success_predict.py
    s_score = min(100, (sessions / 500) * 100) * 0.92
    a_score = max(0, (1 - (aha / 2160))) * 100 * 0.04
    q_score = (qsr) * 100 * 0.02
    d_score = (div / 13) * 100 * 0.02
    
    prob = round(s_score + a_score + q_score + d_score, 2)
    
    status = "CHURN RISK"
    if prob > 80: status = "POWER USER"
    elif prob > 50: status = "STEADY GROWER"
    
    return jsonify({
        'score': prob,
        'status': status
    })

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
