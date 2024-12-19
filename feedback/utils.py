import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def process_feedback_with_gpt4(raw_feedback):
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"Process the following feedback into a more insightful and human-readable format:\n\n{raw_feedback}",
            max_tokens=150,  # Adjust based on expected output length
            temperature=0.7,  # Adjust for randomness
        )

        processed_feedback = response.choices[0].text.strip()
        return processed_feedback
    except Exception as e:
        print(f"Error processing feedback with GPT-4: {e}")
        return raw_feedback  # Return raw feedback in case of error
