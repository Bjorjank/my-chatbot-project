import sys
import os
from flask import Flask, request, jsonify

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from my_chatbot_project.actions import ActionCheckAnswer, ActionDefaultFallback

app = Flask(__name__)

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.json
    message = data.get("message", "")
    action = ActionCheckAnswer()
    response_text = action.call_qwen_api(message)
    return jsonify({"response": response_text})

@app.route("/default_fallback", methods=["POST"])
def default_fallback():
    data = request.json
    message = data.get("message", "")
    action = ActionDefaultFallback()
    response_text = action.call_qwen_api(message)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)

