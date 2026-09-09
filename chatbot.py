from google import genai
from config import API_KEY

MODEL_NAME = "gemini-3.6-flash"
THINKING_LEVEL = "minimal"
MAX_OUTPUT_TOKENS = 512

client = genai.Client(api_key=API_KEY)
previous_interaction_id = None


def stream_ai_response(user_text, update_callback, finish_callback):
    global previous_interaction_id

    try:
        generation_config = {
            "thinking_level": THINKING_LEVEL,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        }

        kwargs = {
            "model": MODEL_NAME,
            "input": user_text,
            "generation_config": generation_config,
            "stream": True,
        }

        if previous_interaction_id:
            kwargs["previous_interaction_id"] = previous_interaction_id

        stream = client.interactions.create(**kwargs)

        full_response = ""
        interaction_id = None

        for event in stream:
            event_type = getattr(event, "event_type", None)

            if event_type == "step.delta":
                delta = getattr(event, "delta", None)
                if delta is None:
                    continue

                if getattr(delta, "type", None) == "text":
                    text = getattr(delta, "text", "")
                    if text:
                        full_response += text
                        update_callback(text)

            elif event_type == "interaction.created":
                interaction = getattr(event, "interaction", None)
                if interaction:
                    interaction_id = getattr(interaction, "id", None)

            elif event_type == "interaction.completed":
                interaction = getattr(event, "interaction", None)
                if interaction:
                    interaction_id = getattr(
                        interaction, "id", interaction_id
                    )

        if interaction_id:
            previous_interaction_id = interaction_id

        finish_callback(full_response)

    except Exception as e:
        update_callback(f"\n\n[API ERROR]\n{e}")
        finish_callback("")


def clear_chat():
    global previous_interaction_id
    previous_interaction_id = None
