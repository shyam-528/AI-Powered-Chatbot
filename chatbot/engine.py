"""
AI-Powered Chatbot - Core Engine
Handles Gemini API calls and conversation state.
"""
import os
import time
import uuid
from collections import deque

from google import genai
from google.genai import types
from flask import jsonify, request


class ChatEngine:
    """Manages AI conversation logic and session history."""

    HISTORY_LIMIT = 20

    def __init__(self, api_key, model="gemini-1.5-flash", system_prompt=None):
        self.api_key = api_key
        self.model_name = model
        self.system_prompt = system_prompt or (
            "You are a helpful, friendly AI assistant. "
            "Answer clearly and concisely."
        )
        self.sessions = {}

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def _get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = deque(maxlen=self.HISTORY_LIMIT)
        return self.sessions[session_id]

    def _generate_reply(self, message, history):
        if self.client is None:
            return self._offline_reply(message)
        try:
            contents = history + [
                types.Content(
                    role="user",
                    parts=[types.Part(text=message)],
                )
            ]
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                ),
            )
            return response.text or "I could not generate a response."
        except Exception as exc:
            return (
                "Sorry, I could not reach the AI service right now. "
                f"Please try again in a moment. ({exc})"
            )

    @staticmethod
    def _offline_reply(message):
        message_lower = message.lower()
        if any(w in message_lower for w in ("hello", "hi", "hey")):
            return "Hello! I'm running in offline mode (no API key configured). Set GEMINI_API_KEY to enable full AI responses."
        if "help" in message_lower:
            return "I'm a demo chatbot. Configure your GEMINI_API_KEY in a .env file to unlock intelligent responses."
        return (
            "I'm currently in offline mode because no GEMINI_API_KEY is set. "
            "Add your key to the .env file and restart the app."
        )

    def chat_endpoint(self):
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not message:
            return jsonify({"error": "Message cannot be empty."}), 400

        history = self._get_session(session_id)

        started = time.time()
        reply = self._generate_reply(message, list(history))
        elapsed = round(time.time() - started, 2)

        history.append(
            types.Content(role="user", parts=[types.Part(text=message)])
        )
        history.append(
            types.Content(role="model", parts=[types.Part(text=reply)])
        )

        return jsonify(
            {
                "session_id": session_id,
                "reply": reply,
                "response_time": elapsed,
            }
        )

    def history_endpoint(self):
        session_id = request.args.get("session_id")
        if not session_id:
            return jsonify({"error": "session_id is required."}), 400
        history = []
        for content in self.sessions.get(session_id, []):
            history.append(
                {
                    "role": content.role,
                    "text": "".join(
                        part.text or "" for part in content.parts
                    ),
                }
            )
        return jsonify({"session_id": session_id, "history": history})

    def clear_endpoint(self):
        data = request.get_json(silent=True) or {}
        session_id = data.get("session_id")
        if session_id and session_id in self.sessions:
            del self.sessions[session_id]
        return jsonify({"status": "cleared"})
