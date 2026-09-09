import urllib.request
import urllib.error
import json
from config import API_KEY


API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/gemini-2.5-flash:generateContent?key={API_KEY}"
)

chat_history = []


def get_ai_response(user_text):
    """
    Sends the user's message and conversation history
    to the Gemini API and returns the AI response.
    """

    global chat_history

    chat_history.append({
        "role": "user",
        "parts": [{"text": user_text}]
    })

    data_dict = {
        "contents": chat_history
    }

    data_bytes = json.dumps(data_dict).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=data_bytes,
        method="POST"
    )

    req.add_header("Content-Type", "application/json")

    try:

        with urllib.request.urlopen(req, timeout=15) as response:

            response_data = response.read().decode("utf-8")

            response_json = json.loads(response_data)

            ai_reply = (
                response_json["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

            chat_history.append({
                "role": "model",
                "parts": [{"text": ai_reply}]
            })

            return ai_reply.strip()

    except urllib.error.HTTPError as e:

        error_details = e.read().decode("utf-8")

        chat_history.pop()

        return f"[API ERROR {e.code}]: {error_details}"

    except urllib.error.URLError:

        chat_history.pop()

        return "[NETWORK ERROR]: Could not connect to the internet."

    except Exception as e:

        chat_history.pop()