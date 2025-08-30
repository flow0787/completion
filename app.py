from flask import Flask, request, jsonify
import logging, os, requests, json


app = Flask(__name__)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
app_version = "0.1"
history = []

# Configure logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
    )
logger = logging.getLogger("app")

# Define a /healthcheck endpoint
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.debug("Healthcheck endpoint called")
    return jsonify({
        "status": "ok",
        "version": app_version
    })

# Function to call OpenRouter API
def call_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = json.dumps({
        "model": "meta-llama/llama-4-scout:free",
        "stream": False,
        "messages": [{"role": "user", "content": prompt}]
    })
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

# Define a /completion endpoint
@app.route('/completion', methods=['POST'])
def completion():
    logger.debug("Completion endpoint called")
    
    # Validate input
    if not request.is_json:
        logger.warning("Received non-JSON request")
        return jsonify({"error": "Invalid input, JSON expected"}), 400
    data = request.get_json()
    prompt = data.get("prompt", "")
    if 'prompt' not in data:
        logger.error("Missing 'prompt' in request")
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    # Call OpenRouter API
    try:
        api_response = call_openrouter(prompt)
        logger.info("Successfully called OpenRouter API")
        message_content = api_response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {e}")
        return jsonify({"error": "Failed to get completion from external API"}), 500
    
    # Store in history
    history.append({"prompt": prompt, "completion": message_content})
    logger.debug(f"Stored completion in history, total entries: {len(history)}")
    return jsonify({
        "completion": message_content
    })

# Define a /history endpoint
@app.route('/history', methods=['GET'])
def get_history():
    logger.debug("History endpoint called")
    return jsonify(history)

# Error handlers
@app.errorhandler(405)
def method_not_allowed(error):
    logger.warning(f"Method Not Allowed: {request.method} on {request.path}")
    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    logger.info(f"Starting app version {app_version} with log level {log_level} on port 5500")
    app.run(debug=True, host='0.0.0.0', port=5500)