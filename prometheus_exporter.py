import time
import random
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ==========================================
# 1. Definisi 3 Metrik Prometheus Wajib
# ==========================================

# Metrik 1: Counter - Menghitung total jumlah request inference
REQUEST_COUNT = Counter(
    'inference_requests_total',
    'Total number of inference requests',
    ['method', 'endpoint', 'http_status']
)

# Metrik 2: Histogram - Mengukur latensi / durasi proses inference
LATENCY = Histogram(
    'inference_latency_seconds',
    'Inference latency in seconds'
)

# Metrik 3: Gauge - Memantau jumlah request aktif / beban sistem saat ini
ACTIVE_REQUESTS = Gauge(
    'active_requests_count',
    'Number of active inference requests currently processing'
)


# ==========================================
# 2. Endpoint Application & Metrics
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():
    # Menambah jumlah request aktif
    ACTIVE_REQUESTS.inc()

    # Mengukur latensi proses
    start_time = time.time()
    with LATENCY.time():
        # Simulasi proses pemrosesan model
        time.sleep(random.uniform(0.01, 0.05))
        prediction = [0]

    # Menambah counter total request yang berhasil
    REQUEST_COUNT.labels(method='POST', endpoint='/predict', http_status='200').inc()

    # Mengurangi jumlah request aktif setelah selesai
    ACTIVE_REQUESTS.dec()

    return jsonify({
        'prediction': prediction,
        'status': 'success',
        'execution_time': time.time() - start_time
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    # Endpoint resmi untuk di-scrape oleh Prometheus
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)