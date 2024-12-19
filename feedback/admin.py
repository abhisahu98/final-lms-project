from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'instructor', 'rating', 'feedback_text', 'processed_feedback', 'processed', 'created_at']
    search_fields = ['course_id', 'instructor', 'feedback_text', 'processed_feedback']
    list_filter = ['processed', 'rating', 'created_at']
    ordering = ['created_at']

admin.site.register(Feedback, FeedbackAdmin)
