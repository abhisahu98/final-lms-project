from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from .models import Feedback, ChatHistory
from .gpt_integration import process_feedback_with_gpt4, get_gpt_response
import logging

logger = logging.getLogger(__name__)

def analyze_sentiment(feedback_text):
    """
    Analyze feedback sentiment using keywords or basic logic.
    """
    negative_keywords = ["not happy", "bad", "poor", "unhelpful", "waste", "not good", "terrible", "difficult"]
    for keyword in negative_keywords:
        if keyword in feedback_text.lower():
            logger.info(f"Negative sentiment detected: {keyword}")
            return "negative"
    logger.info("Positive sentiment detected.")
    return "positive"

def submit_feedback(request):
    """
    Display the feedback form and handle feedback submission.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                raw_feedback = form.cleaned_data['feedback_text']
                processed_feedback = process_feedback_with_gpt4(raw_feedback)
                sentiment = analyze_sentiment(raw_feedback)

                # Save feedback instance
                feedback_instance = form.save(commit=False)
                feedback_instance.processed_feedback = processed_feedback
                feedback_instance.processed = True
                feedback_instance.save()

                # Redirect based on sentiment
                if sentiment == "negative":
                    logger.info(f"Redirecting to ChatGPT interaction for feedback ID {feedback_instance.id}")
                    return redirect('chatgpt_interaction', feedback_id=feedback_instance.id)

                logger.info("Redirecting to success page for positive feedback.")
                return redirect('success')
            except Exception as e:
                logger.error(f"Error during feedback submission: {e}")
                form.add_error(None, "An error occurred while submitting your feedback.")
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})

def chatgpt_interaction(request, feedback_id):
    """
    Handle ChatGPT interaction for negative feedback.
    """
    feedback = get_object_or_404(Feedback, id=feedback_id)
    chat_history = ChatHistory.objects.filter(feedback=feedback).order_by('timestamp')

    if request.method == "POST":
        user_message = request.POST.get("user_message")
        if user_message:
            # Save user's message to the database
            ChatHistory.objects.create(feedback=feedback, role="user", content=user_message)

            # Get GPT response and save it to the database
            gpt_response = get_gpt_response(user_message, [{"role": msg.role, "content": msg.content} for msg in chat_history])
            ChatHistory.objects.create(feedback=feedback, role="assistant", content=gpt_response)

    chat_history = ChatHistory.objects.filter(feedback=feedback).order_by('timestamp')
    return render(request, 'feedback/chatgpt_interaction.html', {
        'feedback': feedback,
        'chat_history': chat_history,
    })

def success_view(request):
    """
    Render the success page after feedback submission.
    """
    return render(request, 'feedback/success.html')
