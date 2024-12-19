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
            raw_feedback = clean_feedback(form.cleaned_data['feedback_text'])
            logger.info(f"Cleaned raw feedback: {raw_feedback}")

            # Process feedback using GPT-4
            processed_feedback = process_feedback_with_gpt4(raw_feedback)
            form.instance.processed_feedback = processed_feedback
            form.instance.processed = True
            form.save()
            logger.info(f"Feedback processed: {processed_feedback}")
            return redirect('success')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})

def processed_feedback_view(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/processed_feedback.html', {'feedbacks': feedbacks})

def success_view(request):
    return render(request, 'feedback/success.html')

def home(request):
    return render(request, 'feedback/home.html')
