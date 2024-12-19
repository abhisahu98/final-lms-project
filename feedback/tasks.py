from celery import shared_task
from .models import Feedback
from .gpt_integration import process_feedback_with_gpt4
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_feedback_task():
    logger.info("Starting feedback processing task...")

    # Fetch unprocessed feedbacks
    feedbacks = Feedback.objects.filter(processed=False)
    logger.info(f"Unprocessed Feedback Count: {feedbacks.count()}")

    for feedback in feedbacks:
        try:
            logger.info(f"Processing Feedback ID: {feedback.id} with Text: {feedback.feedback_text}")

            # Process feedback using GPT-4
            processed_feedback = process_feedback_with_gpt4(feedback.feedback_text)

            # Update feedback instance
            feedback.processed_feedback = processed_feedback
            feedback.processed = True
            feedback.save()

            logger.info(f"Feedback ID {feedback.id} processed successfully: {processed_feedback}")
        except Exception as e:
            logger.error(f"Error processing Feedback ID {feedback.id}: {e}")
