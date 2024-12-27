from django.contrib import admin
from .models import Feedback, ChatHistory, Rating

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'instructor', 'rating', 'feedback_text', 'processed_feedback', 'processed', 'created_at']
    search_fields = ['course_id', 'instructor', 'feedback_text', 'processed_feedback']
    list_filter = ['processed', 'rating', 'created_at']
    ordering = ['created_at']

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['feedback', 'role', 'content', 'timestamp']
    search_fields = ['content']
    list_filter = ['role', 'timestamp']
    ordering = ['timestamp']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['chat_history', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    ordering = ['created_at']

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ChatHistory, ChatHistoryAdmin)
admin.site.register(Rating, RatingAdmin)
