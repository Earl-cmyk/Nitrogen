# AI Engine Agent - Smart Request Router

![AI Engine Agent](https://img.shields.io/badge/AI-Engine%20Agent-40e0d0)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat&logo=flask)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## 🚀 Overview

**AI Engine Agent** is a sophisticated Flask-based web application that intelligently routes user queries to the most appropriate AI provider based on intent classification. Instead of relying on a single AI model, this smart router analyzes your prompt and directs it to specialized agents for optimal responses.

### 🎯 Why AI Engine Agent?

Different AI models excel at different tasks. This router ensures:
- ✅ **Code questions** → Codex/Programming Agent
- ✅ **Factual lookups** → Gemini
- ✅ **Long explanations** → DeepSeek
- ✅ **Source requests** → Perplexity
- ✅ **Math/Logic puzzles** → GPAI
- ✅ **General knowledge** → ChatGPT

## ✨ Features

### 🤖 Intelligent Routing Engine
- Advanced intent classification using keyword detection & regex patterns
- Scoring-based routing system
- Fallback mechanisms for unsubscribed agents
- Real-time router preview while typing

### 🎨 Modern UI/UX
- **Dark theme** with glassmorphism design
- **Responsive layout** - works on desktop, tablet, and mobile
- **Bing-style contextual search** with real-time results
- **Fixed bottom prompt bar** for easy access
- **Collapsible sidebar** with subscription toggles
- **Live typing animations** and agent color coding

### 📊 Comprehensive Features
- **6 AI Providers**: ChatGPT, Gemini, DeepSeek, Perplexity, GPAI, Codex
- **Subscription management** with localStorage persistence
- **Request history** with session memory
- **Live router preview** - see routing decisions in real-time
- **Error handling** with graceful fallbacks
- **Mock responses** for demonstration (ready for real API integration)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python Flask, Jinja2 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Styling** | Glassmorphism, Flexbox, Grid |
| **State Management** | Flask Sessions, localStorage |
| **Icons** | Font Awesome 6 |
| **Fonts** | Google Fonts - Inter |

## 📁 Project Structure

```
ai-engine-agent/
│
├── app.py                 # Main Flask application with routing logic
├── templates/
│   └── index.html        # Single-page application UI
├── static/
│   ├── css/
│   │   └── style.css    # Glassmorphism dark theme
│   └── js/
│       └── script.js    # Frontend interactions & API calls
└── README.md
```

## 🚦 Routing Logic

| Intent | Keywords | Routed To |
|--------|----------|-----------|
| **Programming** | code, function, debug, python, javascript | Codex |
| **Sources/Links** | sources, references, citations, find | Perplexity |
| **Factual** | who is, what is, history, definition | Gemini |
| **Long-form** | explain in detail, comprehensive, elaborate | DeepSeek |
| **Math/Logic** | calculate, solve, equation, puzzle | GPAI |
| **General** | opinion, thoughts, default | ChatGPT |

## 🎮 How It Works

1. **User inputs a query** in the search bar or prompt area
2. **Engine Agent analyzes** the text using NLP scoring
3. **Intent is classified** based on keywords and patterns
4. **Query is routed** to the most suitable AI provider
5. **Response is displayed** with agent badge and color coding
6. **History is tracked** for future reference

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Dimla/ai-engine-agent.git
cd ai-engine-agent

# Create directory structure
mkdir -p templates static/css static/js

# Install Flask
pip install flask

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

## 💡 Example Queries

Try these to see the router in action:

```
🔹 "Write a Python function to reverse a string" → Routes to Codex
🔹 "Who discovered penicillin?" → Routes to Gemini
🔹 "Explain black holes in detail" → Routes to DeepSeek
🔹 "Give me sources for renewable energy" → Routes to Perplexity
🔹 "Solve for x: 2x² + 5x - 12 = 0" → Routes to GPAI
🔹 "What's your opinion on remote work?" → Routes to ChatGPT
```

## 🎨 Design Highlights

- **Glassmorphism panels** with backdrop blur
- **Dynamic agent colors** (ChatGPT: #10a37f, Gemini: #1a73e8, etc.)
- **Smooth transitions** and hover effects
- **Typing animations** for responses
- **Loading spinners** during routing
- **Toast notifications** for status updates

## 🔮 Future Enhancements

- [ ] Real API integrations (OpenAI, Google AI, etc.)
- [ ] User authentication system
- [ ] Custom agent training
- [ ] Response streaming
- [ ] Export conversation history
- [ ] Dark/light theme toggle
- [ ] Voice input support

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

## 📝 License

MIT License - feel free to use this project for learning or building your own AI router.

## 👨‍💻 Author

**MAKER** - AI Enthusiast

---

<div align="center">
  <strong>⭐ Don't forget to star the repo if you find it useful! ⭐</strong>
  <br><br>
  <sub>Built with ❤️ for the AI community</sub>
</div>
```

---

## Badges to Add at the Top:

```
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0-black)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JS-ES6-yellow)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](http://makeapullrequest.com)
```
