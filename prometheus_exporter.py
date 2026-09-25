import time
import random
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 1. Import & Minimal 3 Metrik
REQUEST_COUNT = Counter('inference_requests_total', 'Total inference requests', ['method', 'endpoint', 'http_status'])
LATENCY = Histogram('inference_latency_seconds', 'Inference latency in seconds')
ACTIVE_REQUESTS = Gauge('active_requests_count', 'Number of active inference requests')

@app.route('/predict', methods=['POST'])
def predict():
    ACTIVE_REQUESTS.inc()
    with LATENCY.time():
        time.sleep(random.uniform(0.01, 0.05)) # Simulasi latensi
        prediction = [0]
        REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='200').inc()
        ACTIVE_REQUESTS.dec()
        return jsonify({'prediction': prediction, 'status': 'success'})

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)