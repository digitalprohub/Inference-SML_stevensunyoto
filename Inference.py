import os
import pandas as pd
from flask import Flask, request, jsonify
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

# 3 Metrik Monitoring Wajib
REQUEST_COUNT = Counter('inference_requests_total', 'Total inference requests', ['method', 'endpoint', 'http_status'])
LATENCY = Histogram('inference_latency_seconds', 'Inference latency in seconds')
ACTIVE_REQUESTS = Gauge('active_requests_count', 'Number of active inference requests')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    ACTIVE_REQUESTS.inc()
    try:
        with LATENCY.time():
            # ... kode prediksi kamu ...
            prediction = [0]
            REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='200').inc()
        return jsonify({'prediction': prediction, 'status': 'success'})
    except Exception as e:
        REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='500').inc()
        return jsonify({'error': str(e), 'status': 'error'}), 500
    finally:
        ACTIVE_REQUESTS.dec()

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)