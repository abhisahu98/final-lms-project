import openai
import logging
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Set OpenAI API Key
openai.api_key = settings.OPENAI_API_KEY

def send_to_gpt(content):
    """
    Sends preprocessed feedback to GPT-4 API and returns the response.
    """
    try:
        logger.info(f"Sending content to GPT-4: {content}")

        # Correct syntax for OpenAI Python SDK <= 0.28.0
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please rephrase and correct this feedback: '{content}'."}
            ]
        )

        # Access response content
        processed_feedback = response['choices'][0]['message']['content'].strip()
        logger.info(f"GPT-4 Response: {processed_feedback}")

        return processed_feedback

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return content
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return content

def process_feedback_with_gpt4(raw_feedback):
    """
    Processes raw feedback using GPT-4.
    """
    try:
        processed_feedback = send_to_gpt(raw_feedback)
        logger.info(f"Final Processed Feedback: {processed_feedback}")
        return processed_feedback
    except Exception as e:
        logger.error(f"Error processing feedback with GPT-4: {e}")
        return raw_feedback
