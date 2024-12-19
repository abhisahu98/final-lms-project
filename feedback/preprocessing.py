import re

def clean_feedback(feedback_text):
    """Clean and capitalize feedback text."""
    feedback_text = re.sub(r'\s+', ' ', feedback_text.strip())  # Remove extra spaces
    feedback_text = feedback_text[0].capitalize() + feedback_text[1:]  # Capitalize first word
    feedback_text = re.sub(r'\bi\b', 'I', feedback_text)  # Replace "i" with "I"
    feedback_text = re.sub(r'\blol\b', 'LOL', feedback_text)  # Replace "lol" with "LOL"
    return feedback_text

def summarize_feedback(feedback_text):
    """Classify feedback into a category."""
    feedback_text = clean_feedback(feedback_text)
    category = "General"

    if "slow" in feedback_text.lower() or "performance" in feedback_text.lower():
        category = "Platform Performance"
    elif "quiz" in feedback_text.lower() or "question" in feedback_text.lower():
        category = "Quiz Difficulty"
    elif "video" in feedback_text.lower() or "content" in feedback_text.lower():
        category = "Content Quality"
    elif "great" in feedback_text.lower() or "helpful" in feedback_text.lower():
        category = "Positive Feedback"

    return feedback_text.capitalize(), category
