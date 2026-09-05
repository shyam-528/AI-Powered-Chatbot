"""
AI-Powered Chatbot - Application Factory
Flask application with Gemini AI integration.
"""
import os

from dotenv import load_dotenv
from flask import Flask, render_template

from chatbot.engine import ChatEngine

load_dotenv()

app = Flask(__name__)

engine = ChatEngine(
    api_key=os.getenv("GEMINI_API_KEY"),
    model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    system_prompt=os.getenv("SYSTEM_PROMPT"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok", "service": "ai-powered-chatbot"}, 200


app.add_url_rule(
    "/api/chat",
    view_func=engine.chat_endpoint,
    methods=["POST"],
)

app.add_url_rule(
    "/api/history",
    view_func=engine.history_endpoint,
    methods=["GET"],
)

app.add_url_rule(
    "/api/clear",
    view_func=engine.clear_endpoint,
    methods=["POST"],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
