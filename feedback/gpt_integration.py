import openai
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

def send_to_gpt(content, chat_history=None):
    """
    Send user input and chat history to GPT-4 for a response.
    """
    try:
        logger.info(f"Sending content to GPT-4: {content}")
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        if chat_history:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        processed_feedback = response.choices[0].message.content.strip()
        logger.info(f"GPT-4 Response: {processed_feedback}")
        return processed_feedback
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return "Error: Unable to process feedback due to API issues."
    except Exception as e:
        logger.error(f"Unexpected error during GPT processing: {e}")
        return "Error: An unexpected issue occurred while processing feedback."

def process_feedback_with_gpt4(raw_feedback):
    """
    Processes feedback with GPT-4 API. Returns processed feedback or raw feedback on failure.
    """
    return send_to_gpt(raw_feedback)

def get_gpt_response(user_message, chat_history):
    """
    Get a response from GPT-4 based on user message and chat history.
    """
    return send_to_gpt(user_message, chat_history)
