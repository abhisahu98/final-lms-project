import openai
import logging
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Ensure OpenAI API key is set
openai.api_key = settings.OPENAI_API_KEY

def send_to_gpt(content):
    """
    Sends the cleaned feedback to GPT-4 and retrieves a processed response.
    """
    try:
        logger.info(f"Sending content to GPT-4: {content}")

        # OpenAI GPT-4 API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that processes and improves feedback."},
                {"role": "user", "content": f"Please clean up and improve this feedback: '{content}'"}
            ],
            temperature=0.7,  # Slight randomness for creative but consistent responses
            max_tokens=200
        )

        # Extract the processed text
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
    Processes feedback with GPT-4 API. Returns the processed feedback or raw feedback on failure.
    """
    return send_to_gpt(raw_feedback)
