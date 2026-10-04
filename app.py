import time
from flask import Flask, render_template, request, abort
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP Request Duration in Seconds',
    ['endpoint']
)

# Mock Product Database (In-Memory)
PRODUCTS = [
    {
        "id": 1,
        "name": "ProBook Ultra Laptop 15\"",
        "price": 999.99,
        "category": "Laptops",
        "badge": "Best Seller",
        "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80"
    },
    {
        "id": 2,
        "name": "Noise-Canceling Wireless Headphones",
        "price": 249.50,
        "category": "Audio",
        "badge": "New Arrival",
        "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
    },
    {
        "id": 3,
        "name": "Smart Fitness Watch v2",
        "price": 179.00,
        "category": "Wearables",
        "badge": "Popular",
        "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"
    },
    {
        "id": 4,
        "name": "4K Curved Gaming Monitor 32\"",
        "price": 429.99,
        "category": "Monitors",
        "badge": "Sale",
        "img": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80"
    }
]

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.endpoint != 'metrics':
        resp_time = time.time() - request.start_time
        endpoint = request.endpoint or 'unknown'
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(resp_time)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
    return response

# Web Routes
@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:product_id>')
def buy_product(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return f"<h3>Order Confirmed! You purchased {product['name']} for ${product['price']}.</h3><a href='/'>Return to Store</a>", 200
    abort(404)

# Error Simulation Routes for Observability
@app.route('/simulate-db-crash')
def simulate_db_crash():
    # Simulates an unexpected database connection failure during checkout
    return "<h1>500 Internal Server Error</h1><p>DatabaseConnectionError: Connection to Inventory DB timed out after 3000ms.</p>", 500

@app.route('/simulate-404')
def simulate_404():
    abort(404)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)