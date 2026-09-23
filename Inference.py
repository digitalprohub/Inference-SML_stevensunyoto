import os
import pandas as pd
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('inference_requests_total', 'Total inference requests', ['method', 'endpoint', 'http_status'])
LATENCY = Histogram('inference_latency_seconds', 'Inference latency')

@app.route('/predict', methods=['POST'])
def predict():
    with LATENCY.time():
        try:
            data = request.get_json()
            # Logika inferensi dummy/simulasi model
            prediction = [0]  # Non-default risk
            
            REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='200').inc()
            return jsonify({'prediction': prediction, 'status': 'success'})
        except Exception as e:
            REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='500').inc()
            return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)