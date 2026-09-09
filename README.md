# Student AI Chatbot

Fast IT Diploma microproject using Python, CustomTkinter and Gemini 3.6 Flash.

## Features
- Gemini 3.6 Flash
- Minimal thinking for lower latency
- Streaming responses
- Conversation memory
- Background API thread
- Clear Chat button
- API key excluded from GitHub

## Install

```bash
pip install -U -r requirements.txt
```

Put your API key in `config.py`, then run:

```bash
python gui.py
```

## Important
The project is optimized for fast responses, but no API can guarantee that every request will finish in under 10 seconds. Network conditions, API load, account limits and question complexity can affect latency.

The GUI streams text as soon as it arrives instead of waiting for the complete answer.
