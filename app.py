from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/run-bot', methods=['GET'])
def run_bot():
    """
    Triggers the job application bot.
    """
    # For now, just return a confirmation message.
    # The actual bot logic will be added here later.
    return jsonify({"status": "success", "message": "Bot run initiated."}), 200

if __name__ == '__main__':
    # The app will run on http://localhost:5001 by default
    app.run(debug=True, host='0.0.0.0', port=5001)
