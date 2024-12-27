from django.db import models

class Feedback(models.Model):
    course_id = models.CharField(max_length=100, null=True, blank=True)
    instructor = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    feedback_text = models.TextField()
    processed_feedback = models.TextField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.course_id} by {self.instructor}"

class ChatHistory(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="chat_history")
    role = models.CharField(max_length=10, choices=(("user", "User"), ("assistant", "Assistant")))
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.role} - {self.content[:50]}..."

class Rating(models.Model):
    chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=((1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating} for Chat {self.chat_history.id}"
