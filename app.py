from flask import Flask, request, jsonify
import random

RANDOM_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language used for web development, data science, and automation.",
    "Flask is a lightweight web framework that makes it easy to build web applications.",
    "Machine learning algorithms can help solve complex problems across various industries.",
    "The sun sets beautifully over the horizon, painting the sky in vibrant colors.",
    "Coffee is the fuel that powers many developers through long coding sessions.",
    "Open source software has revolutionized the way we build and share technology.",
    "Artificial intelligence continues to advance at an unprecedented pace.",
    "The ocean contains mysteries that we are still discovering today.",
    "Good code is not just functional, but also readable and maintainable."
]

app = Flask(__name__)
app_version = "0.1"


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "ok",
        "version": app_version
    })

@app.route('/completion', methods=['POST'])
def completion():

    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    data = request.get_json()
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", 50)

    if 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    random_text = random.choice(RANDOM_TEXTS)
    
    return jsonify({
        "completion": random_text
    })

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)