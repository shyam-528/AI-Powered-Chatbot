# AI-Powered Chatbot

An intelligent, end-to-end AI chatbot built with **Python**, **Flask**, and **Google Gemini**. It provides a clean web UI, session-based conversation memory, and a REST API — ready to deploy locally or in Docker.

## Features

- **Google Gemini Integration** — intelligent, context-aware responses via the Gemini API
- **Conversation Memory** — session-based chat history so the bot remembers context
- **Web Interface** — responsive chat UI with typing indicators and smooth animations
- **REST API** — programmatic access via `/api/chat` for integrations
- **Offline Fallback** — bot still responds (with a notice) when no API key is configured
- **Health Endpoint** — simple `/health` check for monitoring & load balancers
- **Docker Support** — one-command containerized deployment

## Project Structure

```
AI-Powered-Chatbot/
├── app.py                  # Flask app entry point & routes
├── chatbot/
│   ├── __init__.py
│   └── engine.py           # Chat engine: Gemini API + session handling
├── templates/
│   └── index.html          # Chat web UI
├── static/
│   ├── css/style.css       # Styling for the chat interface
│   └── js/script.js        # Frontend logic (fetch, session, render)
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment configuration
├── Dockerfile              # Container deployment
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- A Google Gemini API key — get one free at [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/shyam-528/AI-Powered-Chatbot.git
   cd AI-Powered-Chatbot
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   copy .env.example .env
   ```

   Then edit `.env` and set your API key:

   ```env
   GEMINI_API_KEY=your_actual_api_key
   ```

5. **Run the app**

   ```bash
   python app.py
   ```

6. **Open the chatbot**

   Visit [http://localhost:5000](http://localhost:5000) in your browser.

## API Reference

| Method | Endpoint     | Description                          |
| ------ | ------------ | ------------------------------------ |
| POST   | `/api/chat`  | Send a message, get an AI reply      |
| GET    | `/api/history` | Get conversation history for a session |
| POST   | `/api/clear` | Clear a session's history            |
| GET    | `/health`    | Service health check                 |

### Example Request

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?", "session_id": "demo-session"}'
```

### Example Response

```json
{
  "session_id": "demo-session",
  "reply": "Hi! I'm an AI assistant powered by Google Gemini...",
  "response_time": 1.42
}
```

## Docker Deployment

```bash
# Build the image
docker build -t ai-chatbot .

# Run the container
docker run -p 5000:5000 --env-file .env ai-chatbot
```

The app will be available at [http://localhost:5000](http://localhost:5000).

## Configuration

All settings are managed via environment variables (see `.env.example`):

| Variable         | Default           | Description                          |
| ---------------- | ----------------- | ------------------------------------ |
| `GEMINI_API_KEY` | —                 | Your Google Gemini API key           |
| `GEMINI_MODEL`   | `gemini-3.6-flash`| Gemini model to use                  |
| `SYSTEM_PROMPT`  | built-in default  | Custom persona for the bot           |
| `PORT`           | `5000`            | Server port                          |
| `FLASK_DEBUG`    | `0`               | Set to `1` for debug mode            |

## How It Works

1. The user types a message in the web UI.
2. The frontend sends a `POST /api/chat` request with the message and session ID.
3. The Flask backend loads the session's conversation history and sends it to the **Gemini API**.
4. Gemini generates a context-aware reply, which is returned to the UI and rendered.
5. History is kept in memory per session (last 20 turns), giving the bot short-term memory.

> **Note:** Session history is stored in memory, so it resets when the server restarts. Swap `ChatEngine` storage for Redis or a database for persistent memory.

## Tech Stack

- **Backend:** Python, Flask
- **AI:** Google Gemini (`google-genai` SDK)
- **Frontend:** HTML, CSS, JavaScript (vanilla), Bootstrap
- **Deployment:** Docker

## Roadmap

- [ ] Persistent chat storage (Redis / SQLite)
- [ ] Streaming responses (SSE)
- [ ] Voice input & text-to-speech
- [ ] Multiple personas via system prompts
- [ ] Rate limiting & user authentication

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Shyam** — [GitHub](https://github.com/shyam-528)
