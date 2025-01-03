from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course_id', 'instructor', 'rating', 'feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'placeholder': 'Enter your feedback...'}),
        }
