from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from .preprocessing import clean_feedback
from .gpt_integration import process_feedback_with_gpt4
import logging

logger = logging.getLogger(__name__)

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                # Clean raw feedback
                raw_feedback = clean_feedback(form.cleaned_data['feedback_text'])
                logger.info(f"Raw feedback cleaned: {raw_feedback}")

                # Process feedback with GPT-4
                processed_feedback = process_feedback_with_gpt4(raw_feedback)
                logger.info(f"Processed Feedback: {processed_feedback}")

                # Save feedback to the database
                feedback_instance = form.save(commit=False)
                feedback_instance.processed_feedback = processed_feedback
                feedback_instance.processed = True
                feedback_instance.save()

                logger.info("Feedback saved successfully.")
                return redirect('success')
            except Exception as e:
                logger.error(f"Error during feedback submission: {e}")
                form.add_error(None, "An error occurred while submitting your feedback.")
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})


def processed_feedback_view(request):
    """
    View to display all feedback with processed results.
    """
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/processed_feedback.html', {'feedbacks': feedbacks})


def success_view(request):
    """
    Success view to display a confirmation page.
    """
    return render(request, 'feedback/success.html')


def home(request):
    """
    Home view to display the feedback form.
    """
    return render(request, 'feedback/home.html')